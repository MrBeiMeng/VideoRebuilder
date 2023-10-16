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


class TestSamePDistanceList(TestCase):
    @staticmethod
    def get_feature(model, frame, w, h):
        frame = cv2.resize(frame, (int(w / 5), int(h / 5)))  # 调整帧大小以匹配VGG16的输入大小
        frame = tf.keras.applications.vgg16.preprocess_input(frame)  # 预处理帧
        cv2.imshow("feature", frame)
        cv2.waitKey(1)
        image_4d = np.expand_dims(frame, axis=0)
        feature = model.predict(image_4d, verbose=0)  # verbose=0 关闭日志
        return feature.flatten()

    def test_generate_distance_list_with_same_videos(self):
        # 用来显示两个相同片段的不同分辨率下的distance情况
        video_a_iterator: VideoIteratorI = VideoIteratorImpl(
            'E:/xunleiyunpan/我爱爆米花1080p高码率L.mp4')
        video_b_iterator: VideoIteratorI = VideoIteratorImpl(
            'E:/xunleiyunpan/我爱爆米花30fps480p降分辨率.mp4')

        pbar = tqdm(total=video_b_iterator.get_total_f_num(), desc="视频对比差异值计算", unit="帧")

        # 对齐较小分辨率
        fps, (w, h) = video_b_iterator.get_video_info()
        print(fps, w, h)

        fps1, (w1, h1) = video_a_iterator.get_video_info()
        print(fps1, w1, h1)

        model = ka.VGG16(include_top=False, weights='imagenet', pooling='avg')
        distance_list = []
        while True:
            try:
                frame_a = next(video_a_iterator)
                frame_b = next(video_b_iterator)
                pbar.update(1)
            except StopIteration:
                break

            feature_a = self.get_feature(model, frame_a, w, h)
            feature_b = self.get_feature(model, frame_b, w, h)

            distance = np.linalg.norm(feature_a - feature_b)  # Using numpy instead of tensorflow
            # distance = tf.norm(feature_a - feature_b).numpy()

            print(distance)

            distance_list.append(distance)

        pbar.close()
        self.exec_many(distance_list, "我爱爆米花不同分辨率同帧差异值@np.linalg", fps=30)

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
