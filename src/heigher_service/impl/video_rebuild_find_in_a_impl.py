import sys
import time
from collections import deque
from multiprocessing import Process, Pool, Queue
from threading import Thread

import PIL
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

from src.entity.entitys import KeyFrame
from src.heigher_service.impl.two_p_fast_dtw_orb_impl import TwoPFastDtwOrbImpl
from src.heigher_service.impl.two_p_fast_dtw_sift_impl import TwoPFastDtwSiftImpl
from src.heigher_service.runner_interface import RunnerI
from src.heigher_service.utils.common import BLUtils
from src.heigher_service.utils.common_sequence import CSUtils
from src.heigher_service.utils.frame_cut_util import FrameCutUtilXiGua
from src.service.impl.featuer_iterator_cache_impl import FeatureIteratorCacheImpl, GlobalFeatureMap, GlobalImageMap, \
    GlobalHistList, GlobalAvgHashMap
from src.service.impl.video_creator_impl import VideoCreatorImpl
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl, VideoIteratorImpl
from src.service.impl.video_key_frames_impl import VideoKeyFramesImpl
from src.service.video_iterator_interface import VideoIteratorI, FeatureIteratorI
from src.service.video_key_frames_interface import VideoKeyFramesI
from SSIM_PIL import compare_ssim as compare_ssim_gpu


class VideoRebuildFindInAImpl(RunnerI):

    def __init__(self, dst_path: str, target_path: str, output_path=None):
        self.dst_path = dst_path
        self.target_path = target_path

        if output_path is not None:
            self.output_path = output_path
        else:
            self.output_path = BLUtils.get_unique_filename(self.target_path)

        self.crop_info_path = 'static/crop_info_xi_gua.json'

        self.finder_num = 5

        # 获取两个视频的最小公共 size
        self.common_size = BLUtils.get_common_size(self.dst_path, self.target_path)
        print(f'计算common_size = [{self.common_size}]')
        # --局部变量！
        # self.pool = Pool(self.finder_num)

        # self.video_creator = self._get_video_creator()

    def run(self):

        found_a_b_len_tuples = self.find_same_points()

        print(found_a_b_len_tuples)

        # 根据这个信息制作 video.xml

    def find_same_points(self):
        found_a_b_len_tuples = []  # (a start,b start ,len)
        self.load_video_into_cache()
        # 获取两个视频的最小公共 size
        iterator_b: FeatureIteratorI = FeatureIteratorCacheImpl(self.target_path, self.common_size, self.crop_info_path)
        tbar = tqdm(desc='整体进度', unit='帧', total=iterator_b.get_total_f_num())
        total_distance = 0
        count = 0
        # 直接拿B的帧去A中寻找，第一步找到多个可能值，第二步从这些可能值中找到最长的，保存下来。从这个点继续向后匹配
        while True:
            try:
                feature_b = next(iterator_b)
            except StopIteration:
                break

            # 第一步
            possibly_a_starts = self.find_possibly_a_starts(self.common_size, feature_b)

            # 第二步，寻找最长的正确匹配
            # 2.1 从多个起点处获得多个迭代器以及匹配好的长度,不要忘了释放资源
            working_a_iterators = self._generate_working_a_iterators(self.common_size, iterator_b, possibly_a_starts)

            if len(working_a_iterators) == 0:
                continue

            # 2.2 筛选出最合理的a迭代器
            best_a_iterator, longest_len, distance = self._get_best_a_iterator_with_distance(working_a_iterators)

            # if longest_len == 1:
            #     continue

            a_start = best_a_iterator.get_current_index()
            b_start = iterator_b.get_current_index()

            found_a_b_len_tuples.append((a_start, b_start, longest_len))

            # --- 可以在这类保存
            iterator_b.set_current_index(iterator_b.get_current_index() + longest_len - 1)
            # ---<

            best_a_iterator.release()

            # log
            tbar.update(longest_len)
            count += longest_len
            total_distance += distance
            tbar.set_postfix_str(
                f'abl ({a_start, b_start, longest_len}) 整体差异值[total:{int(total_distance)}/{iterator_b.get_current_index()} pre:{int(total_distance / iterator_b.get_current_index())}] 丢失:{iterator_b.get_current_index() + 1 - count}')
        tbar.close()
        iterator_a: FeatureIteratorI = FeatureIteratorCacheImpl(self.dst_path, self.common_size, self.crop_info_path)
        iterator_a.do_release()
        iterator_b.do_release()
        return found_a_b_len_tuples

    @staticmethod
    def _load_video_into_cache(dst_path, start, end, q: Queue, common_size, crop_info_path):
        iterator_a = VideoIteratorImpl(dst_path)
        iterator_a.set_current_index(start)
        # iterator_a.total_f_size = end
        while True:
            current_index = iterator_a.get_current_index()
            try:
                frame = next(iterator_a)
                if iterator_a.get_current_index() > end:
                    break
            except StopIteration:
                break

            feature = BLUtils.get_cropped_feature(frame, common_size, crop_info_path)

            # rgb_image = cv2.cvtColor(feature, cv2.COLOR_BGR2RGB)

            # 将 NumPy 数组转换为 PIL 图像
            # pil_image = Image.fromarray(rgb_image)

            q.put((current_index, feature))

        iterator_a.release()

    def load_video_into_cache(self):
        print('将视频加入内存')
        iterator_a = FeatureIteratorCacheImpl(self.dst_path, self.common_size,
                                              self.crop_info_path)

        q = Queue()

        # 每个进程要负责的长度是多少
        pre_task = int(iterator_a.get_total_f_num() / self.finder_num)
        process_list = []

        for i in range(self.finder_num):  # 开启5个子进程执行fun1函数
            start = i * pre_task
            end = (i + 1) * pre_task - 1
            if i == self.finder_num - 1:
                end = iterator_a.get_total_f_num()
            print(f'start,end = {start},{end}')

            p = Process(target=self._load_video_into_cache,
                        args=(self.dst_path, start, end, q, self.common_size, self.crop_info_path))  # 实例化进程对象
            p.start()

        # for p in process_list:
        #     p.join()
        # process_list.clear()

        # print(q.queue)
        # time.sleep(5)

        # 全局map 初始化
        GlobalFeatureMap().feature_map[self.dst_path] = {}

        tbar1 = tqdm(desc='正在加载视频', unit='帧', total=iterator_a.get_total_f_num())
        count = 0
        while True:
            try:
                frame_index, feature = q.get(timeout=5)
                GlobalFeatureMap().feature_map[self.dst_path][frame_index] = feature
                GlobalAvgHashMap().add_feature(self.dst_path, index=frame_index, feature=feature)
                count += 1
                tbar1.update(1)
                # print(frame_index,end='')
            except Exception:
                break

        tbar1.close()

        print(f'多进程加载完成 [{count}]')

        tbar = tqdm(desc='验证加载', unit='帧', total=iterator_a.get_total_f_num())

        while True:
            try:
                feature = next(iterator_a)
                # print(f'读取{iterator_a.get_current_index()}')
                GlobalAvgHashMap().add_feature(self.dst_path, index=iterator_a.get_current_index(), feature=feature)
                tbar.update(1)
            except StopIteration:
                break

        print('补充完毕')
        tbar.close()

        # q.task_done()

        print('将视频加入内存 done')
        iterator_a.release()

    def _get_best_a_iterator_with_distance(self, working_a_iterators):
        working_a_iterators.sort(key=lambda x: x[2] / x[1])  # 由大到小排序
        best_a_iterator, longest_len, total_distance = working_a_iterators[0]

        for item in working_a_iterators:
            temp_w_a_iterator, long, _ = item
            if long != longest_len:
                temp_w_a_iterator.release()
        working_a_iterators.clear()
        print(
            f'最精确匹配长度为[{longest_len}],distance[total:{total_distance}/pre:{int(total_distance / longest_len)}]')
        return best_a_iterator, longest_len, total_distance

    def _get_best_a_iterator(self, working_a_iterators):
        working_a_iterators.sort(key=lambda x: x[1], reverse=True)  # 由大到小排序
        best_a_iterator, longest_len, total_distance = working_a_iterators[0]

        for item in working_a_iterators:
            temp_w_a_iterator, long, _ = item
            if long != longest_len:
                temp_w_a_iterator.release()
        working_a_iterators.clear()
        print(
            f'最长成功匹配长度为[{longest_len}],distance[total:{total_distance}/pre:{int(total_distance / longest_len)}]')
        return best_a_iterator, longest_len, total_distance

    def _generate_working_a_iterators(self, common_size, iterator_b, possibly_a_starts):
        print('即将从每个大致起点向下迭代寻找最佳起点')
        working_a_iterators = []  # (iter,len,total_distance)
        for p_a_s in possibly_a_starts:
            # 这是的a起点为 p_a_s b起点为fb.current_index
            temp_iterator_a, temp_iterator_b = FeatureIteratorCacheImpl(self.dst_path, common_size,
                                                                        self.crop_info_path), FeatureIteratorCacheImpl(
                self.target_path, common_size, self.crop_info_path)
            temp_iterator_a.set_current_index(p_a_s)
            temp_iterator_b.set_current_index(iterator_b.get_current_index()-1)  # !! 索引问题，因为上一步使用了数组，所以这里b迭代器索引-1

            # 逐帧比较两个迭代器，遇到第一个合理的值之后，从十个中选一个最合理的再向后匹配
            temp_feature_b = next(temp_iterator_b)

            # 寻找最合理的A起点
            self._set_temp_a_iterator_index_to_best_compare(common_size, temp_feature_b, temp_iterator_a)

            # if temp_iterator_a.get_current_index() == p_a_s:
            #     raise Exception('严重问题！！！')

            temp_len = 1
            temp_distance = 100

            count = 0

            # 这一帧B已经比对过了
            while True:
                try:
                    temp_feature_a = next(temp_iterator_a)
                    temp_feature_b = next(temp_iterator_b)
                    count += 1
                except StopIteration:
                    break

                distance = BLUtils.get_distance(temp_feature_a, temp_feature_b)
                # if not distance < 10:
                #     break

                if count > 10 and not distance < 3:
                    break

                if temp_distance == 100:
                    temp_distance = 0

                temp_len += 1
                temp_distance += distance

            temp_iterator_a.set_current_index(temp_iterator_a.get_current_index() - temp_len)

            working_a_iterators.append((temp_iterator_a, temp_len, temp_distance))
            temp_iterator_b.release()
        print(f'生成迭代器数量:[{len(working_a_iterators)}]')
        return working_a_iterators

    def _set_temp_a_iterator_index_to_best_compare(self, common_size, temp_feature_b, temp_iterator_a):
        print('寻找最合理的A起点')
        short_a_start_list = []  # 候选a起点列表
        found = False
        while True:
            current_index = temp_iterator_a.get_current_index()
            try:
                temp_feature_a = next(temp_iterator_a)
            except StopIteration:
                break

            distance = BLUtils.get_distance(temp_feature_a, temp_feature_b)

            # if found and not distance < 10:
            #     break
            #
            # if not distance < 10:
            #     continue

            found = True
            short_a_start_list.append((current_index, distance))

            if len(short_a_start_list) > 10:
                short_a_start_list.sort(key=lambda x: x[1])  # 由小到大排序
                # print('起点差异值数组', short_a_start_list)

                # 选择差异值最小的点作为起点
                final_a_start, min_distance = short_a_start_list[0]
                temp_iterator_a.set_current_index(final_a_start)
                print(f'最小差异值[{min_distance}] 起点索引:{final_a_start}')
                return

        if found:
            short_a_start_list.sort(key=lambda x: x[1])  # 由小到大排序
            # print(short_a_start_list)
            # print('起点差异值数组', short_a_start_list)

            # 选择差异值最小的点作为起点
            final_a_start, min_distance = short_a_start_list[0]
            temp_iterator_a.set_current_index(final_a_start)
            print(f'最小差异值[{min_distance}] 起点索引:{final_a_start} 总数<10')

    @staticmethod
    def find_possibly_a_start_interval(pre_start, pre_end, process_index, temp_map, feature_b,
                                       q: Queue):
        # temp_iterator = FeatureIteratorCacheImpl(self.dst_path, self.common_size, self.crop_info_path)
        # temp_map = GlobalFeatureMap().feature_map[self.dst_path]
        # temp_iterator.set_current_index(pre_start)
        # temp_iterator.total_f_size = pre_end

        current_index = pre_start

        min_distance = 999
        # 第一步，寻找所有可能的起点
        while True:
            # print('计算')
            if current_index >= pre_end:
                break
            feature_a = temp_map[current_index]
            distance = BLUtils.get_distance(feature_a, feature_b)
            if distance < 20:
                if distance < min_distance:
                    min_distance = distance
                q.put(current_index)
                # print(f'加入{current_index}')
                # tbar.set_postfix_str(
                #     f'找到了[{len(temp_possibly_a_starts)}]个起点，当前起点差异值[{int(distance)}]，最小差异值[{int(min_distance)}]')

            current_index += 3
        # print('结束')

    def find_possibly_a_starts(self, common_size, feature_b):
        # feature_iterator_a = FeatureIteratorCacheImpl(self.dst_path, common_size, self.crop_info_path)

        # possibly_a_starts = self.find_possibly_start_point_cpu_nomal(feature_b, feature_iterator_a)

        possibly_a_starts = self._2_step_find(feature_b)

        # print(possibly_a_starts)

        # tbar.close()
        # 起点归一化
        print('起点归一化')
        final_possibly_a_starts = []
        for p_a_s in possibly_a_starts:
            new_p_a_s = p_a_s - p_a_s % 10
            if not final_possibly_a_starts.__contains__(new_p_a_s):
                final_possibly_a_starts.append(new_p_a_s)
        print(f'剩余[{len(final_possibly_a_starts)}]个起点 [{final_possibly_a_starts}]')

        return final_possibly_a_starts

    def _2_step_find(self, feature_b):
        hash_b = BLUtils.average_hash(feature_b)

        indices = []
        min_hash_distance = 99999
        # 从hash数组中寻找接近的值
        for index_key, hash_a in GlobalAvgHashMap().avg_hash_map[self.dst_path].items():
            distance = BLUtils.hamming_distance(hash_a, hash_b)

            if distance < min_hash_distance:
                min_hash_distance = distance
            # print(distance)
            if distance < 5:
                indices.append(index_key)

        possibly_a_starts = []
        min_distance = 999
        for index_a in indices:
            feature_a = GlobalFeatureMap().feature_map[self.dst_path][index_a]
            distance = BLUtils.get_distance(feature_a, feature_b)
            if distance < 3:
                if distance < min_distance:
                    min_distance = distance
                possibly_a_starts.append(index_a)
        print(
            f'初次查找 = {len(indices)} min_distance = [{min_hash_distance}] 过滤后 = {len(possibly_a_starts)} min_distance = [{min_distance}]')
        return possibly_a_starts

    # def _2_step_find(self, feature_b):
    #     hist_b = BLUtils.calculate_histogram(feature_b)
    #     b_mean_hist = np.mean(hist_b)
    #     indices = GlobalHistList().binary_search_range(self.dst_path, b_mean_hist, 0.002)
    #     possibly_a_starts = []
    #     min_distance = 999
    #     for index_a in indices:
    #         feature_a = GlobalFeatureMap().feature_map[self.dst_path][index_a]
    #         distance = BLUtils.get_distance(feature_a, feature_b)
    #         if distance < 10:
    #             if distance < min_distance:
    #                 min_distance = distance
    #             possibly_a_starts.append(index_a)
    #     print(f'初次查找 = {len(indices)} 过滤后 = {len(possibly_a_starts)} min_distance = [{min_distance}]')
    #     return possibly_a_starts

    def find_possibly_start_point_gpu(self, image_2: PIL.Image, feature_iterator_a: FeatureIteratorCacheImpl):
        feature_iterator_a.set_image_gpu_output()
        result_arr = []

        min_distance = 999

        while True:
            try:
                image_1 = next(feature_iterator_a)
            except StopIteration:
                break

            distance = BLUtils.get_distance_gpu(image_1, image_2)

            if distance < 8:
                if distance < min_distance:
                    min_distance = distance
            result_arr.append(feature_iterator_a.get_current_index())

        feature_iterator_a.release()

        return result_arr

    def find_possibly_start_point_cpu_nomal(self, feature_b, feature_iterator_a: FeatureIteratorCacheImpl):
        result_arr = []

        min_distance = 999

        while True:
            try:
                feature_a = next(feature_iterator_a)
                feature_a = next(feature_iterator_a)
                feature_a = next(feature_iterator_a)
            except StopIteration:
                break

            distance = BLUtils.get_distance(feature_a, feature_b)

            if distance < 20:
                if distance < min_distance:
                    min_distance = distance
                result_arr.append(feature_iterator_a.get_current_index())

        feature_iterator_a.release()
        return result_arr

    def find_possibly_start_point_cpu(self, feature_b, feature_iterator_a):
        # tbar = tqdm(desc='寻找可能的A起点', unit='帧', total=feature_iterator_a.get_total_f_num())
        q = Queue()
        # 每个进程要负责的长度是多少
        pre_task = int(feature_iterator_a.get_total_f_num() / 5)
        process_list = []
        feature_map = GlobalFeatureMap().feature_map[self.dst_path]
        for i in range(5):  # 开启5个子进程执行fun1函数
            start = i * pre_task
            end = (i + 1) * pre_task - 1
            if i == self.finder_num - 1:
                end = feature_iterator_a.get_total_f_num()
            print(f'start,end = {start},{end}')

            Thread(target=self.find_possibly_a_start_interval,
                   args=(start, end, i, feature_map, feature_b,
                         q), name=f'{i}').start()  # 实例化进程对象
        feature_iterator_a.release()
        # for p in process_list:
        #     p.join()
        # process_list.clear()
        possibly_a_starts = []
        # # print(q.queue)
        # while not q.empty():
        #     possibly_a_starts.append(int(q.get()))
        count = 0
        while True:
            try:
                possibly_a_starts.append(int(q.get(timeout=1)))
            except Exception:
                break
        return possibly_a_starts

    def _get_video_creator(self):
        fps_a, (a_w, a_h) = VideoIteratorImpl(self.dst_path).get_video_info()
        print(f"A info {fps_a},({a_w},{a_h})")
        fps_b, (b_w, b_h) = VideoIteratorImpl(self.target_path).get_video_info()
        print(f"B info {fps_b},({b_w},{b_h})")

        # 使用高画质，算法原因只能使用低帧率
        output_path = self.output_path
        output_fps = fps_b

        size = (a_w, a_h) if a_w * a_h > b_w * b_h else (b_w, b_h)
        output_size = size

        print(f"output info {output_fps},{output_size}")

        return VideoCreatorImpl(output_path, output_fps, output_size)
