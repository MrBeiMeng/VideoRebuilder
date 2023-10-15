from typing import List
from sqlalchemy import create_engine, insert

from src.common.models import VideoMetadata, VideoFrames
from src.dao.mysql_connection import SQLAlchemyConnection
from src.dao.video_frame_handler_interface import VideoFrameHandlerI


class VideoFrameHandlerImpl(VideoFrameHandlerI):

    def get_video_metadata_by_video_name(self, video_name: str) -> VideoMetadata:
        # 创建一个查询来查找具有指定video_name的VideoMetadata实例
        query = self.session.query(VideoMetadata).filter(VideoMetadata.video_name == video_name)
        # 执行查询并返回第一个结果（如果存在）
        # 如果没有找到匹配的结果，first()将返回None
        return query.first()

    def __init__(self, db_connection: SQLAlchemyConnection = None):
        """初始化，传递SQLAlchemy连接实例"""
        # super().__init__(db_connection)
        self.db_connection = db_connection

        if db_connection is None:
            self.db_connection = SQLAlchemyConnection()

        self.session = self.db_connection.get_session()

    def insert_video_metadata(self, video_metadata: VideoMetadata):
        self.session.add(video_metadata)
        self.session.commit()

    def get_video_metadata(self, video_id: int) -> VideoMetadata:
        return self.session.query(VideoMetadata).filter(VideoMetadata.video_id == video_id).one()

    def insert_frame(self, frame: VideoFrames):
        self.session.add(frame)
        self.session.commit()

    def get_frame(self, video_id: int, frame_index: int) -> VideoFrames:
        return self.session.query(VideoFrames).filter(
            VideoFrames.video_id == video_id,
            VideoFrames.frame_index == frame_index
        ).one()

    def flush(self):
        self.session.flush()  # Assuming asynchronous operations, adjust as necessary

    def batch_upsert_frames(self, frames: List[VideoFrames]):
        for frame in frames:
            stmt = (
                insert(VideoFrames).
                values(
                    video_id=frame.video_id,
                    frame_index=frame.frame_index,
                    timestamp=frame.timestamp,
                    frame_data=frame.frame_data
                ).
                on_duplicate_key_update(
                    video_id=frame.video_id,
                    frame_index=frame.frame_index,
                    timestamp=frame.timestamp,
                    frame_data=frame.frame_data
                )
            )
            self.session.execute(stmt)
        self.session.commit()

    def batch_insert_frames(self, frames: List[VideoFrames]):
        self.session.add_all(frames)
        self.session.commit()

    def update_video_metadata(self, updated_metadata: VideoMetadata):
        existing_metadata = self.get_video_metadata(updated_metadata.video_id)
        for attr, value in updated_metadata.__dict__.items():
            setattr(existing_metadata, attr, value)
        self.session.commit()

    def delete_video(self, video_id: int):
        video_metadata = self.get_video_metadata(video_id)
        self.session.delete(video_metadata)
        self.session.query(VideoFrames).filter(VideoFrames.video_id == video_id).delete()
        self.session.commit()

    def search_frames(self, video_id: int, start_index: int, end_index: int) -> List[VideoFrames]:
        return self.session.query(VideoFrames).filter(
            VideoFrames.video_id == video_id,
            VideoFrames.frame_index.between(start_index, end_index)
        ).all()
