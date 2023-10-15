from typing import List

import cv2
import numpy as np
from tqdm import tqdm

from src.service.impl.video_iterator_impl import VideoIteratorImpl
from src.service.video_handler import VideoHandlerI
from src.service.video_iterator_interface import VideoIteratorI

import tensorflow as tf

# VGG16特征提取器的实现
import keras.applications as ka


class VideoHandlerImpl(VideoHandlerI):

    def __init__(self, video_path):
        self.video_path = video_path
        self.iterator: VideoIteratorI = VideoIteratorImpl(video_path)

    def get_feature_list(self) -> List[np.ndarray]:
        feature_list = []

        fps, (w, h) = self.iterator.get_video_info()
        print(fps, w, h)
        total_a_size = self.iterator.get_total_f_num()

        if total_a_size <= 0:
            raise Exception("迭代器失效，长度只有0")

        model = ka.VGG16(include_top=False, weights='imagenet', pooling='avg')
        for i in tqdm(range(total_a_size), desc=f"特征序列制作", unit="帧"):
            frame_a = next(self.iterator)

            frame = cv2.resize(frame_a, (int(w / 10), int(h / 10)))  # 调整帧大小以匹配VGG16的输入大小

            frame = tf.keras.applications.vgg16.preprocess_input(frame)  # 预处理帧

            image_4d = np.expand_dims(frame, axis=0)

            feature = model.predict(image_4d, verbose=0)  # verbose=0 关闭日志

            feature = feature.flatten()

            feature_list.append(feature)

            cv2.imshow("特征帧", frame)
            cv2.waitKey(1)

        return feature_list
