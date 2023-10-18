import os

import cv2
import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip

from src.heigher_service.impl.two_p_fast_dtw_orb_impl import TwoPFastDtwOrbImpl
from src.heigher_service.impl.two_p_fast_dtw_sift_impl import TwoPFastDtwSiftImpl
from src.heigher_service.runner_interface import RunnerI
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl
from src.service.video_iterator_interface import VideoIteratorPrefixI

import tensorflow as tf
# VGG16特征提取器的实现
import keras.applications as ka


class VideoAlignTaskMadajiasijiaImpl(RunnerI):
    def __init__(self, video_a_path, video_b_path):
        self.video_a_path = video_a_path
        self.video_b_path = video_b_path

    @staticmethod
    def _get_unique_filename(filename: str) -> str:
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filename):
            filename = f"{base}({counter}){ext}"
            counter += 1
        print(f"set output path: {filename}")
        return filename

    def run(self):
        a_iterator = VideoIteratorPrefixImpl(video_path=self.video_a_path)
        output_path = self._get_unique_filename(self.video_b_path)
        # model = ka.VGG16(include_top=False, weights='imagenet', pooling='avg')

        for i in range(360):
            try:
                frame = next(a_iterator)
            except StopIteration:
                raise Exception("不足360")

            if i == 115:
                # 对比两帧差异
                # 使用cv2.imread()函数读取图片
                image = cv2.imread('D:/code/python/pycharm/VidelAligner/static/img/img_115_.png')

                # cv2.imshow('frame A', image)
                # cv2.imshow('frame B', frame)
                # cv2.waitKey(1)

                distance = TwoPFastDtwOrbImpl.get_distance(image, frame)
                if distance < 70:
                    print("发现视频A存在固定开头，正在去除")
                    pass
                else:
                    a_iterator = None
                    print("视频A不存在固定开头")
                    break
                cv2.destroyAllWindows()

        runner: RunnerI = TwoPFastDtwSiftImpl(v_a_path=self.video_a_path,
                                              v_b_path=self.video_b_path,
                                              a_iterator=a_iterator,
                                              output_path=output_path,
                                              pool_size=300)

        runner.run()

        video1 = VideoFileClip(self.video_b_path)
        video2 = VideoFileClip(output_path)

        video1_audio = video1.audio
        final_video = video2.set_audio(video1_audio)

        final_video.write_videofile(self._get_unique_filename(output_path), codec='libx264', audio_codec='aac')
