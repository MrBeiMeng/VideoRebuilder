import math
import random
from typing import List

import cv2
import numpy as np

from src.heigher_service.utils.common import BLUtils
from src.service.impl.video_iterator_impl import VideoIteratorImpl
from src.service.video_iterator_interface import FeatureIteratorI


# from src.service.video_iterator_interface import VideoIteratorI, VideoIteratorPrefixI


class GlobalFeatureMap:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.feature_map = {}
            print("inited model")
        return cls._instance

    # def get_feature_map(self):
    #     return self.feature_map


class FeatureIteratorCacheImpl(FeatureIteratorI, VideoIteratorImpl):
    # _video_path_list = []
    # _instance_list = []
    #
    # def __new__(cls, video_path, common_size, crop_info_path):
    #     if video_path not in cls._video_path_list:
    #         _instance = super().__new__(cls)
    #
    #         cls._video_path_list.append(video_path)
    #         cls._instance_list.append(_instance)
    #
    #         print(f"inited 特征迭代器:[{video_path}]")
    #
    #     return cls._instance_list[cls._video_path_list.index(video_path)]

    def __init__(self, video_path, common_size, crop_info_path):
        super().__init__(video_path=video_path)
        self.common_size = common_size
        self.crop_info_path = crop_info_path

        if video_path not in GlobalFeatureMap().feature_map:
            GlobalFeatureMap().feature_map[video_path] = {}

        # print(f'缓存长度 [{len(GlobalFeatureMap().feature_map[video_path].values())}]')

    def set_current_index(self, index):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        self.current_index = index

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self) -> np.ndarray:
        self.has_read = True

        if self.current_index < self.total_f_size:

            if self.current_index not in GlobalFeatureMap().feature_map[self.video_path]:
                ret, frame = self.cap.read()
                # print('读取帧')
                if ret:
                    feature = BLUtils.get_cropped_feature(frame=frame, common_size=self.common_size,
                                                          crop_info_path=self.crop_info_path)
                    GlobalFeatureMap().feature_map[self.video_path][self.current_index] = feature
                else:
                    raise Exception(f"迭代错误{self.current_index}/{self.video_path}/{self.get_video_info()}")

            feature = GlobalFeatureMap().feature_map[self.video_path][self.current_index]
            self.current_index += 1
            return feature
        else:
            raise StopIteration

    def release(self):
        # pass
        self.cap.release()

    def do_release(self):
        GlobalFeatureMap().feature_map.pop(self.video_path)
        # self.cap.release()
