from src.heigher_service.impl.two_p_fast_dtw_sift_impl import TwoPFastDtwSiftImpl
from src.heigher_service.runner_interface import RunnerI
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl
from src.service.video_iterator_interface import VideoIteratorPrefixI

if __name__ == '__main__':
    a_iterator: VideoIteratorPrefixI = VideoIteratorPrefixImpl('E:/xunleiyunpan/我爱爆米花高清23fs.mkv')

    for i in range(360):
        next(a_iterator)

    runner: RunnerI = TwoPFastDtwSiftImpl(v_a_path='E:/xunleiyunpan/我爱爆米花高清23fs.mkv',
                                          v_b_path='E:/data/央视配音24fs/我爱爆米花.mp4', a_iterator=a_iterator,
                                          pool_size=500)

    runner.run()
