import multiprocessing

from src.heigher_service.impl.video_align_task_madajiasijia_impl import VideoAlignTaskMadajiasijiaImpl
from src.heigher_service.runner_interface import RunnerI


def process_task(task):
    video_a_path, video_b_path = task
    video_align_task = VideoAlignTaskMadajiasijiaImpl(video_a_path, video_b_path)
    video_align_task.run()


if __name__ == '__main__':
    # runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(video_a_path='E:/xunleiyunpan/我爱爆米花高清23fs.mkv',
    #                                                  video_b_path='E:/data/央视配音24fs/我爱爆米花.mp4')
    # runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(
    #     'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E01.Gone.in.a.Flash.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
    #     'E:/data/央视配音24fs/1 我爱大毛 Gone In A Flash.mp4')
    # runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(
    #     'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E16.Popcorn.Panic.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
    #     'D:/code/python/pycharm/VideoFrameAligner/static/我爱大毛-10s.mp4')

    # runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(
    #     'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E02.Launchtime.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
    #     'E:/data/央视配音24fs/2 月球度假记 LaunchTime.mp4')

    # runner: RunnerI = VideoAlignTaskMadajiasijiaImpl( # 差异值 导致不对齐
    #     'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E04.Operation.Plush.and.Cover.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
    #     'E:/data/央视配音24fs/4 抢救小毛 (Operation Plush & Cover).mp4')
    # runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(
    #     'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E05.Happy.King.Julien.Day.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
    #      'E:/data/央视配音24fs/5 快乐国王节 (Happy King Julien Day).mp4')
    # runner: RunnerI = VideoAlignTaskMadajiasijiaImpl( # 去除开头导致的不对齐
    #     'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E06.Paternal.Egg-Stinct.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
    #      'E:/data/央视配音24fs/6 最佳奶爸 (Paternal Egg-Stinct).mp4')
    # runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(
    #     'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E07.Assault.and.Batteries.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
    #     'E:/data/央视配音24fs/7 抢电池大作战 (Assault & Batteries).mp4')

    runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(
        'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E08.Penguiner.Takes.All.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
        'E:/data/央视配音24fs/8 企鹅的胜利 (Penguiner Takes All).mp4')

    runner.run()
