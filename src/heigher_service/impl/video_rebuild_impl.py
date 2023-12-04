import cv2
from tqdm import tqdm

from src.entity.entitys import KeyFrame
from src.heigher_service.impl.two_p_fast_dtw_orb_impl import TwoPFastDtwOrbImpl
from src.heigher_service.impl.two_p_fast_dtw_sift_impl import TwoPFastDtwSiftImpl
from src.heigher_service.runner_interface import RunnerI
from src.heigher_service.utils.common import BLUtils
from src.heigher_service.utils.frame_cut_util import FrameCutUtilXiGua
from src.service.impl.video_creator_impl import VideoCreatorImpl
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl, VideoIteratorImpl
from src.service.impl.video_key_frames_impl import VideoKeyFramesImpl
from src.service.video_iterator_interface import VideoIteratorI
from src.service.video_key_frames_interface import VideoKeyFramesI


class VideoRebuildImpl(RunnerI):

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

        # 比对两个视频
        # 先计算视频A的画像（即特征帧序列）（每一帧画像应该保存一个对应的索引区间。）
        # 读取视频B进行画像比对，这一步是为了大致的确定比对的范围。
        #    方案一：计算视频B的画像，在A画像序列中进行寻找（取最接近的）
        # 精细比对

        # 获取两个视频的最小公共 size
        common_size = BLUtils.get_common_size(self.dst_path, self.target_path)
        print(f'计算common_size = [{common_size}]')

        video_a_key_frames = self._get_key_frames(common_size, self.dst_path)
        # video_b_key_frames = self._get_key_frames(common_size, self.target_path)

        # 遍历b序列，寻找
        b_iterator: VideoIteratorI = VideoIteratorImpl(self.target_path)

        while True:
            try:
                b_f = next(b_iterator)
                b_f = BLUtils.get_cropped_feature(common_size=common_size, crop_info_path=self.crop_info_path,frame=b_f)
            except StopIteration:
                break

            min_distance = 101
            a_index = -1

            tbar = tqdm(total=len(video_a_key_frames))

            for a_key_frame in video_a_key_frames:
                distance = TwoPFastDtwOrbImpl.get_distance(b_f, a_key_frame.get_frame())
                tbar.update(1)
                if distance < min_distance:
                    min_distance = distance
                    a_index = a_key_frame.get_start_index()
                    tbar.set_postfix_str(f'min_distance = {min_distance}')

            tbar.close()

        # ab_key_point = self._get_key_point(video_a_key_frames=video_a_key_frames,
        #                                    video_b_key_frames=video_b_key_frames)
        # 用来保存对应的AB关键帧的起止点 {min_distance,(as,ae),(bs,be)}

        # 之后我们便可以开始精细比对了
        # for item in ab_key_point:
        #     temp_a_iterator = self._get_temp_iterator_by_start_end(item[1], self.dst_path)
        #     temp_b_iterator = self._get_temp_iterator_by_start_end(item[2], self.target_path)
        #
        #     BLUtils.show_video(temp_a_iterator, wait=True)
        #     BLUtils.show_video(temp_b_iterator, wait=True)

        # runner: RunnerI = TwoPFastDtwSiftImpl(
        #     v_a_path='',
        #     v_b_path='',
        #     a_iterator=temp_a_iterator,
        #     b_iterator=temp_b_iterator,
        #     video_creator=self.video_creator,
        #     pool_size=200,
        #     crop_info=FrameCutUtilXiGua(self.crop_info_path).crop_info)
        #
        # runner.run()

    @staticmethod
    def _get_temp_iterator_by_start_end(start_end, path):
        temp_a_iterator = VideoIteratorPrefixImpl(path)
        temp_a_iterator.set_current_index(start_end[0])
        temp_a_iterator.total_f_size = temp_a_iterator.current_index + (start_end[1] - start_end[0])
        return temp_a_iterator

    @staticmethod
    def _get_key_point(video_a_key_frames, video_b_key_frames):
        tbar = tqdm(total=len(video_b_key_frames), desc='对齐关键帧', unit='帧')

        ab_key_point = []
        # 对两个序列进行比对
        for b_key_frame in video_b_key_frames:
            min_distance = 100
            a_interval = (0, 0)
            for a_key_frame in video_a_key_frames:
                distance = BLUtils.get_distance(b_key_frame.get_frame(), a_key_frame.get_frame())
                if distance < min_distance:
                    min_distance = distance
                    a_interval = a_key_frame.get_start_index(), a_key_frame.get_end_index()

            # 最终的到最接近的A关键帧的对应的起点和终点
            ab_key_point.append(
                (
                    min_distance,
                    a_interval,
                    (b_key_frame.get_start_index(), b_key_frame.get_end_index())
                )
            )
            tbar.update(1)
            tbar.set_postfix_str(f'min_distance = [{int(min_distance)}]')

        tbar.close()

        # log
        VideoRebuildImpl._show_biggest_distance(ab_key_point)

        return ab_key_point

    @staticmethod
    def _show_biggest_distance(ab_key_point):
        biggest_distance = 0
        for item in ab_key_point:
            if item[0] > biggest_distance:
                biggest_distance = item[0]
        print(f'最大distance = [{biggest_distance}]')

    def _get_key_frames(self, common_size, video_path) -> list[KeyFrame]:
        v_key_i: VideoKeyFramesI = VideoKeyFramesImpl(video_path, common_size=common_size,
                                                      crop_info_path=self.crop_info_path)  # 获取视频A的画像序列
        return v_key_i.get_key_frames()

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
