import abc
from typing import List

import numpy as np


class VideoHandlerI(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, video_path):
        pass

    @abc.abstractmethod
    def get_feature_list(self) -> List[np.ndarray]:
        pass
