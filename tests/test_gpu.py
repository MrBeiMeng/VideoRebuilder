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


import cv2

print(cv2.__version__)

print(cv2.cuda.printCudaDeviceInfo(0))

# 检查是否支持CUDA
if not cv2.cuda.getCudaEnabledDeviceCount():
    print("CUDA is not available. Please make sure CUDA drivers are installed.")
    exit()

# 创建GPU设备对象
gpu_id = 0  # 选择GPU设备的ID
device = cv2.cuda.Device(gpu_id)
ctx = device.createContext()

# 打开视频文件
video_path = "E:/xunleiyunpan/我爱爆米花高清23fs.mkv"
cap = cv2.VideoCapture(video_path)

# 检查视频文件是否成功打开
if not cap.isOpened():
    print("Failed to open the video file.")
    exit()

# 设置GPU加速
cap.set(cv2.CAP_PROP_CUDA_MPS, 1)

# 循环读取视频的每一帧
while True:
    # 使用GPU加速读取一帧
    ret, frame = cap.read(cv2.CAP_CUDA)

    # 检查是否成功读取帧
    if not ret:
        break

    # 在这里进行你希望执行的操作
    # ...

# 释放资源
cap.release()
cv2.destroyAllWindows()
