import multiprocessing

from src.heigher_service.impl.video_align_task_madajiasijia_impl import VideoAlignTaskMadajiasijiaImpl


def process_task(task):
    video_a_path, video_b_path = task
    video_align_task = VideoAlignTaskMadajiasijiaImpl(video_a_path, video_b_path)
    video_align_task.run()


if __name__ == '__main__':
    # Assuming video_paths is a list of tuples where each tuple contains a pair of video paths
    video_paths = [
        ('E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E01.Gone.in.a.Flash.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
         'E:/data/央视配音24fs/1 我爱大毛 Gone In A Flash.mp4'),
        ('E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E02.Launchtime.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
         'E:/data/央视配音24fs/2 月球度假记 LaunchTime.mp4'),
        ('E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E03.Haunted.Habitat.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
         'E:/data/央视配音24fs/3 鬼哭神嚎 (Haunted Habitat).mp4'),
        (
            'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E04.Operation.Plush.and.Cover.1080p.WEB-DL.AAC2.0.H.264'
            '-CtrlHD.mkv',
            'E:/data/央视配音24fs/4 抢救小毛 (Operation Plush & Cover).mp4'),
        ('E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E05.Happy.King.Julien.Day.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
         'E:/data/央视配音24fs/5 快乐国王节 (Happy King Julien Day).mp4'),
        ('E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E06.Paternal.Egg-Stinct.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
         'E:/data/央视配音24fs/6 最佳奶爸 (Paternal Egg-Stinct).mp4'),
        ('E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E07.Assault.and.Batteries.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
         'E:/data/央视配音24fs/7 抢电池大作战 (Assault & Batteries).mp4'),
        ('E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E08.Penguiner.Takes.All.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
         'E:/data/央视配音24fs/8 企鹅的胜利 (Penguiner Takes All).mp4'),
        (
            'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E09.Two.Feet.High.and.Rising.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
            'E:/data/央视配音24fs/9 恋脚癖大作战 (Two Feet High and Right).mp4'),
        ('E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E10.Tangled.in.the.Web.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv',
         'E:/data/央视配音24fs/10 我要红 (Tangled in the Web).mp4'),
    ]
    # a_path = 'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E06.Paternal.Egg-Stinct.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv'
    # b_path = 'E:/data/央视配音24fs/10 我要红 (Tangled in the Web).mp4'

    # Set the number of concurrent processes
    num_processes = 1

    with multiprocessing.Pool(num_processes) as pool:
        pool.map(process_task, video_paths)
