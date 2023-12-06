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


def average_hash(feature, hash_size=8):
    # 缩放到 8x8
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


def hamming_distance(hash1, hash2):
    # XOR 两个哈希值，然后计算结果中的1的个数
    x = hash1 ^ hash2
    distance = 0
    while x:
        distance += 1
        x &= x - 1
    return distance


if __name__ == '__main__':
    dst_path, target_path = "E:/360MoveData/Users/MrB/Desktop/源视频A.mp4", "E:/360MoveData/Users/MrB/Desktop/剪辑版B.mp4"
    # 获取两个视频的最小公共 size
    common_size = BLUtils.get_common_size(dst_path, target_path)

    # 读取所有帧到内存
    video_a_feature_list = get_feature_to_arr(dst_path, common_size, crop_info_path)

    print('已读取所有a到内存')

    # 获得hash数组
    hash_a_list = [average_hash(feature) for feature in video_a_feature_list]

    video_b_feature_list = get_feature_to_arr(target_path, common_size, crop_info_path)
    # 通过B的帧寻找对应的索引

    for feature_b in video_b_feature_list:

        indices = []
        hash_b = average_hash(feature_b)
        # 从hash数组中寻找接近的值
        for index_a, hash_a in enumerate(hash_a_list):
            distance = hamming_distance(hash_a, hash_b)
            if distance < 10:
                indices.append(index_a)

        print(f'indices = {len(indices)}')

        indices_v2 = []
        min_distance = 999
        for index_a in indices:
            feature_a = video_a_feature_list[index_a]
            distance = BLUtils.get_distance(feature_a, feature_b)
            if distance < 10:
                if distance < min_distance:
                    min_distance = distance
                indices_v2.append(index_a)

        print(f'indices_v2 = {len(indices_v2)} min_distance = [{min_distance}]')

    pass
