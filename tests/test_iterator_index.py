import cv2

from src.service.impl.video_iterator_impl import VideoIteratorImpl
from src.service.video_iterator_interface import VideoIteratorI

if __name__ == '__main__':
    iter_a: VideoIteratorI = VideoIteratorImpl("F:/xunleiyunpan/S02E06.Hard.Boiled.Eggy.mkv")

    frame = next(iter_a)

    cv2.imshow('frame', frame)
    cv2.waitKey(0)

    iter_a.set_current_index(0)
    frame = next(iter_a)

    cv2.imshow('frame', frame)
    cv2.waitKey(0)
