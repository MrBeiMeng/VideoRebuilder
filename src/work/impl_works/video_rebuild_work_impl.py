import time

import cv2
from tqdm import tqdm

from src.heigher_service.impl.frame_index_founder_impl import FrameIndexFounderImpl
from src.heigher_service.impl.video_rebuild_find_in_a_impl import VideoRebuildFindInAImpl
from src.heigher_service.utils.common import BLUtils
from src.heigher_service.utils.global_storage import GlobalStorage
from src.heigher_service.utils.multi_work_utils import MultiWorkUtils, MultiWorkUtilsFactory
from src.service.impl.video_iterator_impl import VideoIteratorImpl
from src.work.work_interface import WorkI


class VideoRebuildWorkImpl(WorkI):
    cache_path = "static/cache/cache_info_xi_gua.json"
    GlobalStorage.parse(cache_path)

    def __init__(self, a_path, b_path):
        self.a_path = a_path
        self.b_path = b_path

    def do_work(self):
        self.check_attributes()

        # 测试多进程读取帧

        ab_points = VideoRebuildFindInAImpl(self.a_path, self.b_path).find_same_points()

        print(ab_points)

        # done
        MultiWorkUtilsFactory().process_utils.do_work('', None)  # 销毁所有子进程
        GlobalStorage.dump(self.cache_path)

    def check_attributes(self):

        if not GlobalStorage.exist('common_size'):
            GlobalStorage.set('common_size', BLUtils.get_common_size(self.a_path, self.b_path))

        if not GlobalStorage.exist('cropping_b_part'):
            raise Exception('需要选择裁剪区域')

        pass
