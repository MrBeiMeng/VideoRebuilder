from unittest import TestCase

import cv2
import numpy as np

from src.heigher_service.impl.two_p_fast_dtw_sift_impl import SiftModelSingleImpl, PathSetI, PathSetImpl, \
    TwoPFastDtwSiftImpl
from src.heigher_service.runner_interface import RunnerI
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl
from src.service.video_iterator_interface import VideoIteratorPrefixI

from unittest import TestCase


class TestSiftModelSingleImpl(TestCase):
    def test_get_model(self):
        SiftModelSingleImpl().get_model()
        SiftModelSingleImpl().get_model()
        SiftModelSingleImpl().get_model()
        SiftModelSingleImpl().get_model()


class TestTwoPFastDtwSiftImpl(TestCase):

    def test_run(self):
        a_iterator: VideoIteratorPrefixI = VideoIteratorPrefixImpl('E:/xunleiyunpan/我爱爆米花高清23fs.mkv')

        for i in range(360):
            next(a_iterator)

        runner: RunnerI = TwoPFastDtwSiftImpl(v_a_path='E:/xunleiyunpan/我爱爆米花高清23fs.mkv',
                                              v_b_path='E:/data/央视配音24fs/我爱爆米花.mp4', a_iterator=a_iterator)

        runner.run()

    def test_show_when_write(self):

        a_iterator: VideoIteratorPrefixI = VideoIteratorPrefixImpl('E:/xunleiyunpan/我爱爆米花高清23fs.mkv')
        b_iterator: VideoIteratorPrefixI = VideoIteratorPrefixImpl('E:/data/央视配音24fs/我爱爆米花.mp4')

        while True:
            try:
                frame_a = next(a_iterator)
                frame_b = next(b_iterator)
            except StopIteration:
                break

            print(f"Index [{b_iterator.get_current_index()}/{b_iterator.get_total_f_num()}]")

            # 确保两个帧的维度相同
            if frame_a.shape != frame_b.shape:
                print("Frames have different dimensions, resizing frame2 to match frame1")
                frame_a = cv2.resize(frame_a, (frame_b.shape[1], frame_b.shape[0]))

            # 使用numpy的hstack函数水平堆叠两个帧
            merged_frame = np.hstack((frame_a, frame_b))

            # 使用cv2.imshow展示合并后的帧
            cv2.imshow('writing Frame', merged_frame)
            cv2.waitKey(1)

        self.fail()


class TestPathSetImpl(TestCase):
    def test_add(self):
        p_set: PathSetI = PathSetImpl()  # todo 想办法实现

        p_set.add((22, 22))
        p_set.add((22, 23))
        p_set.add((22, 24))

        p_set.add((23, 24))

        # p_set.add((3, 4))
        print(p_set.pop())

        p_set.add((25, 25))

        print(p_set.pop())
