import os

import cv2
from tqdm import tqdm

from src.service.impl.video_iterator_impl import VideoIteratorImpl, VideoIteratorPrefixImpl, VideoIteratorPrefixFpsImpl, \
    VideoIteratorPrefixStepImpl
from src.service.video_iterator_interface import VideoIteratorI, VideoIteratorPrefixI

if __name__ == '__main__':
    v_path = 'F:/code/python/pycharm/detection2_bl_demo/46 英雄爱美 (The Falcon and the Sno).mp4'
    output_frames_path = 'E:/360MoveData/Users/MrB/Desktop/label_of_video_46/frames'
    # 将视频变成帧序列
    v_iter: VideoIteratorPrefixI = VideoIteratorPrefixStepImpl(v_path, 3000)

    total_frames = v_iter.get_total_f_num()
    tbar = tqdm(desc='视频转帧', unit='帧', total=total_frames)

    while True:
        try:
            frame = next(v_iter)
        except StopIteration:
            print('done！')
            break

        current_frame_index = v_iter.get_current_index()
        img_path = os.path.join(output_frames_path, f'frame_{current_frame_index}.png')
        cv2.imwrite(img_path, frame)
        tbar.update(1)

    tbar.close()
