import sys

from src.heigher_service.impl.video_align_task_madajiasijia_impl import VideoAlignTaskMadajiasijiaImpl
from src.heigher_service.runner_interface import RunnerI

videos = [('E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E17.Go.Fish.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
           'E:/data/央视配音24fs/17 捕鱼记 (Go Fish).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E16.Popcorn.Panic.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/16 我爱爆米花(Popcorn Panic).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E15.Little.Zoo.Coupe.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/15 不吐不快 (All Choked Up).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E14.All.Choked.Up.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/14 动物园赛车 (Little Zoo Coupe).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E13.Kingdom.Come.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/13 接受王国 (Kingdom Come).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E12.The.Hidden.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/12 看不见的敌人 (The Hidden).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E11.Crown.Fools.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/11 我要王冠 Crown Fools.mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E10.Tangled.in.the.Web.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/10 我要红 (Tangled in the Web).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E09.Two.Feet.High.and.Rising.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/9 恋脚癖大作战 (Two Feet High and Right).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E08.Penguiner.Takes.All.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/8 企鹅的胜利 (Penguiner Takes All).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E07.Assault.and.Batteries.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/7 抢电池大作战 (Assault & Batteries).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E06.Paternal.Egg-Stinct.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/6 最佳奶爸 (Paternal Egg-Stinct).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E05.Happy.King.Julien.Day.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/5 快乐国王节 (Happy King Julien Day).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E04.Operation.Plush.and.Cover.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/4 抢救小毛 (Operation Plush & Cover).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E03.Haunted.Habitat.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/3 鬼哭神嚎 (Haunted Habitat).mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E02.Launchtime.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/2 月球度假记 LaunchTime.mp4'), (
              'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E01.Gone.in.a.Flash.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
              'E:/data/央视配音24fs/1 我爱大毛 Gone In A Flash.mp4')]


def main():
    if len(sys.argv) > 1:
        argument = sys.argv[1]
        print(f'接收到的参数值: {argument}')

        index = -int(argument)
        target = videos[index]

        print(target)

        input('回车开始')

        runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(target[0], target[1])

        runner.run()

    else:
        print('未提供任何参数')


if __name__ == '__main__':
    main()
