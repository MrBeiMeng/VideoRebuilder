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


class GlobalAvgHashMap:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.avg_hash_map = {}  # key, {index,avg_hash}
            print("inited model")
        return cls._instance

    def add_feature(self, path, index, feature):
        if path in self.avg_hash_map and index in self.avg_hash_map[path]:
            return

        if path not in self.avg_hash_map:
            self.avg_hash_map[path] = {}
        avg_hash = BLUtils.average_hash(feature)

        self.avg_hash_map[path][index] = avg_hash


class GlobalHistList:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.hist_mean_tuple = {}  # key, [(hist_mean,index)]
            print("inited model")
        return cls._instance

    def sort(self, path=None, total=None):
        for key, value in self.hist_mean_tuple.items():
            # 将每个直方图的平均值与其索引配对
            frame_hist_and_index: List[tuple[float, int]] = value

            # 排序：这里以直方图的平均值作为排序依据
            frame_hist_and_index.sort(key=lambda x: x[0])

            # 提取排序后的帧和它们的索引
            self.hist_mean_tuple[key] = [(hist, index) for hist, index in frame_hist_and_index]

        if path is not None and total is not None:
            print(f'path hist 总计[{len(self.hist_mean_tuple[path])}] 丢失[{total - len(self.hist_mean_tuple[path])}]')

    def binary_search_range(self, path, target_hist_mean, tolerance):

        sorted_frames = self.hist_mean_tuple[path]

        left, right = 0, len(sorted_frames) - 1
        result_indices = []

        while left <= right:
            mid = (left + right) // 2
            mid_mean_hist = sorted_frames[mid][0]  # 获取中间帧的直方图平均值

            # 检查是否在容差范围内
            if abs(mid_mean_hist - target_hist_mean) <= tolerance:
                # 向左和向右扩展，寻找所有符合条件的帧
                l, r = mid - 1, mid + 1
                result_indices.append(sorted_frames[mid][1])  # 添加中间帧的索引

                # 向左扩展
                while l >= 0 and abs(sorted_frames[l][0] - target_hist_mean) <= tolerance:
                    result_indices.append(sorted_frames[l][1])
                    l -= 1

                # 向右扩展
                while r < len(sorted_frames) and abs(sorted_frames[r][0] - target_hist_mean) <= tolerance:
                    result_indices.append(sorted_frames[r][1])
                    r += 1

                break  # 跳出循环
            elif mid_mean_hist < target_hist_mean:
                left = mid + 1
            else:
                right = mid - 1

        return result_indices


class GlobalImageMap:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.image_map = {}
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

        self.output_gpu = False

        # print(f'缓存长度 [{len(GlobalFeatureMap().feature_map[video_path].values())}]')

    def set_current_index(self, index):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        self.current_index = index

    def set_image_gpu_output(self):
        self.output_gpu = True

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

            if not self.output_gpu:
                feature = GlobalFeatureMap().feature_map[self.video_path][self.current_index]
                self.current_index += 1
                return feature

            image = GlobalImageMap().image_map[self.video_path][self.current_index]
            self.current_index += 1
            return image
        else:
            raise StopIteration

    def release(self):
        # pass
        self.cap.release()

    def do_release(self):
        GlobalFeatureMap().feature_map.pop(self.video_path)
        # self.cap.release()
