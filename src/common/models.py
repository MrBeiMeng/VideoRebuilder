import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Index, LargeBinary, func
from sqlalchemy.dialects.mysql import LONGBLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

from src.common import Config
from src.dao.mysql_connection import SQLAlchemyConnection

# 定义基础模型类
Base = declarative_base()


class DistanceList(Base):
    __tablename__ = 'distance_list'
    id = Column(Integer, primary_key=True, autoincrement=True)
    distance = Column(Integer, nullable=False)
    frame_index = Column(Integer, nullable=False)
    video_name = Column(String(255), nullable=False)
    i_time_stamp = Column(Integer, nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())


class VideoMetadata(Base):
    __tablename__ = 'video_metadata'
    video_id = Column(Integer, primary_key=True, autoincrement=True)
    video_name = Column(String(255), nullable=False)
    video_path = Column(String(255), nullable=False)
    frame_rate = Column(Integer, nullable=False)
    total_frame = Column(Integer, nullable=False)
    resolution_w = Column(Integer, nullable=False)
    resolution_h = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)  # 视频时长，以秒为单位
    creation_date = Column(DateTime, nullable=False, server_default=func.now())

    # frames = relationship('VideoFrames', back_populates='video')


class VideoFrames(Base):
    __tablename__ = 'video_frames'
    frame_id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer, nullable=False)
    frame_index = Column(Integer, nullable=False)
    timestamp = Column(Integer, nullable=False)  # 帧的时间戳，以毫秒为单位
    frame_data = Column(LONGBLOB, nullable=False)

    # 新增的列
    shape = Column(String(255), nullable=True)  # 存储图像的 shape
    dtype = Column(String(255), nullable=True)  # 存储图像的 dtype

    def set_image_info(self, image: np.ndarray):
        self.shape = str(image.shape)
        self.dtype = str(image.dtype)

    def get_image_info(self):
        # 将字符串转换回元组和NumPy dtype对象
        shape = tuple(map(int, self.shape.strip('()').split(',')))
        dtype = np.dtype(self.dtype)
        return shape, dtype

    # video = relationship('VideoMetadata', back_populates='frames')


if __name__ == '__main__':
    config = Config()
    db_config = {
        'host': config.get_nested('mysql.host'),
        'user': config.get_nested('mysql.user'),
        'port': config.get_nested('mysql.port'),
        'password': config.get_nested('mysql.password'),
        'database': config.get_nested('mysql.database')
    }
    # 初始化数据库连接和会话
    # 创建数据库引擎
    engine_url = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    engine = create_engine(engine_url, echo=True)  # echo=True 用于日志记录SQL查询，生产环境中可设为False
    # 创建会话
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    # 创建索引
    # Index('idx_video_frames_video_id', VideoFrames.video_id)
    # Index('idx_video_frames_frame_index', VideoFrames.frame_index)

    # 创建表结构
    Base.metadata.create_all(engine)
