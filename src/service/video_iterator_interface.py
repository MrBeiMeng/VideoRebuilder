import abc
from typing import List

import numpy as np


class VideoIteratorI(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, video_path):
        pass

    @abc.abstractmethod
    def __iter__(self):
        pass

    @abc.abstractmethod
    def __next__(self) -> np.ndarray:
        pass

    @abc.abstractmethod
    def get_total_f_num(self) -> int:
        pass

    @abc.abstractmethod
    def get_video_info(self) -> (float, (int, int)):
        pass


class VideoIteratorPrefixI(VideoIteratorI, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_prefix(self, arr: List[np.ndarray]):
        pass

    @abc.abstractmethod
    def get_current_index(self):
        pass
