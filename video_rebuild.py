from src.heigher_service.impl.video_rebuild_common_sequence_impl import VideoRebuildCommonSequenceImpl
from src.heigher_service.impl.video_rebuild_find_in_a_impl import VideoRebuildFindInAImpl
from src.heigher_service.impl.video_rebuild_impl import VideoRebuildImpl
from src.heigher_service.runner_interface import RunnerI

import os


if __name__ == '__main__':


    runner: RunnerI = VideoRebuildFindInAImpl(
        "F:/xunleiyunpan/S02E06.Hard.Boiled.Eggy.mkv",
        "E:/360MoveData/Users/MrB/Desktop/企鹅特工孵化鸭子，用训练作为胎教，结果鸭子一出生就成为特工@不正经的小酥肉.mp4")

    # runner: RunnerI = VideoRebuildFindInAImpl(
    #     "E:/360MoveData/Users/MrB/Desktop/源视频A.mp4",
    #     "E:/360MoveData/Users/MrB/Desktop/剪辑版B.mp4")

    runner.run()
