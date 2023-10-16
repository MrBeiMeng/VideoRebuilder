from typing import List
from unittest import TestCase

import cv2
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from tqdm import tqdm

from src.common import Config
from src.common.models import DistanceList
from src.service.impl.video_iterator_impl import VideoIteratorImpl
from src.service.video_iterator_interface import VideoIteratorI

import tensorflow as tf
# VGG16特征提取器的实现
import keras.applications as ka


class SameVideoDistanceVgg16:
    def __init__(self, v_a_path, v_b_path, draw_name=''):
        self.model = ka.VGG16(include_top=False, weights='imagenet', pooling='avg')
        self.draw_name = draw_name
        self.v_a_path = v_a_path
        self.v_b_path = v_b_path

    @staticmethod
    def get_feature(model, frame, w, h):
        frame = cv2.resize(frame, (int(w / 5), int(h / 5)))  # 调整帧大小以匹配VGG16的输入大小
        frame = tf.keras.applications.vgg16.preprocess_input(frame)  # 预处理帧
        cv2.imshow("feature", frame)
        cv2.waitKey(1)
        image_4d = np.expand_dims(frame, axis=0)
        feature = model.predict(image_4d, verbose=0)  # verbose=0 关闭日志
        return feature.flatten()

    @staticmethod
    def get_distance(frame_a: np.ndarray, frame_b: np.ndarray):
        return np.linalg.norm(frame_a - frame_b)  # Using numpy instead of tensorflow

    def generate_distance(self, frame_a, frame_b, w, h):
        feature_a = self.get_feature(self.model, frame_a, w, h)
        feature_b = self.get_feature(self.model, frame_b, w, h)

        distance = self.get_distance(feature_a, feature_b)
        return distance

    def test_generate_distance_list_with_same_videos(self):
        # 用来显示两个相同片段的不同分辨率下的distance情况
        video_a_iterator: VideoIteratorI = VideoIteratorImpl(
            video_path=self.v_a_path)
        video_b_iterator: VideoIteratorI = VideoIteratorImpl(
            self.v_b_path)
        range_time = video_b_iterator.get_total_f_num()
        pbar = tqdm(total=range_time, desc="视频对比差异值计算", unit="帧")

        frame_index_start = 0  # 每次加入数据库之后更新frame_index 起点

        # 对齐较小分辨率
        fps, (w, h) = video_b_iterator.get_video_info()
        print(fps, w, h)

        fps1, (w1, h1) = video_a_iterator.get_video_info()
        print(fps1, w1, h1)

        distance_list = []
        while True:
            try:
                frame_a = next(video_a_iterator)
                frame_b = next(video_b_iterator)
                pbar.update(1)
            except StopIteration:
                break

            distance = self.generate_distance(frame_a, frame_b, w, h)

            print(distance)

            distance_list.append(distance)

            if len(distance_list) >= 100:
                self.exec_many(distance_list, self.draw_name, fps=fps, frame_index=frame_index_start)
                distance_list.clear()
                frame_index_start += 100

        pbar.close()
        self.exec_many(distance_list, self.draw_name, fps=fps)

    @staticmethod
    def exec_many(distance_list: List, video_name: str, fps=24, frame_index=0):
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
            tmp.frame_index = frame_index + i
            tmp.video_name = video_name
            tmp.i_time_stamp = int((frame_index + i) * (1000.0 / fps))
            buffer.append(tmp)

        session.add_all(buffer)
        session.commit()

        session.close()
