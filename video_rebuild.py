from src.heigher_service.impl.video_rebuild_common_sequence_impl import VideoRebuildCommonSequenceImpl
from src.heigher_service.impl.video_rebuild_find_in_a_impl import VideoRebuildFindInAImpl
from src.heigher_service.impl.video_rebuild_impl import VideoRebuildImpl
from src.heigher_service.runner_interface import RunnerI

import os

from src.heigher_service.utils.global_storage import GlobalStorage
from src.work.impl_works.video_rebuild_work_impl import VideoRebuildWorkImpl
from src.work.work_interface import WorkI

#
# if __name__ == '__main__':
#     runner: RunnerI = VideoRebuildFindInAImpl(
#         "E:/data/02e06 Source.mp4",
#         "E:/data/202312071923.mp4")
#
#     # runner: RunnerI = VideoRebuildFindInAImpl(
#     #     "E:/360MoveData/Users/MrB/Desktop/源视频A.mp4",
#     #     "E:/360MoveData/Users/MrB/Desktop/剪辑版B.mp4")
#
#     runner.run()

# cache_path = "static/cache/cache_madajiasijiadeqie.json"
cache_path = "static/cache/cache_info_xi_gua.json"
GlobalStorage.parse(cache_path)

if __name__ == '__main__':
    worker: WorkI = VideoRebuildWorkImpl("E:/data/02e06 Source.mp4",
                                         "E:/data/202312071923.mp4")

    worker.do_work()

# cache_path = "static/cache/cache_madajiasijiadeqie.json"
# GlobalStorage.parse(cache_path)
#
# if __name__ == '__main__':
#     worker: WorkI = VideoRebuildWorkImpl("F:/xunleiyunpan/S01E45.Jiggles.mkv",
#                                          "E:/data/Penguins/45 我爱绿绿 (Jiggles).mp4")
#
#     worker.do_work()
