import abc

import numpy as np


class VideoIteratorIndexSearchI(metaclass=abc.ABCMeta):
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
    def load(self, video_path: str):
        pass

    @abc.abstractmethod
    def get_total_f_num(self) -> int:
        pass

    @abc.abstractmethod
    def get_by_index(self, index) -> np.ndarray:
        pass

    @abc.abstractmethod
    def reset_by_index(self, index):
        pass

    @abc.abstractmethod
    def get_video_info(self) -> (int, (int, int)):
        pass
