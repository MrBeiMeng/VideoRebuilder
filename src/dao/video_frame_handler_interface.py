import abc
from typing import List

from src.common.models import VideoMetadata, VideoFrames
from src.dao.mysql_connection import SQLAlchemyConnection


class VideoFrameHandlerI(metaclass=abc.ABCMeta):

    # def __init__(self, db_connection: SQLAlchemyConnection = None):
    #     """初始化，传递SQLAlchemy连接实例"""
    #     self.db_connection = db_connection
    #
    #     if db_connection is None:
    #         self.db_connection = SQLAlchemyConnection().get_session()

    @abc.abstractmethod
    def insert_video_metadata(self, video_metadata: VideoMetadata):
        """插入视频元数据"""
        pass

    @abc.abstractmethod
    def get_video_metadata(self, video_id: int) -> VideoMetadata:
        """获取视频元数据"""
        pass

    @abc.abstractmethod
    def get_video_metadata_by_video_name(self, video_name: str) -> VideoMetadata:
        """获取视频元数据"""
        pass

    @abc.abstractmethod
    def insert_frame(self, frame: VideoFrames):
        """插入视频帧"""
        pass

    @abc.abstractmethod
    def get_frame(self, video_id: int, frame_index: int) -> VideoFrames:
        """获取视频帧"""
        pass

    @abc.abstractmethod
    def flush(self):
        """手动触发异步数据存储"""
        pass

    @abc.abstractmethod
    def batch_insert_frames(self, frames: List[VideoFrames]):
        """批量插入视频帧"""
        pass

    @abc.abstractmethod
    def update_video_metadata(self, updated_metadata: VideoMetadata):
        """更新视频元数据"""
        pass

    @abc.abstractmethod
    def delete_video(self, video_id: int):
        """删除视频及其帧数据"""
        pass

    @abc.abstractmethod
    def search_frames(self, video_id: int, start_index: int, end_index: int) -> List[VideoFrames]:
        """检索特定范围内的视频帧"""
        pass

    @abc.abstractmethod
    def batch_upsert_frames(self, frames: List[VideoFrames]):
        pass
