import abc

import numpy as np


class FrameIndexFounderI(metaclass=abc.ABCMeta):
    """
    这个类负责从给定的视频或图片序列中找出与指定图片最相近的索引集合
    """

    @abc.abstractmethod
    def get_best_math_a_index_list(self, feature_b: np.ndarray, expect_num: int = 0, expect_distance: float = 0.0) -> \
            list[int]:
        """
        获取到和目标特征B最接近的索引集合
        实现： 通过多进程进行寻找
        :param feature_b:
        :param expect_num: 期待的数量 ，若指定，则选择期待值以下的
        :param expect_distance: 期待的差异值，若指定，则选择期待值以下的
        :return:
        """
        pass
