import os

import cv2
import numpy as np

from src.service.video_creator_interface import VideoCreatorI


class VideoCreatorImpl(VideoCreatorI):
    def __init__(self, filename: str, fps=30, frame_size=(1920, 1080)):
        super().__init__(filename)
        self.filename = self._get_unique_filename(filename)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.frame_size = frame_size  # 定义视频的帧尺寸
        self.out = cv2.VideoWriter(self.filename, self.fourcc, fps, frame_size)

    @staticmethod
    def _get_unique_filename(filename: str) -> str:
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filename):
            filename = f"{base}({counter}){ext}"
            counter += 1
        print(f"set output path: {filename}")
        return filename

    def write_frame(self, frame: np.ndarray):
        # 检查帧的尺寸是否匹配
        if (frame.shape[1], frame.shape[0]) != self.frame_size:
            raise ValueError(
                f"Frame size mismatch: current ({frame.shape[1], frame.shape[0]}), expected {self.frame_size}")
        self.out.write(frame)

    def release(self):
        self.out.release()
