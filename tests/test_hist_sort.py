# 通过颜色直方图为feature 进行排序
import cv2
import numpy as np

from src.heigher_service.utils.common import BLUtils
from src.service.impl.featuer_iterator_cache_impl import FeatureIteratorCacheImpl
from src.service.video_iterator_interface import VideoIteratorI

# runner: RunnerI = VideoRebuildFindInAImpl(
#     "E:/360MoveData/Users/MrB/Desktop/源视频A.mp4",
#     "E:/360MoveData/Users/MrB/Desktop/剪辑版B.mp4")

crop_info_path = '../static/crop_info_xi_gua.json'


def get_feature_to_arr(path, t_common_size, t_crop_info_path):
    result = []

    iterator = FeatureIteratorCacheImpl(path, common_size, crop_info_path)
    while True:

        try:
            feature = next(iterator)
        except StopIteration:
            break

        result.append(feature)

    return result


# def calculate_histogram(frame, bins=256):
#     """ 计算图像的颜色直方图 """
#     hist = cv2.calcHist([frame], [0, 1, 2], None, [bins, bins, bins], [0, 256, 0, 256, 0, 256])
#     hist = cv2.normalize(hist, hist).flatten()
#     return hist

def calculate_histogram(frame, bins=256):
    """ 计算灰度图像的直方图 """
    hist = cv2.calcHist([frame], [0], None, [bins], [0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist


def get_sorted_v_frames(video_feature_list):
    # 计算每一帧的颜色直方图
    # 计算每个直方图的平均值

    histograms = [calculate_histogram(frame) for frame in video_feature_list]

    histogram_means = [np.mean(hist) for hist in histograms]

    # 将每个直方图的平均值与其索引配对
    frame_hist_and_index = list(zip(histogram_means, range(len(video_feature_list))))

    # 排序：这里以直方图的平均值作为排序依据
    frame_hist_and_index.sort(key=lambda x: x[0])

    # 提取排序后的帧和它们的索引
    sorted_frames_with_index = [(hist, index) for hist, index in frame_hist_and_index]

    return sorted_frames_with_index


def binary_search_range(sorted_frames, target, tolerance):
    left, right = 0, len(sorted_frames) - 1
    result_indices = []

    while left <= right:
        mid = (left + right) // 2
        mid_mean_hist = sorted_frames[mid][0]  # 获取中间帧的直方图平均值

        # 检查是否在容差范围内
        if abs(mid_mean_hist - target) <= tolerance:
            # 向左和向右扩展，寻找所有符合条件的帧
            l, r = mid - 1, mid + 1
            result_indices.append(sorted_frames[mid][1])  # 添加中间帧的索引

            # 向左扩展
            while l >= 0 and abs(sorted_frames[l][0] - target) <= tolerance:
                result_indices.append(sorted_frames[l][1])
                l -= 1

            # 向右扩展
            while r < len(sorted_frames) and abs(sorted_frames[r][0] - target) <= tolerance:
                result_indices.append(sorted_frames[r][1])
                r += 1

            break  # 跳出循环
        elif mid_mean_hist < target:
            left = mid + 1
        else:
            right = mid - 1

    return result_indices


if __name__ == '__main__':
    dst_path, target_path = "E:/360MoveData/Users/MrB/Desktop/源视频A.mp4", "E:/360MoveData/Users/MrB/Desktop/剪辑版B.mp4"
    # 获取两个视频的最小公共 size
    common_size = BLUtils.get_common_size(dst_path, target_path)

    # 读取所有帧到内存
    video_a_feature_list = get_feature_to_arr(dst_path, common_size, crop_info_path)

    print('已读取所有a到内存')

    # 为帧进行排序
    sorted_v_a_frames = get_sorted_v_frames(video_a_feature_list)

    video_b_feature_list = get_feature_to_arr(target_path, common_size, crop_info_path)
    # 通过B的帧寻找对应的索引

    for feature_b in video_b_feature_list:
        hist_b = calculate_histogram(feature_b)
        b_mean_hist = np.mean(hist_b)

        indices = binary_search_range(sorted_v_a_frames, b_mean_hist, 0.0001)

        print(f'indices = {indices}')

        indices_v2 = []
        min_distance = 999
        for index_a in indices:
            feature_a = video_a_feature_list[index_a]
            distance = BLUtils.get_distance(feature_a, feature_b)
            if distance < 10:
                if distance < min_distance:
                    min_distance = distance
                indices_v2.append(index_a)

        print(f'indices_v2 = {indices_v2} min_distance = [{min_distance}]')

    pass
