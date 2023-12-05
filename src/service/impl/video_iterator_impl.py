import math
import random
from typing import List

import cv2
import numpy as np

from src.service.video_iterator_interface import VideoIteratorI, VideoIteratorPrefixI


class VideoIteratorImpl(VideoIteratorI):
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        # self.cap = cv2.cudacodec.createVideoReader(video_path)
        if not self.cap.isOpened():
            # print(f"文件对象未打开@[{video_path}]")
            raise Exception(f"文件对象未打开@[{video_path}]")
        # print(f"Open File [{video_path}]: True")

        self.video_path = video_path

        # 获取视频的帧率和尺寸
        self.fps_a = self.cap.get(cv2.CAP_PROP_FPS)
        self.width_a = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height_a = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 总帧数
        self.total_f_size = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        self.current_index = 0

        self.has_read = False  # 读取过

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self) -> np.ndarray:
        self.has_read = True

        if self.current_index < self.total_f_size:
            # ret, frame = self.cap.nextFrame()
            ret, frame = self.cap.read()
            if ret:
                self.current_index += 1
                return frame
            else:
                raise Exception(f"迭代错误{self.current_index}/{self.video_path}/{self.get_video_info()}")
        else:
            raise StopIteration

    def get_total_f_num(self) -> int:
        return self.total_f_size

    def get_video_info(self) -> (float, (int, int)):
        # 获取视频的帧率和尺寸
        return self.fps_a, (self.width_a, self.height_a)

    def get_current_index(self):
        if self.has_read:
            return self.current_index - 1
        return self.current_index

    def set_current_index(self, index):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        self.current_index = index

    def release(self):
        self.cap.release()


class SampleVideoIteratorImpl(VideoIteratorImpl):

    def __init__(self, video_path, sample_num):
        """
        通过概率来
        :param video_path:
        :param sample_num: 不管视频多长，从中取出<=total数量的帧
        """
        super().__init__(video_path)

        if not sample_num or sample_num <= 0:
            raise Exception(f'total is None or zero [sample_num = {sample_num}]')
        self.sample_num = sample_num

        # 计算抛弃每一帧的概率
        self.abandon_rate = int(self.sample_num / self.get_total_f_num() * 100) / 100

        self.sample_total_frame_size = int(self.total_f_size * (1 - self.abandon_rate))
        self.sample_iterator_counter = 0

        self.random_float = random

    def get_current_index(self):
        return self.sample_iterator_counter

    def get_total_f_num(self) -> int:
        return self.sample_total_frame_size

    def __next__(self) -> np.ndarray:

        if self.current_index < self.total_f_size:
            # 先进行判断
            if self.random_float.random() < self.abandon_rate:
                self.current_index += 1

            ret, frame = self.cap.read()
            if ret:
                self.current_index += 1
                self.sample_iterator_counter += 1
                return frame
            else:
                raise Exception(f"迭代错误{self.current_index}/{self.video_path}/{self.get_video_info()}")
        else:
            raise StopIteration


class VideoIteratorPrefixImpl(VideoIteratorPrefixI, VideoIteratorImpl):

    def __init__(self, video_path):

        # 设置一个新的prefix数组
        self.prefix_list = []

        super().__init__(video_path)

    def __next__(self) -> np.ndarray:
        if len(self.prefix_list) > 0:
            self.current_index += 1
            return self.prefix_list.pop(0)
        else:
            return super().__next__()

    def set_current_index(self, index):
        self.prefix_list.clear()
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        self.current_index = index

    def add_prefix(self, arr: List[np.ndarray]):

        if len(arr) == 0:
            print("你加入了一个长度为0的数组")

        if len(self.prefix_list) == 0:
            for frame in arr:
                self.prefix_list.append(frame)
        else:
            tmp_prefix = []
            for frame in arr:
                tmp_prefix.append(frame)
            for p_frame in self.prefix_list:
                tmp_prefix.append(p_frame)
            self.prefix_list = tmp_prefix

        self.current_index -= len(arr)

        print(f"added prefix{len(arr)}, len(pfx)=[{len(self.prefix_list)}] ", end='')

        if self.current_index < 0:
            print("这是因为加入了前置prefix数组,放心，不影响的。")


class VideoIteratorPrefixFpsImpl(VideoIteratorPrefixImpl):
    def __init__(self, video_path, target_fps):
        super().__init__(video_path=video_path)
        self.target_fps = target_fps
        if target_fps > self.fps_a:
            print('帧率超过原有帧率')
        self.sec = 0
        self.frame_rate = 1 / self.target_fps
        self.new_current_index = 0  # 这个表示在新帧率上，当前是第几帧
        self.new_total_frames = int(int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) * (1 / self.fps_a) / self.frame_rate)

    def get_total_f_num(self) -> int:
        return self.new_total_frames

    def get_video_info(self) -> (float, (int, int)):
        # 获取视频的帧率和尺寸
        return self.fps_a, (self.width_a, self.height_a)

    def get_current_index(self):
        return self.new_current_index

    def __next__(self) -> np.ndarray:
        if len(self.prefix_list) > 0:
            self.new_current_index += 1
            return self.prefix_list.pop(0)
        else:
            self.sec = round(self.sec, 2)
            self.sec = self.sec + self.frame_rate
            self.cap.set(cv2.CAP_PROP_POS_MSEC, self.sec * 1000)
            has_frames, image = self.cap.read()
            if has_frames:
                self.new_current_index += 1
                return image
            else:
                raise StopIteration


class VideoIteratorPrefixStepImpl(VideoIteratorPrefixImpl):

    def __init__(self, video_path, target_frames):
        super().__init__(video_path)
        # 获取原视频的总帧数和帧率
        original_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        original_fps = self.cap.get(cv2.CAP_PROP_FPS)

        # 计算步长值
        self.step = original_frames // target_frames
        # 计算新的帧率
        new_fps = original_fps / self.step
        self.fps_a = int(new_fps * 1000) / 1000
        self.total_f_size = int(target_frames)
        self.original_frames = original_frames
        # print(f"视频原帧总数与新总数为[{original_frames}]/[{self.total_f_size}]")
        # print(f"视频原帧帧率与新帧率为[{original_fps}]/[{new_fps}]")

        self.frame_number = 0
        # print(f'步长为{self.step}')

    def __next__(self) -> np.ndarray:
        if len(self.prefix_list) > 0:
            self.current_index += 1
            return self.prefix_list.pop(0)
        else:
            if self.frame_number < self.original_frames:
                ret, frame = self.cap.read()
                self.frame_number += 1
                if ret:
                    result = self.frame_number / self.step
                    # 如果当前帧号是步长值的整数倍，则写入输出视频
                    if math.isclose(result, round(result), rel_tol=1e-9):
                        self.current_index += 1
                        return frame
                    else:
                        # print('跳过帧=========================')
                        return self.__next__()
                else:
                    raise Exception(f"迭代错误{self.current_index}/{self.video_path}/{self.get_video_info()}")
            else:
                raise StopIteration


class VideoIteratorPrefixStepV2Impl(VideoIteratorImpl):
    def __init__(self, video_path, over_step_num):
        super().__init__(video_path)
        # 修改total frame 和current index
        self.original_frame_num = self.total_f_size
        self.total_f_size = int(self.total_f_size / over_step_num)
        self.real_frame_number = 0
        self.over_step = over_step_num

    def __next__(self) -> np.ndarray:

        if self.real_frame_number < self.original_frame_num:
            ret, frame = self.cap.read()
            if ret:
                self.real_frame_number += 1
                self.current_index += 1

                # 跳过step
                self.real_frame_number += self.over_step
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.real_frame_number)

                return frame
            else:
                raise Exception(f"迭代错误{self.current_index}/{self.video_path}/{self.get_video_info()}")
        else:
            raise StopIteration

# class VideoIteratorPrefixFpsImpl(VideoIteratorPrefixStepImpl):
#
#     def __init__(self, video_path, target_fps):
#         cap = cv2.VideoCapture(video_path)
#         if not cap.isOpened():
#             print(f"文件对象未打开@[{video_path}]")
#             raise Exception(f"文件对象未打开@[{video_path}]")
#         # print(f"Open File [{video_path}]: True")
#         original_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#         original_fps = cap.get(cv2.CAP_PROP_FPS)
#         target_frames = (target_fps / original_fps) * original_frames
#
#         super().__init__(video_path, target_frames)
