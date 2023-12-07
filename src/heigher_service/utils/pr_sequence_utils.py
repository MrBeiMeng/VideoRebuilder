import abc
import urllib.parse
import uuid

from src.heigher_service.utils.common import BLUtils
from src.service.impl.video_iterator_impl import VideoIteratorImpl

import cv2
from moviepy.editor import VideoFileClip
import wave
import contextlib


class PrFile:
    def __init__(self, file_path, name, fps, total_frames, width_height, audio_depth=16, audio_channel_count=2,
                 audio_sample_rate=44100):
        self.id = uuid.uuid4().__str__()
        self.file_path = ""
        self.name = ""
        self.path_url = ""
        self.fps = 0
        self.total_frames = 0
        self.width_height = (0, 0)
        self.audio_depth = 0
        self.audio_channel_count = 0
        self.audio_sample_rate = 0

    def generate_file(self, file_path):
        # 更新文件路径
        self.file_path = file_path
        self.name = file_path.split('/')[-1]

        # 使用 OpenCV 获取视频相关信息
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print("Error opening video file")
            return

        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width_height = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                             int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        # 使用 moviepy 获取音频相关信息
        clip = VideoFileClip(file_path)
        if clip.audio:
            self.audio_channel_count = clip.audio.nchannels
            self.audio_sample_rate = clip.audio.fps
            # 使用 wave 获取音频位深度
            self.audio_depth = 16  # 位深度 = 样本宽度 * 8

        # 注意：这里假设 file_path 是一个绝对路径
        file_url = urllib.parse.quote(file_path)
        self.path_url = f"file://localhost/{file_url}"

        # 释放资源
        cap.release()

        return self


class ClipItem:

    def __init__(self, name, total_frames, fps, start_end, in_out, p_in_out, file):
        self.id: str = uuid.uuid4().__str__()
        self.name: str = ''
        self.total_frames: int = 0
        self.fps: int = 0
        self.start_end: tuple[int, int] = (0, 0)
        self.in_out: tuple[int, int] = (0, 0)
        self.ppro_ticks_in_out: tuple[int, int] = (0, 0)
        self.file: PrFile = file

    @staticmethod
    def init(name, total_frames, fps, start_end, in_out, p_in_out, file_path, width_height):
        file_name = BLUtils.get_filename(file_path)
        file = PrFile(file_path=file_path, name=file_name, fps=fps, total_frames=total_frames,
                      width_height=width_height)

        return ClipItem(name=name, total_frames=total_frames, fps=fps, start_end=start_end, in_out=in_out,
                        p_in_out=p_in_out, file=file)

    def generate_clip_item_2(self, fps, total_frames, name):
        self.fps = fps
        self.total_frames = total_frames

        self.name = name

        return self

    def generate_clip_item(self, file_path: str):
        # iterator = VideoIteratorImpl(file_path)
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print("Error opening video file")
            return

        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        self.name = BLUtils.get_filename(file_path)

        # self.file = PrFile().generate_file(file_path)

        cap.release()

        return self

    def generate_clip_item_full(self, start_end, in_out, fps, total_frames, name):
        self.start_end = start_end
        self.in_out = in_out
        return self.generate_clip_item_2(fps, total_frames, name)
        # return None


class PrTrack:  # 轨道

    def __init__(self, name, clip_items):
        self.name: str = name
        self.clip_items: [] = clip_items

    def add_clip(self, clip_item: ClipItem):
        self.clip_items.append(clip_item)


class PrSequenceUtils:

    def __init__(self):
        self.uuid = uuid.uuid4().__str__()
        self.total_frames: int = 0  # duration
        # total_duration: int  # 总时长
        self.fps: int
        self.name: str
        self.video_data: list[PrTrack] = []
        self.video_format = ()  # (长，宽)
        self.audio_data: list[PrTrack] = []
        self.audio_format = None  # 深度，采样率

    def add_pr_track(self, pr_track_name):
        pr_track = PrTrack(pr_track_name, [])
        # 视频轨道和音频轨道应该同时添加
        self.video_data.append(pr_track)
        self.audio_data.append(pr_track)

    def add_clip_item(self, track_name, clip_item: ClipItem):
        # find

        not_found = True
        for index, pr_t in enumerate(self.video_data):
            if pr_t.name == track_name:
                not_found = False
                self.video_data[index].add_clip(clip_item)
                self.audio_data[index].add_clip(clip_item)

                # 信息更新

        if not_found:
            self.add_pr_track(track_name)

        for index, pr_t in enumerate(self.video_data):
            if pr_t.name == track_name:
                self.video_data[index].add_clip(clip_item)
                self.audio_data[index].add_clip(clip_item)

        # todo 更新自身相关信息
        if clip_item.total_frames > self.total_frames:
            self.total_frames = clip_item.total_frames

    def save_to_xml(self, xml_path=None):
        # 保存到 文件目录\

        pass


class PrSequenceUtilI(metaclass=abc.ABCMeta):

    def add_point(self, track_name, start_end, in_out):
        pass

    def save_to_xml(self, xml_path=None):
        """
        这个函数负责将类中的数据保存到 xml文件中
        :param xml_path:  为None 则保存到 BLUtils.get_unique_filename({当前的b_path 即可})
        :return:
        """
        pass
