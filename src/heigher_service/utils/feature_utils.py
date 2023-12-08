import cv2
import numpy as np

from src.heigher_service.utils.common import BLUtils
from src.heigher_service.utils.global_storage import GlobalStorage
from src.heigher_service.utils.util_interface.feature_util_heigher_interface import FeatureUtilsHigherI
from src.heigher_service.utils.util_interface.feature_util_interface import FeatureUtilsI


class FeatureUtils(FeatureUtilsHigherI, FeatureUtilsI):
    """
    !!!
    可能的几个方案
    方案一：最方便的 计算一个共同的大小common size ，通过这个大小将两视频调整至一致的大小。再通过crop裁切出重点的部分。
    方案二：比较方便： 先裁剪b帧，计算裁剪过后的视频B与原视频相交的部分，得到关键帧。好处是可以解决目标视频做了边缘裁剪的问题。
    方案三： 计算量较大： 将A视频放大至合适的大小直接保存，b帧进行裁剪保留重点部分，每次对比时，寻找两帧的交集部分，返回distance。好处是即使视频b进行了镜头移动，也能完整还原。

    当前类使用方案一。
    """

    # def __init__(self, common_size, rebuild_cropping_b_part=False):
    #
    #     pass

    @staticmethod
    def get_a_feature(frame: np.ndarray, dsize_width: int = 64) -> np.ndarray:
        feature = BLUtils.get_feature(frame, GlobalStorage.get('common_size'))

        return FeatureUtils.get_cropped(feature)

    @staticmethod
    def get_b_feature(frame: np.ndarray) -> np.ndarray:
        return FeatureUtils.get_a_feature(frame)

    @staticmethod
    def get_distance(feature_a: np.ndarray, feature_b: np.ndarray) -> float:
        return BLUtils.get_distance(feature_a, feature_b)

    # 下面是FeatureUtilsI 的方法

    @staticmethod
    def get_intersection_part(frame: np.ndarray) -> np.ndarray:
        pass

    @staticmethod
    def get_cropped(feature: np.ndarray) -> np.ndarray:
        crop_info = GlobalStorage.get('cropping_b_part')
        height, width = feature.shape[:2]

        # 根据比例计算裁剪区域的坐标
        x_start = int(crop_info["x_ratio_start"] * width)
        y_start = int(crop_info["y_ratio_start"] * height)
        x_end = int(crop_info["x_ratio_end"] * width)
        y_end = int(crop_info["y_ratio_end"] * height)

        # # 计算裁剪区域的边界（如果需要进一步裁剪）
        # crop_width_start = width // 5
        # crop_width_end = 4 * width // 5
        # crop_height_start = height // 5
        # crop_height_end = 4 * height // 5

        # height, width = frame_b.shape[:2]
        # crop_width_start = width // 5
        # crop_width_end = width - 1
        # crop_height_start = 2 * height // 3
        # crop_height_end = height - 1

        # 裁剪调整分辨率后的frame_a和frame_b的中间3/5的区域
        final_cropped_frame = feature[y_start:y_end,
                              x_start:x_end] if feature is not None else None

        return final_cropped_frame
