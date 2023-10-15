import abc
from typing import Tuple

import cv2
import numpy as np
from tqdm import tqdm

from src.common import utils, models
from src.dao.impl.video_frame_handler_impl import VideoFrameHandlerImpl
from src.dao.video_frame_handler_interface import VideoFrameHandlerI
from src.service.video_iterator_index_search_interface import VideoIteratorIndexSearchI


class VideoIteratorIndexSearchImpl(VideoIteratorIndexSearchI):
    def __init__(self, video_path: str, frame_handler: VideoFrameHandlerI = None):
        self.video_path = video_path
        self.frame_handler = frame_handler
        if frame_handler is None:
            self.frame_handler: VideoFrameHandlerI = VideoFrameHandlerImpl()

        self.current_index = 0  # Initialize the index to 0

        self.video_name = ""
        self.frame_rate = 0
        self.total_frame = 0
        self.resolution = (0, 0)
        self.duration = 0

        self.video_id = 0

        self.load(video_path)

    def __iter__(self):
        self.current_index = 0  # Reset the index on a new iteration
        return self

    def __next__(self) -> np.ndarray:
        total_frames = self.get_total_f_num()
        if self.current_index < total_frames:
            frame = self.get_by_index(self.current_index)
            self.current_index += 1
            return frame
        else:
            raise StopIteration

    def load(self, video_path: str):
        # 如果查询不到，就进行保存
        mate_data = self.frame_handler.get_video_metadata_by_video_name(utils.get_filename_without_ext(video_path))

        if mate_data is None:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise Exception("文件未打开")

            data = models.VideoMetadata()
            data.video_path = utils.get_filename(video_path)
            # data.video_id
            data.video_name = utils.get_filename_without_ext(video_path)
            data.frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
            data.total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            data.resolution_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            data.resolution_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            data.duration = data.total_frame / data.frame_rate

            self.frame_handler.insert_video_metadata(data)
            mate_data = self.frame_handler.get_video_metadata_by_video_name(utils.get_filename_without_ext(video_path))

            total_f = mate_data.total_frame

            frame_data_buffer = []

            for i in tqdm(range(total_f), desc="保存视频帧", unit="帧"):
                ret, frame = cap.read()
                if ret:
                    frame_data = models.VideoFrames()  # 降低初始化次数
                    frame_data.video_id = mate_data.video_id
                    frame_data.frame_index = i
                    frame_data.frame_data = frame
                    frame_data.timestamp = i / mate_data.frame_rate
                    frame_data.set_image_info(frame)
                    frame_data_buffer.append(frame_data)

                if len(frame_data_buffer) >= 10:
                    self.frame_handler.batch_insert_frames(frame_data_buffer)
                    frame_data_buffer.clear()

            self.frame_handler.batch_insert_frames(frame_data_buffer)
            frame_data_buffer.clear()

            cap.release()
        self.video_name = mate_data.video_name
        self.frame_rate = mate_data.frame_rate
        self.total_frame = mate_data.total_frame
        self.resolution = (mate_data.resolution_w, mate_data.resolution_h)
        self.duration = mate_data.duration
        self.video_id = mate_data.video_id

    def get_total_f_num(self) -> int:
        return self.total_frame

    def get_by_index(self, index: int) -> np.ndarray:

        vf = self.frame_handler.get_frame(self.video_id, index)

        # 方法1: 如果知道原始图像的形状和数据类型
        original_shape, original_dtype = vf.get_image_info()

        # 将二进制数据转换为 NumPy 数组
        restored_image = np.frombuffer(vf.frame_data, dtype=original_dtype).reshape(original_shape)

        # 重新整形数组以匹配图像的尺寸和颜色通道
        return restored_image

    def reset_by_index(self, index: int):
        self.current_index = index

    def get_video_info(self) -> Tuple[int, Tuple[int, int]]:
        return self.frame_rate, self.resolution
