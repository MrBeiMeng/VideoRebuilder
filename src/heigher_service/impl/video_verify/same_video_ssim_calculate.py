import math

import cv2
import numpy as np
from tqdm import tqdm

from src.heigher_service.impl.two_p_fast_dtw_sift_impl import TwoPFastDtwSiftImpl
from src.heigher_service.runner_interface import RunnerI
from src.service.impl.video_iterator_impl import VideoIteratorImpl, VideoIteratorPrefixStepImpl, \
    VideoIteratorPrefixStepV2Impl


def get_feature(common_size, frame) -> np.ndarray:
    if frame.shape[1] > common_size[0] and frame.shape[0] > common_size[1]:
        # 计算视频B的长宽比
        aspect_ratio_b = common_size[0] / common_size[1]  # 宽度/高度

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
        resized_frame_a = cv2.resize(cropped_frame_a, (int(common_size[0] / 2), int(common_size[1] / 2)),
                                     interpolation=cv2.INTER_AREA)
        # resized_frame_b = cv2.resize(frame_b, (cropped_frame_a.shape[1], cropped_frame_a.shape[0]),
        #                              interpolation=cv2.INTER_AREA)

        resized_frame_a = cv2.cvtColor(resized_frame_a, cv2.COLOR_BGR2GRAY)
        # 归一化
        # normalized_image = cv2.normalize(resized_frame_a, None, 0, 255, cv2.NORM_MINMAX)
        # 直方图均衡化
        equalized_image_a = cv2.equalizeHist(resized_frame_a)
        blurred_frame_a = cv2.GaussianBlur(equalized_image_a, (51, 51), 0)

        # # 应用边缘卷积
        # edge_convolved_imageA = cv2.filter2D(resized_frame_a, -1, self.sobel_x)

        return blurred_frame_a
    else:
        frame = cv2.resize(frame,
                           (int(common_size[0] / 2), int(common_size[1] / 2)))  # 调整帧大小来降低计算量

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # # 归一化
        # # normalized_image = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX)
        # 直方图均衡化
        frame = cv2.equalizeHist(frame)
        frame = cv2.GaussianBlur(frame, (51, 51), 0)

        # frame = cv2.filter2D(frame, -1, self.sobel_x)

    return frame


class SameVideoSsimCalculate(RunnerI):

    def __init__(self, video_tuples):

        if video_tuples is None or len(video_tuples) == 0:
            raise Exception('video_tuples is None or len(video_tuples) == 0')
        # 注册迭代器

        self.video_tuples = video_tuples

        pass

    @staticmethod
    def _max(a, b):
        if a >= b:
            return a
        return b

    def run(self):

        frames_counts = []

        # 先进行比对
        for v_a_path, v_b_path in self.video_tuples:
            try:
                a_iterator = VideoIteratorImpl(v_a_path)
                b_iterator = VideoIteratorImpl(v_b_path)

                frames_counts.append(
                    (math.fabs(a_iterator.get_total_f_num() - b_iterator.get_total_f_num()), v_a_path, v_b_path))
            except Exception as e:
                # print(e)
                frames_counts.append((
                    999999, v_a_path, v_b_path))

        # 使用sorted函数和lambda表达式进行降序排序
        sorted_frames_counts = sorted(frames_counts, key=lambda x: x[0], reverse=True)

        for sorted_frames_count in sorted_frames_counts:
            print(sorted_frames_count)

        # 第二轮对比结果
        distance_counts = []  # 名字，总差异值，[]差异值列表

        # 先进行比对
        for _, v_a_path, v_b_path in sorted_frames_counts:
            a_iterator = VideoIteratorImpl(v_a_path)

            total_frame = a_iterator.get_total_f_num()

            sample_count = 50
            over_step = int(total_frame / sample_count)

            # over_step = 50
            try:
                print(f'开始分析任务：[{v_a_path}]')
                a_iterator = VideoIteratorPrefixStepV2Impl(v_a_path, over_step)
                b_iterator = VideoIteratorPrefixStepV2Impl(v_b_path, over_step)

                fps, (a_w, a_h) = a_iterator.get_video_info()
                fps, (b_w, b_h) = b_iterator.get_video_info()
                common_size = (a_w, a_h) if a_w < b_w and a_h < b_h else (b_w, b_h)

                # tbar = tqdm(total=sample_count, unit='帧')

                temp_distance_list = []

                # 进行比对，计算总和
                while True:
                    try:
                        frame_a = next(a_iterator)
                        frame_b = next(b_iterator)

                        feature_a = get_feature(common_size, frame_a)
                        feature_b = get_feature(common_size, frame_b)

                        ffa, ffb = TwoPFastDtwSiftImpl.cut_frame(feature_a, feature_b)
                        distance = TwoPFastDtwSiftImpl.get_distance(ffa, ffb)
                        temp_distance_list.append(distance)
                        # tbar.update(1)
                    except StopIteration:
                        distance_counts.append((v_a_path, sum(temp_distance_list), temp_distance_list))
                        print((v_a_path, sum(temp_distance_list), []))
                        # tbar.close()
                        break
                    except Exception as e:
                        # print(e)
                        distance_counts.append((v_a_path, 999999, temp_distance_list))
                        print((v_a_path, 999999, []))
                        break

            except Exception as e:
                print((v_a_path, 999999, []))

        # 使用sorted函数和lambda表达式进行降序排序
        sorted_distance_counts = sorted(distance_counts, key=lambda x: x[1], reverse=True)

        for sorted_distance_count in sorted_distance_counts:
            print(sorted_distance_count)
