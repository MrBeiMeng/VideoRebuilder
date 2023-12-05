# import tensorflow as tf
#
# print(tf.__version__)
# print(tf.test.gpu_device_name())
# print(tf.config.experimental.set_visible_devices)
# print('GPU:', tf.config.list_physical_devices('GPU'))
# print('CPU:', tf.config.list_physical_devices(device_type='CPU'))
# print(tf.config.list_physical_devices('GPU'))
# print(tf.test.is_gpu_available())
# # 输出可用的GPU数量
# print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
# # 查询GPU设备

import os

import numpy as np
from tqdm import tqdm

# 使用os模块中的add_dll_directory函数
# 用于将指定路径添加到DLL搜索路径中，以便在程序运行时加载DLL文件
os.add_dll_directory(r'C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8\\bin')
os.add_dll_directory(r'E:\\MrB\\Downloads\\opencv_contrib_cuda_4.6.0.20221106_win_amd64 (1)\\install\\x64\\vc17\\bin')

import cv2

image_path = "E:/RemovedD/code/python/pycharm/VidelAligner/static/img/img_115_.png"

# 加载图像
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)


# 显示输出
cv2.imshow('input', img)
cv2.waitKey()

# 创建GPU图像对象
gpu_img = cv2.cuda_GpuMat()
gpu_img.upload(img)

# 创建GPU输出对象
gpu_output = cv2.cuda_GpuMat()

# 创建Sobel算子
sobel = cv2.cuda.createSobelFilter(cv2.CV_8UC1, cv2.CV_8UC1, 1, 1)

# 运行Sobel算子
sobel.apply(gpu_img, gpu_output)

# 将输出从GPU对象中下载到CPU中
output = gpu_output.download()

print(output)

# 显示输出
cv2.imshow('Output', output)
cv2.waitKey()
