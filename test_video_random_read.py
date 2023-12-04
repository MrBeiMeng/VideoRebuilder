import cv2

# 打开视频文件
cap = cv2.VideoCapture('F:/code/python/pycharm/detection2_bl_demo/46 英雄爱美 (The Falcon and the Sno).mp4')

# 指定要访问的帧号
frame_index = 5000

# 将位置设置为特定的帧号
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

# 读取该帧
success, frame = cap.read()
if success:
    # 在这里处理帧
    # 例如：显示帧
    cv2.imshow('Frame', frame)
    cv2.waitKey(0)

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
success, frame = cap.read()
if success:
    # 在这里处理帧
    # 例如：显示帧
    cv2.imshow('Frame', frame)
    cv2.waitKey(0)


# 释放视频捕获对象
cap.release()
cv2.destroyAllWindows()

# 比对两个视频
# 先计算视频A的画像（即特征帧序列）（每一帧画像应该保存一个对应的索引区间。）
# 读取视频B进行画像比对，这一步是为了大致的确定比对的范围。
#    方案一：计算视频B的画像，在A画像序列中进行寻找（取最接近的）
# 精细比对