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
    def get_feature(frame: np.ndarray, dsize_width: int = 64) -> np.ndarray:
        common_size = GlobalStorage.get('common_size')

        if frame.shape[1] != common_size[0] or frame.shape[0] != common_size[1]:
            # 计算视频B的长宽比
            aspect_ratio_b = common_size[0] / common_size[1]  # 宽度/高度

            # 视频A向视频B看齐
            # 计算中间截取区域的宽度和高度
            center_y, center_x = frame.shape[0] // 2, frame.shape[1] // 2
            if frame.shape[1] / frame.shape[0] > aspect_ratio_b:
                # 如果视频A的长宽比大于视频B的长宽比，则保持高度不变，调整宽度
                crop_height = frame.shape[0]
                crop_width = int(crop_height * aspect_ratio_b)
            else:
                # 如果视频A的长宽比小于等于视频B的长宽比，则保持宽度不变，调整高度
                crop_width = frame.shape[1]
                crop_height = int(crop_width / aspect_ratio_b)

            # 计算裁剪区域的边界
            crop_x_start = center_x - crop_width // 2
            crop_x_end = center_x + crop_width // 2
            crop_y_start = center_y - crop_height // 2
            crop_y_end = center_y + crop_height // 2

            # 从视频A的中间按照视频B的长宽比截取
            frame = frame[crop_y_start:crop_y_end, crop_x_start:crop_x_end]

        frame = cv2.resize(frame,
                           (64, int(common_size[1] / common_size[0] * 64)),
                           interpolation=cv2.INTER_AREA)  # 调整帧大小来降低计算量

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # # 归一化
        # # normalized_image = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX)
        # 直方图均衡化
        frame = cv2.equalizeHist(frame)
        feature = cv2.GaussianBlur(frame, (5, 5), 0)

        return feature

    @staticmethod
    def get_a_feature(frame: np.ndarray, dsize_width: int = 64) -> np.ndarray:

        feature = FeatureUtils.get_feature(frame)

        return FeatureUtils.get_cropped(feature)

    @staticmethod
    def get_b_feature(frame: np.ndarray) -> np.ndarray:
        print(FeatureUtils.get_a_feature(frame).shape)
        return FeatureUtils.get_a_feature(frame)

    @staticmethod
    def get_distance(feature_a: np.ndarray, feature_b: np.ndarray) -> float:
        if feature_a.shape != feature_b.shape:
            print(feature_a.shape, feature_b.shape)

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

        # 裁剪调整分辨率后的frame_a和frame_b的中间3/5的区域
        final_cropped_frame = feature[y_start:y_end,
                              x_start:x_end]

        return final_cropped_frame
