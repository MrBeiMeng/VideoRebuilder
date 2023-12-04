import cv2
from tqdm import tqdm

from src.entity.entitys import KeyFrame
from src.heigher_service.impl.two_p_fast_dtw_orb_impl import TwoPFastDtwOrbImpl
from src.heigher_service.impl.two_p_fast_dtw_sift_impl import TwoPFastDtwSiftImpl
from src.heigher_service.runner_interface import RunnerI
from src.heigher_service.utils.common import BLUtils
from src.heigher_service.utils.common_sequence import CSUtils
from src.heigher_service.utils.frame_cut_util import FrameCutUtilXiGua
from src.service.impl.video_creator_impl import VideoCreatorImpl
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl, VideoIteratorImpl
from src.service.impl.video_key_frames_impl import VideoKeyFramesImpl
from src.service.video_iterator_interface import VideoIteratorI
from src.service.video_key_frames_interface import VideoKeyFramesI


class VideoRebuildCommonSequenceImpl(RunnerI):

    def __init__(self, dst_path: str, target_path: str, output_path=None):
        self.dst_path = dst_path
        self.target_path = target_path

        if output_path is not None:
            self.output_path = output_path
        else:
            self.output_path = BLUtils.get_unique_filename(self.target_path)

        self.crop_info_path = 'static/crop_info_xi_gua.json'

        # self.video_creator = self._get_video_creator()

    def run(self):

        # 获取两个视频的最小公共 size
        common_size = BLUtils.get_common_size(self.dst_path, self.target_path)
        print(f'计算common_size = [{common_size}]')

        max_map = self._get_max_map(common_size)

        # max_map 中保存的是匹配的最长序列
        max_arr = self._get_max_arr(max_map)

        # 展示一下

        iterator_a, iterator_b = VideoIteratorImpl(self.dst_path), VideoIteratorImpl(self.target_path)

        count = 1
        for items in max_arr:
            start_a, start_b, equal_len, b, distance = tuple(items)
            if equal_len < 2:
                continue
            iterator_a.set_current_index(start_a)
            iterator_b.set_current_index(start_b)

            print(f'第{count}段，此段的distance=[{distance}/{equal_len}={int(distance / equal_len)}]')
            count += 1

            for i in range(equal_len):
                frame_a, frame_b = next(iterator_a), next(iterator_b)
                temp_distance = BLUtils.get_distance(
                    BLUtils.get_cropped_feature(frame_a, common_size, self.crop_info_path),
                    BLUtils.get_cropped_feature(frame_b, common_size, self.crop_info_path))
                print(f'准确distance={temp_distance}')
                cv2.imshow('generated frame', frame_a)
                cv2.imshow('original frame', frame_b)
                cv2.waitKey(0)

    def _get_max_arr(self, max_map):
        iterator_b = VideoIteratorImpl(self.target_path)
        segments = []
        for val in max_map.values():
            for items in val:
                segments.append(items)
        max_arr = CSUtils.cover_interval(segments, (0, iterator_b.get_total_f_num()))
        got_frames = 0
        for items in max_arr:
            start_a, start_b, equal_len, b, distance = tuple(items)
            got_frames += equal_len
        print(f'过滤掉特别不合理的，剩余[{len(max_arr)}]条 丢失[{iterator_b.get_total_f_num() - got_frames}]帧')
        iterator_b.release()
        return max_arr

    def _get_max_map(self, common_size):
        # 生成两个视频的迭代器，计算匹配的公共区间
        iterator_a, iterator_b = VideoIteratorImpl(self.dst_path), VideoIteratorImpl(self.target_path)

        def is_equal(distance: int) -> bool:
            return distance <= 10

        max_map = CSUtils.find_all_common_sequence(iterator_a=iterator_a, iterator_b=iterator_b,
                                                   common_size=common_size,
                                                   is_equal=is_equal, crop_info_path=self.crop_info_path)

        iterator_a.release()
        iterator_b.release()
        return max_map

    def _get_video_creator(self):
        fps_a, (a_w, a_h) = VideoIteratorImpl(self.dst_path).get_video_info()
        print(f"A info {fps_a},({a_w},{a_h})")
        fps_b, (b_w, b_h) = VideoIteratorImpl(self.target_path).get_video_info()
        print(f"B info {fps_b},({b_w},{b_h})")

        # 使用高画质，算法原因只能使用低帧率
        output_path = self.output_path
        output_fps = fps_b

        size = (a_w, a_h) if a_w * a_h > b_w * b_h else (b_w, b_h)
        output_size = size

        print(f"output info {output_fps},{output_size}")

        return VideoCreatorImpl(output_path, output_fps, output_size)
