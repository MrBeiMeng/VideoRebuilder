import abc

import numpy as np


class FeatureUtilsHigherI(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def get_a_feature(frame: np.ndarray, dsize_width: int = 270) -> np.ndarray:
        """
        这个函数负责将原有帧转为我们需要的feature 特征帧。
        !!! 这里发生了一个变化，我们是先去保存特征帧，每次对比时在调整大小去对比。！！！
        :param frame: 传入帧
        :param dsize_width:  返回的特征帧大小
        :return:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_b_feature(frame: np.ndarray) -> np.ndarray:
        """
        这个函数负责获取目标b的特征帧，目标B的特征帧因为水印的关系，所以要切割
        :param frame:
        :return:
        """

        pass

    @staticmethod
    @abc.abstractmethod
    def get_distance(frame_a: np.ndarray, frame_b: np.ndarray) -> float:
        """
        这个函数负责获取目标b的特征帧，目标B的特征帧因为水印的关系，所以要切割
        :param frame_a:
        :param frame_b:
        :return:
        """

        pass
