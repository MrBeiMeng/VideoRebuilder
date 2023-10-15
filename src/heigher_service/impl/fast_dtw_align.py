from typing import List

import numpy as np
from fastdtw import fastdtw
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from tqdm import tqdm

from src.common import Config
from src.common.models import DistanceList
from src.heigher_service.runner_interface import RunnerI
from src.service.impl.video_handler_impl import VideoHandlerImpl
from src.service.video_handler import VideoHandlerI

import tensorflow as tf


class FastDtwAlign(RunnerI):

    def __init__(self, video_a_path, video_b_path):
        # 初始化VideoHandler 对象
        self.a_handler: VideoHandlerI = VideoHandlerImpl(video_a_path)
        self.b_handler: VideoHandlerI = VideoHandlerImpl(video_b_path)

    @staticmethod
    def get_distance_list_by_video_name(video_name: str) -> List:
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
        session_factory = sessionmaker(bind=engine)
        session = scoped_session(session_factory)

        result: List[DistanceList] = session.query(DistanceList).filter(DistanceList.video_name == video_name).all()

        distance_list = []

        for e in result:
            distance_list.append(e.distance)
        return distance_list

    @staticmethod
    def exec_many(distance_list: List, video_name: str, fps=24):
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
        session_factory = sessionmaker(bind=engine)
        session = scoped_session(session_factory)

        buffer = []

        for i in tqdm(range(len(distance_list)), desc="结果整理", unit="distance"):
            tmp = DistanceList()
            tmp.distance = distance_list[i]
            tmp.frame_index = i
            tmp.video_name = video_name
            tmp.i_time_stamp = (i / fps) * 1000
            buffer.append(tmp)

        session.add_all(buffer)
        session.commit()

        session.close()

    @staticmethod
    def euclidean(feature_a, feature_b):
        return tf.norm(feature_a - feature_b).numpy()

    def run(self):
        feature_a_list = self.a_handler.get_feature_list()
        feature_b_list = self.b_handler.get_feature_list()

        # len feature_a_list must equal with len a

        distance_list_a = self.get_distance_list_by_video_name("我爱大毛央视原版")
        distance_list_b = self.get_distance_list_by_video_name("我爱大毛央视片段")

        if (len(feature_a_list) != len(distance_list_a)) or (len(feature_b_list) != len(distance_list_b)):
            raise Exception(
                f"长度不相等{len(feature_a_list)}{len(distance_list_a)}{len(feature_b_list)}{len(distance_list_b)}")

        # 创建两个简单的一维序列
        x = np.array(distance_list_a, dtype=float)
        y = np.array(distance_list_b, dtype=float)

        print("开始进行dtw对齐")

        # 使用 fastdtw 函数计算 DTW 对齐
        distance, path = fastdtw(feature_a_list, feature_b_list, dist=self.euclidean)

        print("dtw 对齐结束")

        # 初始化两个空的新序列
        new_seq_x = []
        new_seq_y = []

        # 遍历 DTW 路径，生成新的序列
        for i, j in path:
            new_seq_x.append(x[i])
            new_seq_y.append(y[j])

        self.exec_many(new_seq_x, "我爱大毛完整对齐后v2", fps=24)
        self.exec_many(new_seq_y, "我爱大毛片段对齐后v2", fps=24)
