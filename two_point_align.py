from src.heigher_service.impl.two_p_align_sift_impl import TwoPointAlignSiftImpl, TwoPointAlignSiftImplMaDaJiaSiJia
from src.heigher_service.runner_interface import RunnerI
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl
from src.service.video_iterator_interface import VideoIteratorPrefixI

if __name__ == '__main__':
    a_iterator: VideoIteratorPrefixI = VideoIteratorPrefixImpl('E:/xunleiyunpan/我爱爆米花高清23fs.mkv')

    for i in range(360):
        next(a_iterator)

    # self.fail()
    runner: RunnerI = TwoPointAlignSiftImplMaDaJiaSiJia('E:/xunleiyunpan/我爱爆米花高清23fs.mkv',
                                                        'E:/data/央视配音24fs/我爱爆米花.mp4', a_iterator)
    # runner: RunnerI = TwoPointAlignImpl(
    #     'D:/code/python/pycharm/VideoFrameAligner/static/我爱爆米花-原版-开车前.mp4',
    #     'D:/code/python/pycharm/VideoFrameAligner/static/央配-我爱爆米花-开车前.mp4')
    runner.run()
