from unittest import TestCase

import cv2

from src.heigher_service.impl.two_p_align import TwoPointAlignImpl
from src.heigher_service.impl.two_p_align_sift_impl import TwoPointAlignSiftImpl
from src.heigher_service.runner_interface import RunnerI
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl
from src.service.video_iterator_interface import VideoIteratorPrefixI


class TestTwoPointAlignImpl(TestCase):

    def test_iterator(self):
        b_iterator: VideoIteratorPrefixI = VideoIteratorPrefixImpl('E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E04.Operation.Plush.and.Cover.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv')

        last_frame_list = []

        while True:
            try:
                frame = next(b_iterator)
                last_frame_list.append(frame)
            except StopIteration:
                break

            print(f"Index [{b_iterator.get_current_index()}/{b_iterator.get_total_f_num()}]")

            if b_iterator.get_current_index() == 115:
                cv2.imwrite('img_115_.png', frame)
                break

            cv2.imshow('frame b', frame)
            cv2.waitKey(40)

            if len(last_frame_list) > 1000:
                b_iterator.add_prefix(last_frame_list)
                last_frame_list.clear()

    def test_run(self):
        # self.fail()
        runner: RunnerI = TwoPointAlignImpl('E:/data/WoAiDaMaoYangShi.mp4', 'E:/data/WoAiDaMaoCeShi.mp4')
        # runner: RunnerI = TwoPointAlignImpl(
        #     'D:/code/python/pycharm/VideoFrameAligner/static/我爱爆米花-原版-开车前.mp4',
        #     'D:/code/python/pycharm/VideoFrameAligner/static/央配-我爱爆米花-开车前.mp4')
        runner.run()

    def test_run_sift(self):

        a_iterator: VideoIteratorPrefixI = VideoIteratorPrefixImpl('E:/xunleiyunpan/我爱爆米花高清23fs.mkv')

        for i in range(360):
            next(a_iterator)

        # self.fail()
        runner: RunnerI = TwoPointAlignSiftImpl('E:/xunleiyunpan/我爱爆米花高清23fs.mkv',
                                                'E:/data/央视配音24fs/我爱爆米花.mp4', a_iterator)
        # runner: RunnerI = TwoPointAlignImpl(
        #     'D:/code/python/pycharm/VideoFrameAligner/static/我爱爆米花-原版-开车前.mp4',
        #     'D:/code/python/pycharm/VideoFrameAligner/static/央配-我爱爆米花-开车前.mp4')
        runner.run()
