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

from tqdm import tqdm

from tests.test_generate_element import compare_ssim_cpu

# 使用os模块中的add_dll_directory函数
# 用于将指定路径添加到DLL搜索路径中，以便在程序运行时加载DLL文件
os.add_dll_directory(r'C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8\\bin')
os.add_dll_directory(r'E:\\MrB\\Downloads\\opencv_contrib_cuda_4.6.0.20221106_win_amd64 (1)\\install\\x64\\vc17\\bin')

import cv2

# print(cv2.cuda.printCudaDeviceInfo(0))

# # 检查是否支持CUDA
if not cv2.cuda.getCudaEnabledDeviceCount():
    print("CUDA is not available. Please make sure CUDA drivers are installed.")
    exit()
#
print('---')
print(cv2.cuda.getCudaEnabledDeviceCount())
# 创建GPU设备对象
cv2.cuda.setDevice(0)
# gpu_id = 0  # 选择GPU设备的ID
# device = cv2.cuda.Device(gpu_id)
# ctx = device.createContext()

# 打开视频文件
video_path = "C:/Users/MrB/Videos/the_power_of_love_bilibili.mp4"
# cap = cv2.VideoCapture(video_path)  # 最重要

# 检查视频文件是否成功打开
# if not cap.isOpened():
#     print("Failed to open the video file.")
#     exit()

# 设置GPU加速
# cap.set(cv2.CAP_PROP_CUDA_MPS, 1)

count = 0
tbar = tqdm(desc='读取视频', unit='帧')

# 循环读取视频的每一帧
# while True:
#     # 使用GPU加速读取一帧
#     # ret, frame = cap.read(cv2.CAP_CUDA)
#     ret, frame = cap.read()
#     count += 1
#     tbar.update(1)
#
#     # 检查是否成功读取帧
#     if not ret:
#         brea

# 在这里进行你希望执行的操作
# ...

# gpu
cap = cv2.cudacodec.createVideoReader(video_path)

# frame = frame.download()
# cv2.imshow('image', frame)
# cv2.waitKey(1)

tbar.close()

print(f'count = {count}')

# 释放资源
cap.release()
cv2.destroyAllWindows()
