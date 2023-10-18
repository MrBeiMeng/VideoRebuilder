from unittest import TestCase

import cv2
import numpy as np

from src.heigher_service.impl.two_p_fast_dtw_orb_impl import TwoPFastDtwOrbImpl
from src.heigher_service.impl.two_p_fast_dtw_sift_impl import SiftModelSingleImpl, PathSetI, PathSetImpl, \
    TwoPFastDtwSiftImpl
from src.heigher_service.impl.two_p_fast_dtw_surf_impl import TwoPFastDtwSurfImpl
from src.heigher_service.runner_interface import RunnerI
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl
from src.service.video_iterator_interface import VideoIteratorPrefixI

from unittest import TestCase


class TestTwoPFastDtwOrbImpl(TestCase):

    def test_run(self):
        a_iterator: VideoIteratorPrefixI = VideoIteratorPrefixImpl('E:/xunleiyunpan/我爱爆米花高清23fs.mkv')

        for i in range(360):
            next(a_iterator)

        runner: RunnerI = TwoPFastDtwOrbImpl(v_a_path='E:/xunleiyunpan/我爱爆米花高清23fs.mkv',
                                             v_b_path='E:/data/央视配音24fs/我爱爆米花.mp4', a_iterator=a_iterator,
                                             pool_size=500)

        runner.run()
