from unittest import TestCase

from src.heigher_service.impl.video_distance.same_video_distance_sift import SameVideoDistanceSift, \
    SameVideoDistanceSiftRANSAC
from src.heigher_service.impl.video_distance.same_video_distance_vgg16 import SameVideoDistanceVgg16


# VGG16特征提取器的实现


class TestSamePDistanceList(TestCase):

    def test_generate_distance_list_with_same_videos(self):
        runner = SameVideoDistanceVgg16('E:/xunleiyunpan/我爱爆米花1080p高码率L.mp4',
                                        'E:/xunleiyunpan/我爱爆米花30fps480p降分辨率.mp4')
        runner.test_generate_distance_list_with_same_videos()

    def test_generate_distance_list_with_same_videos_by_sift_compute(self):
        runner = SameVideoDistanceSift('E:/xunleiyunpan/我爱爆米花1080p高码率L.mp4',
                                       'E:/xunleiyunpan/我爱爆米花30fps480p降分辨率.mp4',
                                       draw_name='我爱爆米花不同分辨率同帧差异值@sift_same_size')
        runner.test_generate_distance_list_with_same_videos()

    def test_generate_distance_list_with_same_videos_by_sift_compute_RANSAC(self):  # 放弃
        runner = SameVideoDistanceSiftRANSAC('E:/xunleiyunpan/我爱爆米花1080p高码率L.mp4',
                                             'E:/xunleiyunpan/我爱爆米花30fps480p降分辨率.mp4',
                                             draw_name='我爱爆米花不同分辨率同帧差异值@sift_RANSAC')
        runner.test_generate_distance_list_with_same_videos()
