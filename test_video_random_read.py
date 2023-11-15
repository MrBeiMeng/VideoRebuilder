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
