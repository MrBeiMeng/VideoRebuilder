import cv2

from src.heigher_service.utils.common import BLUtils
from src.service.impl.video_iterator_impl import VideoIteratorImpl

if __name__ == '__main__':
    crop_info_path = '../static/crop_info_madajiasijiadeqie.json'

    a_path = "F:/xunleiyunpan/S02E01.The.Red.Squirrel.mkv"
    b_path = "F:/penguins season 2/1 传奇特务 (The Red Squirrel).mp4"

    common_size = BLUtils.get_common_size(a_path, b_path)

    iterator_a = VideoIteratorImpl(a_path)
    iterator_b = VideoIteratorImpl(b_path)

    iterator_a.set_current_index(0)
    print(iterator_a.get_current_index())
    frame_a = next(iterator_a)
    print(iterator_a.get_current_index())
    frame_b = next(iterator_b)

    # cv2.imshow('fa', frame_a)
    # cv2.imshow('fb', frame_b)
    #
    # cv2.waitKey(0)
    #
    # cv2.destroyAllWindows()

    feature_a = BLUtils.get_cropped_feature(frame_a, common_size=common_size, crop_info_path=crop_info_path)
    feature_b = BLUtils.get_cropped_feature(frame_b, common_size=common_size, crop_info_path=crop_info_path)

    distance = BLUtils.get_distance(feature_a, feature_b)

    print(distance)
