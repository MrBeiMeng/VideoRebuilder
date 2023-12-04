import copy

import cv2
from tqdm import tqdm

from src.entity.entitys import KeyFrame
from src.heigher_service.impl.two_p_fast_dtw_orb_impl import TwoPFastDtwOrbImpl
from src.heigher_service.utils.common import BLUtils
from src.service.impl.video_iterator_impl import VideoIteratorImpl
from src.service.video_iterator_interface import VideoIteratorI
from src.service.video_key_frames_interface import VideoKeyFramesI


class VideoKeyFramesImpl(VideoKeyFramesI):

    def __init__(self, video_path, common_size, crop_info_path):
        self.video_path = video_path
        self.common_size = common_size
        self.crop_info_path = crop_info_path
        # 生成迭代器，

        self.video_iterator: VideoIteratorI = VideoIteratorImpl(self.video_path)

    def _get_cropped_feature(self, frame):
        return BLUtils.get_cropped_feature(frame=frame, common_size=self.common_size,
                                           crop_info_path=self.crop_info_path)

    def get_key_frames(self) -> list[KeyFrame]:
        result: list[KeyFrame] = []

        # 遍历视频帧，在一定范围内取一帧关键帧
        # 方案一：取开头第一帧
        first_frame = next(self.video_iterator)

        key_feature = self._get_cropped_feature(first_frame)
        key_frame = KeyFrame(key_feature, self.video_iterator.get_current_index(),
                             self.video_iterator.get_current_index() + 1)

        tbar = tqdm(desc='正在获取关键帧', unit='帧', total=self.video_iterator.get_total_f_num())

        while True:
            try:
                frame = next(self.video_iterator)
                feature = self._get_cropped_feature(frame)
                # cv2.imshow('key_feature', key_frame.get_frame())
                # cv2.imshow('feature', feature)
                # cv2.waitKey(0)
            except StopIteration:
                break

            # 比对两个feature
            distance = BLUtils.get_distance(key_frame.get_frame(), feature)
            # distance = TwoPFastDtwOrbImpl.get_distance(key_frame.get_frame(), feature)
            tbar.update(1)
            tbar.set_postfix_str(
                f'd={int(distance)} got key feature {len(result)}')

            # 如果distance 大于某个范围，则代表不合理
            if distance < 5:
                key_frame.set_end_index(key_frame.get_end_index() + 1)
            else:
                result.append(copy.copy(key_frame))

                key_frame = KeyFrame(feature, self.video_iterator.get_current_index(),
                                     self.video_iterator.get_current_index() + 1)

        tbar.update(1)
        result.append(copy.copy(key_frame))

        tbar.close()

        self.video_iterator.release()

        return result

    def done(self):
        self.video_iterator.release()
        del self
