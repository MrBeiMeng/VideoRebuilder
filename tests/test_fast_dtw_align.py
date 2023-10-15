from unittest import TestCase


from src.heigher_service.impl.fast_dtw_align import FastDtwAlign
from src.heigher_service.runner_interface import RunnerI


class TestFastDtwAlign(TestCase):
    def test_run(self):
        runner: RunnerI = FastDtwAlign('E:/data/WoAiDaMaoYangShi.mp4', 'E:/data/WoAiDaMaoYangShiPianDuan.mp4')

        runner.run()
