import os

import cv2
import ffmpeg

from src.heigher_service.impl.two_p_fast_dtw_orb_impl import TwoPFastDtwOrbImpl
from src.heigher_service.impl.two_p_fast_dtw_sift_impl import TwoPFastDtwSiftImpl
from src.heigher_service.runner_interface import RunnerI
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl


class VideoAlignTaskMadajiasijiaImpl(RunnerI):
    def __init__(self, video_a_path, video_b_path, reasonable_avg=None, compare_size=None):
        self.video_a_path = video_a_path
        self.video_b_path = video_b_path
        self.reasonable_avg = reasonable_avg
        self.compare_size = compare_size

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
        # output_path = self._get_unique_filename(self.video_b_path)

        base_name = os.path.basename(self.video_b_path)

        output_path = f"E:/360MoveData/Users/MrB/Desktop/penguins_new_result/{base_name}"
        output_path = self._get_unique_filename(output_path)

        # model = ka.VGG16(include_top=False, weights='imagenet', pooling='avg')

        for i in range(360):
            try:
                frame = next(a_iterator)
            except StopIteration:
                raise Exception("不足360")

            if i == 115:
                # 对比两帧差异
                # 使用cv2.imread()函数读取图片
                image = cv2.imread('E:/RemovedD/code/python/pycharm/VidelAligner/tests/img_115_.png')

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
                                              pool_size=200, reasonable_avg=self.reasonable_avg,
                                              compare_size=self.compare_size)

        runner.run()

        final_output = f"E:/360MoveData/Users/MrB/Desktop/penguins_finally/{base_name}"

        final_output = self._get_unique_filename(final_output)

        # 合并视频和音频
        video_stream = ffmpeg.input(output_path)
        audio_stream = ffmpeg.input(self.video_b_path).audio
        ffmpeg.output(video_stream, audio_stream, final_output, vcodec='copy', acodec='copy').run()

        # video1 = VideoFileClip(self.video_b_path)
        # video2 = VideoFileClip(output_path)
        #
        # video1_audio = video1.audio
        # final_video = video2.set_audio(video1_audio)
        #
        # final_video.write_videofile(self._get_unique_filename(output_path), codec='libx264', audio_codec='aac')
