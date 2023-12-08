import abc

import numpy as np


class FeatureUtilsI(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def get_intersection_part(frame: np.ndarray) -> np.ndarray:
        """
        这个函数负责从指定frame中获取 两帧相交的部分
        :param frame:
        :return:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_cropped(frame_a: np.ndarray) -> np.ndarray: ...
