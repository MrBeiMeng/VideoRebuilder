import abc

import numpy as np


class VideoCreatorI(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, filename: str, fps=30, video_size=(1920, 1080)):
        # 通过名字自动创建对应文件，如果文件已经存在，则以“原名字(序号).后缀”的格式创建新文件
        pass

    @abc.abstractmethod
    def write_frame(self, frame: np.ndarray):
        # 将帧写入到视频文件中去
        pass

    @abc.abstractmethod
    def release(self):
        # 释放视频写入对象
        pass
