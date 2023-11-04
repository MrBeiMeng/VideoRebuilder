import os
import sys

import moviepy.editor as mp


# 或者
# import ffmpeg

def list_videos(directory):
    return [f for f in os.listdir(directory) if f.endswith('.mp4') or f.endswith('.avi')]


def process_videos(folder_c, folder_b):
    videos_c = list_videos(folder_c)
    videos_b = list_videos(folder_b)

    common_videos = set(videos_c).intersection(videos_b)

    for video_name in common_videos:
        user_input = input(f"Process {video_name}? (1 for yes, anything else for no): ")
        if user_input == '1':
            video_c = mp.VideoFileClip(os.path.join(folder_c, video_name))
            video_b = mp.VideoFileClip(os.path.join(folder_b, video_name))
            audio_b = video_b.audio
            final_video = video_c.set_audio(audio_b)
            final_video.write_videofile(os.path.join(folder_c, f'processed_{video_name}'))


if __name__ == '__main__':

    if len(sys.argv) > 2:
        path_c = str(sys.argv[1])

        path_b = str(sys.argv[2])

        print(f'接收到的参数值: path_c = [{path_c}],path_b = [{path_b}],按回车确认')
        input()

        # 使用方法:
        process_videos(path_c, path_b)
    else:
        print("请传入参数 1 Path C(被覆盖) 2 Path B(源)")
