import multiprocessing
from multiprocessing import Process

import cv2
import numpy as np

from src.heigher_service.utils.feature_utils import FeatureUtils
from src.service.impl.video_iterator_impl import VideoIteratorImpl


class BlProcessWorker(Process):  # 继承Process类
    def __init__(self, name, input_q: multiprocessing.Queue, output_q: multiprocessing.Queue):
        super().__init__(name=name)
        self.name = name
        self.input_q = input_q
        self.output_q = output_q
        self.scop_first_search_feature_map = {}
        self.scop_original_feature_map = {}

        print(f'进程 {name} 已创建')

    def _first_search_size(self, feature):
        return cv2.resize(feature, (8, 8), interpolation=cv2.INTER_AREA)

    def run(self):

        while True:
            work_name, data = self.input_q.get()
            if work_name == '_load_frames_from_video':
                self._load_frames_from_video(data)
            if work_name == '_first_search':
                self._first_search(data)
            if work_name == '_second_search':
                self._second_search(data)
            if work_name is None or work_name == '':
                break

        print(f'{self.name} 正在关闭')

    def _load_frames_from_video(self, data):
        video_path, start, end = data

        iterator = VideoIteratorImpl(video_path)
        iterator.set_current_index(start)
        print(f'{self.name} 开始读取视频')

        for i in range(end - start):
            # print('yes')
            current_index = iterator.get_current_index()
            try:
                frame = next(iterator)
            except StopIteration:
                break

            # 保存特征帧，这个特征帧将用来最终确定是否匹配
            feature: np.ndarray = FeatureUtils.get_a_feature(frame)
            self.scop_original_feature_map[current_index] = feature

            # 保存特征帧，这个特征帧将用来初次匹配
            first_search_feature = self._first_search_size(feature)
            self.scop_first_search_feature_map[current_index] = first_search_feature

            self.output_q.put((current_index, feature))

        iterator.release()
        print(f'{self.name} 完毕')

    def _first_search(self, feature_b: np.ndarray):
        # print(f'{self.name} 开始初次查找')
        first_feature_b = self._first_search_size(feature_b)

        for index, first_feature_a in self.scop_first_search_feature_map.items():
            distance = FeatureUtils.get_distance(first_feature_a, first_feature_b)
            # if distance < 3:
            self.output_q.put((index, distance))  # (索引，差异值)

        # print(f'{self.name} 查找完毕')

    def _second_search(self, data):
        feature_b, pre_search_scope = data
        for a_index in pre_search_scope:
            feature_a = self.scop_original_feature_map[a_index]
            distance = FeatureUtils.get_distance(feature_a, feature_b)
            self.output_q.put((a_index, distance))  # (索引，差异值)
