import cv2
import numpy as np
from tqdm import tqdm

from src.heigher_service.runner_interface import RunnerI
from src.service.impl.video_creator_impl import VideoCreatorImpl
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl
from src.service.video_creator_interface import VideoCreatorI
from src.service.video_iterator_interface import VideoIteratorPrefixI

# VGG16特征提取器的实现
import keras.applications as ka

import tensorflow as tf


class TwoPointAlignImpl(RunnerI):

    def __init__(self, video_a_path, video_b_path):
        self.video_a_path = video_a_path
        self.video_b_path = video_b_path

        # 初始化 迭代器 对象
        self.a_iterator: VideoIteratorPrefixI = VideoIteratorPrefixImpl(video_a_path)
        self.b_iterator: VideoIteratorPrefixI = VideoIteratorPrefixImpl(video_b_path)
        self.model = ka.VGG16(include_top=False, weights='imagenet', pooling='avg')

        fps, (a_w, a_h) = self.a_iterator.get_video_info()
        fps, (b_w, b_h) = self.b_iterator.get_video_info()

        self.common_size = (a_w, a_h)
        if b_w < a_w and b_h < a_h:
            self.common_size = (b_w, b_h)

        self.pbar = tqdm(total=self.b_iterator.get_total_f_num(), desc="视频对比", unit="帧")
        self.creator: VideoCreatorI = self.get_video_creator()

    def get_video_creator(self) -> VideoCreatorI:
        fps_a, (a_w, a_h) = self.a_iterator.get_video_info()
        fps_b, (b_w, b_h) = self.b_iterator.get_video_info()

        higher_size = (a_w, a_h)
        higher_fps = fps_a
        # if b_w > a_w and b_h > a_h:
        #     higher_size = (b_w, b_h)
        #     higher_fps = fps_b

        # out_put_path, fps, video_size
        print(f"set output info: output_path {self.video_b_path},fps {higher_fps}, size {higher_size}")

        return VideoCreatorImpl(self.video_b_path, higher_fps, higher_size)

    def run(self):
        # 遍历双指针。
        # 如果相同则进行写操作
        # 否则加入到缓存数组，每次都进行对比

        frame_queue_a, frame_queue_b = [], []
        feature_queue_a, feature_queue_b = [], []

        while True:
            self.pbar.set_postfix_str(
                s=f"len queue_a,b {len(frame_queue_a)},{len(frame_queue_b)}\t video A {self.a_iterator.get_current_index()}/"
                  f"{self.a_iterator.get_total_f_num()}\t video B {self.b_iterator.get_current_index()}/"
                  f"{self.b_iterator.get_total_f_num()}")

            try:
                frame_a = next(self.a_iterator)
                frame_b = next(self.b_iterator)

                self.show_frames(frame_a, frame_b)
            except StopIteration:
                break

            feature_a = self.get_feature(frame_a)
            feature_b = self.get_feature(frame_b)

            self.show_features(feature_a, feature_b)

            if len(frame_queue_a) == 0 and len(frame_queue_b) == 0:
                distance = self.get_distance(feature_a, feature_b)

                print(distance)

                if self.check_value(distance):
                    self.pbar.update(1)

                    self.write_method(frame_a, frame_b)  # 进行写操作。这里拿到的就是对齐的两帧
                else:
                    frame_queue_a.append(frame_a)
                    frame_queue_b.append(frame_b)
                    feature_queue_a.append(feature_a)
                    feature_queue_b.append(feature_b)
            else:
                got_flag = False
                # 对比A与B积攒的
                for index in range(len(feature_queue_b)):
                    tmp_feature_b = feature_queue_b[index]
                    distance = self.get_distance(feature_a, tmp_feature_b)
                    if self.check_value(distance):
                        got_flag = True
                        # 重置了一下迭代器，让迭代器回到之前的某个点，至于为什么另一个加了一个点，因为这里左闭右开，为了对齐
                        frame_queue_b.append(frame_b)
                        self.b_iterator.add_prefix(frame_queue_b[index:])
                        self.a_iterator.add_prefix([frame_a])
                        frame_queue_a.clear()
                        frame_queue_b.clear()
                        feature_queue_a.clear()
                        feature_queue_b.clear()
                        break

                # 对比B与A积攒的
                for index in range(len(feature_queue_a)):
                    tmp_feature_a = feature_queue_a[index]
                    distance = self.get_distance(tmp_feature_a, feature_b)
                    if self.check_value(distance):
                        got_flag = True
                        frame_queue_a.append(frame_a)
                        self.a_iterator.add_prefix(frame_queue_a[index:])
                        self.b_iterator.add_prefix([frame_b])
                        frame_queue_a.clear()
                        frame_queue_b.clear()
                        feature_queue_a.clear()
                        feature_queue_b.clear()
                        break

                if not got_flag:
                    # 未对比成功
                    frame_queue_a.append(frame_a)
                    frame_queue_b.append(frame_b)

        self.done_method()

    @staticmethod
    def get_distance(feature_a, feature_b) -> int:
        return tf.norm(feature_a - feature_b).numpy()

    @staticmethod
    def check_value(num: int):
        return num <= 30

    def get_feature(self, frame) -> np.ndarray:
        frame = cv2.resize(frame, (int(self.common_size[0] / 10), int(self.common_size[1] / 10)))  # 调整帧大小以匹配VGG16的输入大小
        frame = tf.keras.applications.vgg16.preprocess_input(frame)  # 预处理帧
        image_4d = np.expand_dims(frame, axis=0)
        feature = self.model.predict(image_4d, verbose=0)  # verbose=0 关闭日志
        feature = feature.flatten()
        return feature

    def write_method(self, frame_a: np.ndarray, frame_b: np.ndarray):
        self.creator.write_frame(frame_a)

    def done_method(self):
        self.pbar.close()
        self.creator.release()
        print("结束")

    @staticmethod
    def show_features(feature_a, feature_b):
        ...

    @staticmethod
    def show_frames(frame_a, frame_b):
        cv2.imshow("Rolling A", frame_a)
        cv2.imshow("Rolling B", frame_b)
        cv2.waitKey(1)
