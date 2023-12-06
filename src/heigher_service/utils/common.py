import os
import typing

import PIL
import cv2
import numpy as np

from src.heigher_service.utils.frame_cut_util import FrameCutUtil, FrameCutUtilXiGua
from src.service.impl.video_iterator_impl import VideoIteratorImpl
from skimage.metrics import structural_similarity as compare_ssim
# from SSIM_PIL import compare_ssim
from SSIM_PIL import compare_ssim as compare_ssim_gpu
from PIL import Image

from src.service.video_iterator_interface import VideoIteratorI


class BLUtils:
    @staticmethod
    def get_unique_filename(filename: str) -> str:
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filename):
            filename = f"{base}({counter}){ext}"
            counter += 1
        print(f"set output path: {filename}")
        return filename

    @staticmethod
    def get_feature(frame, common_size):

        if frame.shape[1] > common_size[0] and frame.shape[0] > common_size[1]:
            # 计算视频B的长宽比
            aspect_ratio_b = common_size[0] / common_size[1]  # 宽度/高度

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
            cropped_frame_a = frame[crop_y_start:crop_y_end, crop_x_start:crop_x_end]

            # 调整截取后的frame_a的分辨率以匹配frame_b
            resized_frame_a = cv2.resize(cropped_frame_a,
                                         (260, int(int(common_size[1] / 5) / int(common_size[0] / 5) * 260)),
                                         interpolation=cv2.INTER_AREA)
            # resized_frame_b = cv2.resize(frame_b, (cropped_frame_a.shape[1], cropped_frame_a.shape[0]),
            #                              interpolation=cv2.INTER_AREA)

            resized_frame_a = cv2.cvtColor(resized_frame_a, cv2.COLOR_BGR2GRAY)
            # 归一化
            # normalized_image = cv2.normalize(resized_frame_a, None, 0, 255, cv2.NORM_MINMAX)
            # 直方图均衡化
            equalized_image_a = cv2.equalizeHist(resized_frame_a)
            blurred_frame_a = cv2.GaussianBlur(equalized_image_a, (11, 11), 0)

            # # 应用边缘卷积
            # edge_convolved_imageA = cv2.filter2D(resized_frame_a, -1, sobel_x)

            return blurred_frame_a
        else:
            frame = cv2.resize(frame,
                               (260, int(int(common_size[1] / 5) / int(common_size[0] / 5) * 260)),
                               interpolation=cv2.INTER_AREA)  # 调整帧大小来降低计算量

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # # 归一化
            # # normalized_image = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX)
            # 直方图均衡化
            frame = cv2.equalizeHist(frame)
            frame = cv2.GaussianBlur(frame, (11, 11), 0)

            # frame = cv2.filter2D(frame, -1, self.sobel_x)

        return frame

    @staticmethod
    def calculate_histogram(frame, bins=256):
        """ 计算灰度图像的直方图 """
        hist = cv2.calcHist([frame], [0], None, [bins], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist

    @staticmethod
    def average_hash(feature, hash_size=64):
        # 缩放到 32x32
        resized = cv2.resize(feature, (hash_size, hash_size), interpolation=cv2.INTER_LINEAR)
        # 计算平均值
        avg = resized.mean()
        # 计算哈希
        hash_value = 0
        for i in range(hash_size):
            for j in range(hash_size):
                bit = 0 if resized[i, j] < avg else 1
                hash_value |= (bit << (i * hash_size + j))
        return hash_value

    @staticmethod
    def hamming_distance(hash1, hash2):
        # XOR 两个哈希值，然后计算结果中的1的个数
        x = hash1 ^ hash2
        distance = 0
        while x:
            distance += 1
            x &= x - 1
        return distance

    @staticmethod
    def crop_feature(feature, crop_info_path: str):

        # // 使用util中的裁切方法
        crop_info = FrameCutUtilXiGua(crop_info_path).crop_info

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

        # TwoPFastDtwSiftImpl.draw_matches(0, final_cropped_frame, final_cropped_frame_b)

        return final_cropped_frame

    @staticmethod
    def get_cropped_feature(frame, common_size, crop_info_path):
        return BLUtils.crop_feature(BLUtils.get_feature(frame=frame, common_size=common_size),
                                    crop_info_path=crop_info_path)

    @staticmethod
    def get_common_size(a_path, b_path):
        fps, (a_w, a_h) = VideoIteratorImpl(a_path).get_video_info()
        fps, (b_w, b_h) = VideoIteratorImpl(b_path).get_video_info()
        common_size = (a_w, a_h) if a_w < b_w and a_h < b_h else (b_w, b_h)
        return common_size

    @staticmethod
    def get_distance(feature_a, feature_b):
        feature_a = feature_a.astype(np.uint8)
        feature_b = feature_b.astype(np.uint8)

        # 计算SSIM
        ssim_value, _ = compare_ssim(feature_a, feature_b, full=True)

        # B帧全黑或全白检测
        # 设置阈值
        lower_threshold = 30  # 低于此值将被认为是黑色
        upper_threshold = 245  # 高于此值将被认为是白色

        # 检查是否接近全黑或全白
        # if np.max(feature_b) <= lower_threshold:
        #     # print("The B is nearly entirely black.")
        #     ssim_value = 1

        distance = ((2 - (ssim_value + 1)) / 2) * 100

        # Draw matches
        # TwoPFastDtwSiftImpl.draw_matches(distance=distance, feature_a=feature_a, feature_b=feature_b)

        return distance

    @staticmethod
    def get_distance_gpu(image_1, image_2: PIL.Image):

        # 计算SSIM
        ssim_value = compare_ssim_gpu(image_1, image_2)

        # B帧全黑或全白检测
        # 设置阈值
        lower_threshold = 30  # 低于此值将被认为是黑色
        upper_threshold = 245  # 高于此值将被认为是白色

        # 检查是否接近全黑或全白
        # if np.max(feature_b) <= lower_threshold:
        #     # print("The B is nearly entirely black.")
        #     ssim_value = 1

        distance = ((2 - (ssim_value + 1)) / 2) * 100

        # Draw matches
        # TwoPFastDtwSiftImpl.draw_matches(distance=distance, feature_a=feature_a, feature_b=feature_b)

        return distance

    @staticmethod
    def show_video(video_iterator: VideoIteratorI, wait=False):  # 这会影响原来的迭代器
        if wait:
            num = 0
        else:
            num = 1

        while True:
            try:
                frame = next(video_iterator)
            except StopIteration:
                break

            cv2.imshow(f'video', frame)
            cv2.waitKey(num)
