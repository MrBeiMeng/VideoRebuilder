from typing import List

import cv2
import numpy as np

from src.service.video_iterator_interface import VideoIteratorI, VideoIteratorPrefixI


class VideoIteratorImpl(VideoIteratorI):
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            print(f"文件对象未打开@[{video_path}]")
            raise Exception(f"文件对象未打开@[{video_path}]")
        print(f"Open File [{video_path}]: True")

        self.video_path = video_path

        # 获取视频的帧率和尺寸
        self.fps_a = self.cap.get(cv2.CAP_PROP_FPS)
        self.width_a = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height_a = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 总帧数
        self.total_f_size = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        self.current_index = 0

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self) -> np.ndarray:

        if self.current_index < self.total_f_size:
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

    def get_current_index(self):
        return self.current_index
