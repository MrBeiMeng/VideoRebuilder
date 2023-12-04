import abc

from src.entity.entitys import KeyFrame


class VideoKeyFramesI(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_key_frames(self) -> list[KeyFrame]:
        pass
