from tqdm import tqdm

from src.service.impl.video_creator_impl import VideoCreatorImpl
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl
from src.service.video_creator_interface import VideoCreatorI
from src.service.video_iterator_interface import VideoIteratorPrefixI

# if __name__ == '__main__':
#     v_b_path = ''
#
#     b_iterator: VideoIteratorPrefixI = VideoIteratorPrefixImpl(v_b_path)
#
#     fps_b, (b_w, b_h) = b_iterator.get_video_info()
#
#     creator: VideoCreatorI = VideoCreatorImpl('changed.mp4', fps_b, (b_w, b_h))
#
#     # 帧率转换的一个操作


import cv2

target_fps = 5

# frames = []
vidcap = cv2.VideoCapture('E:/xunleiyunpan/S01E01.Gone.in.a.Flash.mkv')
sec = 0
frameRate = 1 / target_fps  # it will capture image in each 0.5 second

# 创建一个保存
# 获取视频的帧率和尺寸
fps_a = vidcap.get(cv2.CAP_PROP_FPS)
width_a = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
height_a = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
creator: VideoCreatorI = VideoCreatorImpl('changed.mp4', target_fps, (width_a, height_a))

total = int(int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) * (1 / fps_a) / frameRate)

temp_tbar = tqdm(total=total, desc='改变帧率', unit='帧')

while True:
    sec = round(sec, 2)
    sec = sec + frameRate
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
        # frames.append(image)
        creator.write_frame(image)
        temp_tbar.update(1)
        # cv2.imshow('frame', image)
        # cv2.waitKey(1)
    else:
        break

vidcap.release()
creator.release()
cv2.destroyAllWindows()
