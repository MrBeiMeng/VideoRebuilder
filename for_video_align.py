import sys

from src.heigher_service.impl.video_align_task_madajiasijia_impl import VideoAlignTaskMadajiasijiaImpl
from src.heigher_service.runner_interface import RunnerI

videos = [("E:/360MoveData/Users/MrB/Desktop/result/9 恋脚癖大作战 (Two Feet High and Right)(1).mp4",
           "E:/360MoveData/Users/MrB/Desktop/西瓜/恋足.mp4"),
          ]


def main():
    if len(sys.argv) > 1:
        argument = sys.argv[1]
        print(f'接收到的参数值: {argument}')

        avg = None

        if len(sys.argv) > 2:
            avg = int(sys.argv[2])
            print(f"设定的匹配标准是{avg}")

        index = -int(argument)
        target = videos[index]

        print(target)

        input('回车开始')

        # runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(target[0], target[1], avg)
        runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(video_a_path=target[0],
                                                         video_b_path=target[1], reasonable_avg=avg)

        runner.run()

    else:
        print('未提供任何参数')


from moviepy.config import change_settings

change_settings({"IMAGEIO_FFMPEG_EXE": "e:/MrB/Downloads/ffmpeg-6.0/bin/ffmpeg.exe", "IMAGEIO_USE_GPU": True})
if __name__ == '__main__':
    main()
