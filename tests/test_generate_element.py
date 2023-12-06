import os
import time
from timeit import timeit

import cv2
import numpy as np
from tqdm import tqdm

from src.service.impl.featuer_iterator_cache_impl import FeatureIteratorCacheImpl
from src.service.impl.video_iterator_impl import VideoIteratorImpl

from skimage.metrics import structural_similarity as compare_ssim_cpu_1

from SSIM_PIL import compare_ssim as compare_ssim_gpu_1
from PIL import Image

image1 = Image.open("E:/360MoveData/Users/MrB/Pictures/81F2hWFJeML._SX600_.jpg")
image2 = Image.open("E:/360MoveData/Users/MrB/Pictures/81F2hWFJeML._SX600_.jpg")

frame_a = cv2.imread("E:/360MoveData/Users/MrB/Pictures/81F2hWFJeML._SX600_.jpg")
frame_b = cv2.imread("E:/360MoveData/Users/MrB/Pictures/81F2hWFJeML._SX600_.jpg")


# cv2.imshow('test', frame_b)
# cv2.waitKey(0)


def compare_ssim_cpu():
    feature_a = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
    feature_b = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)

    feature_a = feature_a.astype(np.uint8)
    feature_b = feature_b.astype(np.uint8)

    # 计算SSIM
    ssim_value, _ = compare_ssim_cpu_1(feature_a, feature_b, full=True)
    # compare_ssim_cpu_1(frame_a, frame_b)

    # print(ssim_value)
    pass


def compare_ssim_gpu():
    distance = compare_ssim_gpu_1(image1, image2)
    # print(distance)
    pass


if __name__ == '__main__':
    # 计算1000次，比较时间差距
    # gpu_duration = timeit(stmt='compare_ssim_gpu()',
    #                       setup='from tests.test_generate_element import compare_ssim_gpu', number=10000)
    # print(f'gpu 计算时间{gpu_duration}')
    #
    # cpu_duration = timeit(stmt='compare_ssim_cpu()',
    #                       setup='from tests.test_generate_element import compare_ssim_cpu', number=10000)
    # print(f'cpu 计算时间{cpu_duration}')

    # 将 BGR 转换为 RGB
    rgb_image = cv2.cvtColor(frame_a, cv2.COLOR_BGR2RGB)

    # 将 NumPy 数组转换为 PIL 图像
    pil_image = Image.fromarray(rgb_image)

    pil_image.show('test')
