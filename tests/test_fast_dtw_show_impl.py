import time
from unittest import TestCase

import cv2

from src.service.impl.video_iterator_index_search_impl import VideoIteratorIndexSearchImpl
from src.service.video_iterator_index_search_interface import VideoIteratorIndexSearchI

import logging
import sqlalchemy


# 禁用sqlalchemy的日志输出
# sqlalchemy.engine.echo = False

class TestFastDtwShowImpl(TestCase):
    def test_video_inter(self):
        # 禁用SQLAlchemy的日志
        logging.getLogger('sqlalchemy.engine').propagate = False
        logging.getLogger('sqlalchemy.pool').propagate = False
        logging.getLogger('sqlalchemy.orm').propagate = False

        self.video_path_a = "E:/xunleiyunpan/我爱爆米花高清23fs.mkv"
        # self.video_path_b = "video_path_b"

        self.video_a_iterator: VideoIteratorIndexSearchI = VideoIteratorIndexSearchImpl(self.video_path_a)

        print(self.video_a_iterator.get_video_info())
        print(self.video_a_iterator.get_total_f_num())

        cv2.imshow("video A", self.video_a_iterator.get_by_index(100))
        cv2.waitKey(1)
        time.sleep(5)

        self.video_a_iterator.reset_by_index(0)
        for i in range(self.video_a_iterator.get_total_f_num()):
            cv2.imshow("video A", next(self.video_a_iterator))
            cv2.waitKey(1)
            print(f"第[{i}]帧")
            if i == 100:
                time.sleep(5)

        pass
        # self.fail()
