from unittest import TestCase

from src.heigher_service.impl.video_align_task_madajiasijia_impl import VideoAlignTaskMadajiasijiaImpl
from src.heigher_service.runner_interface import RunnerI


class TestVideoAlignTaskMadajiasijiaImpl(TestCase):
    def test_run(self):
        # runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(video_a_path='E:/xunleiyunpan/我爱爆米花高清23fs.mkv',
        #                                                  video_b_path='E:/data/央视配音24fs/我爱爆米花.mp4')
        runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(
            "E:/360MoveData/Users/MrB/Desktop/视频A.mp4",
            "E:/360MoveData/Users/MrB/Desktop/视频B.mp4")

        # runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(
        #     'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E02.Launchtime.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
        #     'E:/data/央视配音24fs/2 月球度假记 LaunchTime.mp4')

        runner.run()
