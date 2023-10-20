import abc
from typing import Tuple, List

import cv2
import numpy as np
from fastdtw import fastdtw
from tqdm import tqdm

from src.heigher_service.runner_interface import RunnerI
from src.service.distance_avg_reasonable_interface import DistanceAvgReasonableI
from src.service.impl.DistanceAvgReasonableImpl import DistanceAvgReasonableImpl
from src.service.impl.video_creator_ffmpeg_impl import VideoCreatorFfmpegImpl
from src.service.impl.video_creator_impl import VideoCreatorImpl
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl
from src.service.video_creator_interface import VideoCreatorI
from src.service.video_iterator_interface import VideoIteratorPrefixI


class PathSetI(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self): ...

    @abc.abstractmethod
    def exist(self, path: Tuple) -> bool: ...  # 返回布尔值表示是否重复

    @abc.abstractmethod
    def add(self, path: Tuple) -> bool: ...  # 返回布尔值表示是否重复

    @abc.abstractmethod
    def pop(self) -> (List[int], List[int]): ...  # 推出所有的内容，在最后恢复迭代器使用

    @abc.abstractmethod
    def handle(self, feature_a_list, feature_b_list, compare_func) -> ((int, int), int): ...  # 处理数据，得到最相似的两帧索引

    @abc.abstractmethod
    def is_empty(self) -> bool: ...


class PathSetImpl(PathSetI):

    def __init__(self):
        self._a_index_list = []
        self._b_index_list = []

    @staticmethod
    def _check_path(path: Tuple):
        if len(path) < 2:
            raise Exception("PathSetImpl 传入的参数不对")

    def exist(self, path: Tuple) -> bool:
        self._check_path(path)

        # 只判断B是否重复即可

        return self._b_index_list.__contains__(path[1])

        # ---

        # if len(self._a_index_list) == 1 and len(self._b_index_list) == 1:
        #     return self._a_index_list.__contains__(path[0]) or self._b_index_list.__contains__(path[1])
        # elif len(self._a_index_list) == 1:
        #     return self._a_index_list[0] == path[0]
        # elif len(self._b_index_list) == 1:
        #     return self._b_index_list[0] == path[1]
        # else:
        #     return False

        # return self._a_index_list.__contains__(path[0]) or self._b_index_list.__contains__(path[1])

    def add(self, path: Tuple) -> bool:
        self._check_path(path)

        flag_exist = self.exist(path)

        if not flag_exist:
            self._a_index_list.clear()
            self._b_index_list.clear()

        if not self._a_index_list.__contains__(path[0]):
            self._a_index_list.append(path[0])
        if not self._b_index_list.__contains__(path[1]):
            self._b_index_list.append(path[1])

        return flag_exist

    def pop(self) -> (List[int], List[int]):

        return_a, return_b = [], []
        for index in self._a_index_list:
            return_a.append(index)
        for index in self._b_index_list:
            return_b.append(index)

        self._a_index_list.clear()
        self._b_index_list.clear()

        return return_a, return_b

    def handle(self, feature_a_list, feature_b_list, compare_func) -> ((int, int), int):
        check = len(self._a_index_list) > 1 and len(self._b_index_list) > 1  # 两个数组都大于1是错误的
        if check:
            raise Exception("# 两个数组都大于1是错误的")

        min_distance = float('inf')  # 初始化最小差异值为无穷大
        min_a_index = None  # 初始化对应的 a_index
        min_b_index = None  # 初始化对应的 b_index

        for a_index in self._a_index_list:
            for b_index in self._b_index_list:
                distance = compare_func(feature_a_list[a_index], feature_b_list[b_index])  # 得到差异值
                if distance < min_distance:  # 如果当前差异值小于已找到的最小差异值，则更新最小差异值和对应的索引
                    min_distance = distance
                    min_a_index = a_index
                    min_b_index = b_index

        if min_a_index is None or min_b_index is None:  # 如果没有找到有效的索引，则抛出异常
            raise Exception("No valid indices found")

        # self.pop()

        return (min_a_index, min_b_index), min_distance  # 返回差异值最小的 a_index 和 b_index

    def is_empty(self) -> bool:
        return len(self._a_index_list) == 0 and len(self._b_index_list) == 0


class SiftModelSingleImpl:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = cv2.SIFT_create()
            print("inited model")
        return cls._instance

    def get_model(self):
        return self.model


# 双指针使用dtw进行比对
class TwoPFastDtwSiftImpl(RunnerI):

    def __init__(self, v_a_path, v_b_path, a_iterator=None, b_iterator=None, model=None, output_path=None,
                 output_fps=None, output_size=None, pool_size=None, debug_window=True):
        self.v_a_path = v_a_path
        self.v_b_path = v_b_path
        self.pool_size = pool_size or 100
        self.debug_window = debug_window

        self.a_iterator: VideoIteratorPrefixI = a_iterator or VideoIteratorPrefixImpl(self.v_a_path)
        self.b_iterator: VideoIteratorPrefixI = b_iterator or VideoIteratorPrefixImpl(self.v_b_path)
        # self.model = model or cv2.SIFT_create() # 目前没用上

        self.creator: VideoCreatorI = self.get_video_creator(output_path, output_fps, output_size)  # todo 测试阶段不用生成
        self.common_size = self.get_small_size()

        range_time = self.b_iterator.get_total_f_num() if self.b_iterator.get_total_f_num() < self.a_iterator.get_total_f_num() else self.a_iterator.get_total_f_num()
        self.pbar = tqdm(total=range_time, desc="fast dtw and sift 逐帧对比", unit="帧")

        self.distance_avg_reasonable_check: DistanceAvgReasonableI = DistanceAvgReasonableImpl(
            reasonable_avg=85)  # 可以修改参数

    def get_small_size(self):
        fps, (a_w, a_h) = self.a_iterator.get_video_info()
        fps, (b_w, b_h) = self.b_iterator.get_video_info()
        common_size = (a_w, a_h) if a_w < b_w and a_h < b_h else (b_w, b_h)
        return common_size

    def get_video_creator(self, path, fps, size) -> VideoCreatorI:
        fps_a, (a_w, a_h) = self.a_iterator.get_video_info()
        print(f"A info {fps_a},({a_w},{a_h})")
        fps_b, (b_w, b_h) = self.b_iterator.get_video_info()
        print(f"B info {fps_b},({b_w},{b_h})")

        # 使用高画质，算法原因只能使用低帧率
        output_path = path or self.v_b_path
        # if fps is None:
        #     fps = fps_a if fps_a < fps_b else fps_b
        output_fps = fps_b
        if size is None:
            size = (a_w, a_h) if a_w * a_h > b_w * b_h else (b_w, b_h)
        output_size = size

        print(f"output info {output_fps},{output_size}")

        # return VideoCreatorImpl(output_path, output_fps, output_size)
        return VideoCreatorFfmpegImpl(filename=output_path, fps=output_fps, frame_size=output_size)

    def get_feature(self, frame) -> np.ndarray:

        if frame.shape[1] > self.common_size[0] and frame.shape[0] > self.common_size[1]:
            # 计算视频B的长宽比
            aspect_ratio_b = self.common_size[0] / self.common_size[1]  # 宽度/高度

            # 计算中间截取区域的宽度和高度
            center_y, center_x = frame.shape[0] // 2, frame.shape[1] // 2
            if frame.shape[1] / frame.shape[0] > aspect_ratio_b:
                # 如果视频A的长宽比大于视频B的长宽比，则保持高度不变，调整宽度
                crop_height = frame.shape[0]
                crop_width = int(crop_height * aspect_ratio_b)
            else:
                # 如果视频A的长宽比小于等于视频B的长宽比，则保持宽度不变，调整高度
                crop_width = frame.shape[1]
                crop_height = int(crop_width / aspect_ratio_b)

            # 计算裁剪区域的边界
            crop_x_start = center_x - crop_width // 2
            crop_x_end = center_x + crop_width // 2
            crop_y_start = center_y - crop_height // 2
            crop_y_end = center_y + crop_height // 2

            # 从视频A的中间按照视频B的长宽比截取
            cropped_frame_a = frame[crop_y_start:crop_y_end, crop_x_start:crop_x_end]

            # 调整截取后的frame_a的分辨率以匹配frame_b
            resized_frame_a = cv2.resize(cropped_frame_a, (int(self.common_size[0] / 2), int(self.common_size[1] / 2)),
                                         interpolation=cv2.INTER_AREA)
            # resized_frame_b = cv2.resize(frame_b, (cropped_frame_a.shape[1], cropped_frame_a.shape[0]),
            #                              interpolation=cv2.INTER_AREA)

            resized_frame_a = cv2.cvtColor(resized_frame_a, cv2.COLOR_BGR2GRAY)

            return resized_frame_a
        else:
            frame = cv2.resize(frame,
                               (int(self.common_size[0] / 2), int(self.common_size[1] / 2)))  # 调整帧大小来降低计算量

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        return frame

    def _cut_frame(self, frame_a, frame_b):

        # 计算裁剪区域的边界（如果需要进一步裁剪）
        height, width = frame_b.shape[:2]
        crop_width_start = width // 5
        crop_width_end = 4 * width // 5
        crop_height_start = height // 5
        crop_height_end = 4 * height // 5

        # 裁剪调整分辨率后的frame_a和frame_b的中间3/5的区域
        final_cropped_frame_a = frame_a[crop_height_start:crop_height_end, crop_width_start:crop_width_end]
        final_cropped_frame_b = frame_b[crop_height_start:crop_height_end, crop_width_start:crop_width_end]

        return final_cropped_frame_a, final_cropped_frame_b

    @staticmethod
    def draw_matches(distance, feature_a, feature_b, good_matches=None, keypoints1=None, keypoints2=None):
        # Draw matches
        img_matches = cv2.drawMatches(feature_a, keypoints1, feature_b, keypoints2, good_matches, outImg=None)
        height, width, _ = img_matches.shape
        center_coordinates = (3, height - 3)
        font_scale = 1
        font_color = (0, 255, 0)  # Green color
        thickness = 2
        cv2.putText(img_matches, f'{distance:.2f}', center_coordinates, cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale, font_color, thickness)
        cv2.imshow('Matches', img_matches)
        cv2.waitKey(1)

    @staticmethod
    def get_distance(feature_a, feature_b) -> float:
        global descriptors1, descriptors2, keypoints1, keypoints2, good_matches
        try:
            feature_a = feature_a.astype(np.uint8)
            feature_b = feature_b.astype(np.uint8)

            # Find the keypoints and descriptors with SIFT
            keypoints1, descriptors1 = SiftModelSingleImpl().get_model().detectAndCompute(feature_a, None)
            keypoints2, descriptors2 = SiftModelSingleImpl().get_model().detectAndCompute(feature_b, None)
        except Exception as e:
            print(e.args)

        if descriptors1 is None or descriptors2 is None or descriptors1.size == 0 or descriptors2.size == 0:
            # print("Descriptors are empty.")
            if descriptors1 is None:
                return 80
            if descriptors2 is None:
                return 60
        try:
            # Use BFMatcher to find matches
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(descriptors1, descriptors2, k=2)

            # Apply ratio test
            good_matches = []
            # for element in matches: # 修改可能导致异常
            #     try:
            #         m, n = element
            #         if m.distance < 0.88 * n.distance:
            #             good_matches.append(m)
            #     except Exception as e:
            #         print('catch err', end='')
            #         continue

            for m, n in matches:
                if m.distance < 0.88 * n.distance:
                    good_matches.append(m)

            # Print the number of good matches
            # print(len(good_matches))

            similarity = 0  # 如果黑屏则确认匹配
            if (len(keypoints1) + len(keypoints2)) != 0:
                similarity = len(good_matches) / (len(keypoints1) + len(keypoints2))

            # print(similarity)

        except Exception as e:
            print(f"出现异常 {e.args}")
            # print(f"-/-", end='')  # todo 有时间看看
            # for m, n in matches: 报的异常：('not enough values to unpack (expected 2, got 1)',) 没敢改因为怕影响结果
            similarity = 0.2

        distance = 1 - similarity  # 可以加上一个 判断。

        if distance > 0.8:
            distance = 1

        distance *= 100

        # Draw matches
        TwoPFastDtwSiftImpl.draw_matches(distance=distance, feature_a=feature_a, feature_b=feature_b,
                                         good_matches=good_matches, keypoints1=keypoints1, keypoints2=keypoints2)

        return distance

    def run(self):
        # 遍历双指针。
        # 每次固定长度进行dtw，为了让每段能够衔接，所以要保存对应长度的 feature队列和frame队列 以便之后比对和衔接.
        # 得到distance 和 path 之后。
        # 遍历path ，每次将path对 判断是否重复。
        # 如果重复，则加入暂且不管
        # 如果不重复，则要调用一个方法对缓存进行比对。得到最匹配的 索引对 。我们要写的，也就是这个了。之后在加入
        # path 遍历结束之后，如果 数据结构中仍有值。说明后面没有对齐，如果指针未结束，这些值应该重新放回对应的迭代器当中。
        # 所以并且清空几个队列
        # 在指针都循环结束之后，再处理一次 数据结构 将剩余的值写入

        # 缓存机制，方便进行比对和写操作，同时方便迭代器进行恢复
        frame_queue_a, frame_queue_b = [], []
        feature_queue_a, feature_queue_b = [], []

        p_set: PathSetI = PathSetImpl()

        while True:
            try:
                frame_a = next(self.a_iterator)
                frame_b = next(self.b_iterator)

                self.show_frames(frame_a, frame_b)
            except StopIteration:
                break

            frame_queue_a.append(frame_a)
            frame_queue_b.append(frame_b)

            feature_a = self.get_feature(frame_a)
            feature_b = self.get_feature(frame_b)
            feature_a, feature_b = self._cut_frame(feature_a, feature_b)

            feature_queue_a.append(feature_a)
            feature_queue_b.append(feature_b)

            # 判断数量是否够了
            if len(feature_queue_a) >= self.pool_size:
                # 使用 fastdtw 函数计算 DTW 对齐
                distance, path = fastdtw(feature_queue_a, feature_queue_b, dist=self.get_distance)
                print(f"fast dtw distance: [{distance}]")
                total_path_num = len(path)

                write_size = 0  # 进度统计

                for i in range(total_path_num):
                    index_a, index_b = path[i]

                    stopping_flag = total_path_num - i <= 50
                    jump_a_flag = False

                    if p_set.exist((index_a, index_b)):
                        p_set.add((index_a, index_b))
                        continue
                    if not p_set.is_empty():
                        # 如果不存在 且 不为空 则处理。
                        (same_index_a, same_index_b), min_distance = p_set.handle(feature_queue_a, feature_queue_b,
                                                                                  self.get_distance)

                        self.distance_avg_reasonable_check.add_index_tuple_and_distance(same_index_a, same_index_b,
                                                                                        min_distance)

                        if not self.distance_avg_reasonable_check.avg_reasonable(stopping_flag):
                            confirm_index_list, _ = self.distance_avg_reasonable_check.get_rb_list_and_b_index()

                            tmp_a_index, tmp_b_index = 0, 0

                            for tmp_a_index, tmp_b_index in confirm_index_list:
                                # 写操作
                                self.show_when_write(frame_queue_a[tmp_a_index], frame_queue_b[tmp_b_index])
                                self.creator.write_frame(frame_queue_a[tmp_a_index])  # todo 测试阶段不用生成
                                write_size += 1
                                # ---

                            # --- 跳A 开始
                            print("开始跳A")
                            if tmp_a_index < len(frame_queue_a):
                                self.a_iterator.add_prefix(frame_queue_a[tmp_a_index:])
                            if tmp_b_index < len(frame_queue_b):
                                self.b_iterator.add_prefix(frame_queue_b[tmp_b_index:])

                            tmp_frame_a_queue, tmp_frame_b_queue = [], []

                            frame_b = next(self.b_iterator)
                            tmp_frame_b_queue.append(frame_b)
                            feature_b = self.get_feature(frame_b)

                            tmp_count = 0

                            while True:  # 跳A ，从这个点开始，B 不动，A向后遍历 。直到满足条件
                                try:
                                    frame_a = next(self.a_iterator)
                                    feature_a = self.get_feature(frame_a)
                                    tmp_frame_a_queue.append(frame_a)
                                    tmp_count += 1

                                    feature_a, tmp_feature_b = self._cut_frame(feature_a, feature_b)

                                    distance = self.get_distance(feature_a, tmp_feature_b)

                                    if distance < 70:
                                        self.a_iterator.add_prefix([frame_a])
                                        self.b_iterator.add_prefix([frame_b])

                                        self.distance_avg_reasonable_check: DistanceAvgReasonableI = DistanceAvgReasonableImpl(
                                            reasonable_avg=85)  # 可以修改参数

                                        print(f"跳帧成功 A跳{tmp_count}帧")
                                        break

                                    if tmp_count > 1000:
                                        raise StopIteration

                                except StopIteration:
                                    print("跳A失败")
                                    self.distance_avg_reasonable_check.upd_reasonable_avg(3)
                                    self.a_iterator.add_prefix(tmp_frame_a_queue)
                                    self.b_iterator.add_prefix(tmp_frame_b_queue)
                                    tmp_frame_a_queue.clear()
                                    tmp_frame_b_queue.clear()
                                    break

                            # --- 跳A结束

                            jump_a_flag = True
                            p_set.pop()
                            break  # break 是防止调用50帧荣誉方法
                        else:
                            if stopping_flag:
                                index_list = self.distance_avg_reasonable_check.pop_all()  # todo 处理写操作

                                for tmp_a_index, tmp_b_index in index_list:
                                    # 写操作
                                    self.show_when_write(frame_queue_a[tmp_a_index], frame_queue_b[tmp_b_index])
                                    self.creator.write_frame(frame_queue_a[tmp_a_index])  # todo 测试阶段不用生成
                                    write_size += 1
                                    # ---
                            else:
                                (first_a_index,
                                 first_b_index), enough = self.distance_avg_reasonable_check.pop_first_index_t()

                                if enough:
                                    # 写操作
                                    self.show_when_write(frame_queue_a[first_a_index], frame_queue_b[first_b_index])
                                    self.creator.write_frame(frame_queue_a[first_a_index])  # todo 测试阶段不用生成
                                    write_size += 1
                                    # ---

                        if not jump_a_flag and stopping_flag:  # 如果没有重复的，留下50帧荣誉
                            self.a_iterator.add_prefix(frame_queue_a[index_a:])
                            self.b_iterator.add_prefix(frame_queue_b[index_b:])
                            print("break 50 帧冗余")
                            p_set.pop()
                            break
                        p_set.add((index_a, index_b))  # 和下面重复了，这里是为了 50 帧 break 的时候不要重复添加帧
                    else:
                        p_set.add((index_a, index_b))

                if not p_set.is_empty():  # 其实这里不可能是empty，但是最后一对无法判断是否匹配。所以索性没问题
                    a_index_list, b_index_list = p_set.pop()
                    tmp_frame_a_list = []
                    tmp_frame_b_list = []
                    for a_index in a_index_list:
                        tmp_frame_a_list.append(frame_queue_a[a_index])
                    for b_index in b_index_list:
                        tmp_frame_b_list.append(frame_queue_b[b_index])

                    self.a_iterator.add_prefix(tmp_frame_a_list)
                    self.b_iterator.add_prefix(tmp_frame_b_list)

                self.pbar.update(write_size)  # 进度统计

                # 清空缓存
                frame_queue_a.clear()
                frame_queue_b.clear()
                feature_queue_a.clear()
                feature_queue_b.clear()

        print("收尾阶段")
        # feature 队列仍有剩余
        # 使用 fastdtw 函数计算 DTW 对齐
        distance, path = fastdtw(feature_queue_a, feature_queue_b, dist=self.get_distance)
        print(f"fast dtw distance: [{distance}]")

        write_size = 0  # 进度统计
        for index_a, index_b in path:
            if p_set.exist((index_a, index_b)):
                p_set.add((index_a, index_b))
                continue

            if not p_set.is_empty():
                (same_index_a, same_index_b), min_distance = p_set.handle(feature_queue_a, feature_queue_b,
                                                                          self.get_distance)
                # 写操作
                self.show_when_write(frame_queue_a[same_index_a], frame_queue_b[same_index_b])
                self.creator.write_frame(frame_queue_a[same_index_a])  # todo 测试阶段不用生成
                write_size += 1
                # ---
            p_set.add((index_a, index_b))

        self.pbar.update(write_size)  # 进度统计

        (same_index_a, same_index_b), min_distance = p_set.handle(feature_queue_a, feature_queue_b, self.get_distance)
        # 写操作
        self.show_when_write(frame_queue_a[same_index_a], frame_queue_b[same_index_b])
        self.creator.write_frame(frame_queue_a[same_index_a])  # todo 测试阶段不用生成
        write_size += 1
        # ---
        self.pbar.update(1)  # 进度统计

        self.done_method()  # 程序结束

    def done_method(self):
        self.pbar.close()
        self.creator.release()  # todo 测试阶段不用生成

        print("结束")

    def show_when_write(self, frame_a, frame_b):

        if self.debug_window:
            # 确保两个帧的维度相同
            if frame_a.shape != frame_b.shape:
                # print("Frames have different dimensions, resizing frame2 to match frame1")
                frame_a = cv2.resize(frame_a, (frame_b.shape[1], frame_b.shape[0]))

            # 使用numpy的hstack函数水平堆叠两个帧
            merged_frame = np.hstack((frame_a, frame_b))

            # 使用cv2.imshow展示合并后的帧
            cv2.imshow('writing Frame', merged_frame)
            cv2.waitKey(1)

    def show_frames(self, frame_a, frame_b):
        if self.debug_window:
            cv2.imshow("rolling A", frame_a)
            cv2.imshow("rolling B", frame_b)
            cv2.waitKey(1)
