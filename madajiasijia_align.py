import sys

from src.heigher_service.impl.video_align_task_madajiasijia_impl import VideoAlignTaskMadajiasijiaImpl
from src.heigher_service.runner_interface import RunnerI

videos = [
    ('E:/xunleiyunpan/S01E47.The.Penguin.Stays.in.the.Picture.mkv',
     'E:/data/Penguins/47 我最可爱 (The Penguin Stays In the..).mp4'),
    ('E:/xunleiyunpan/S01E46.The.Falcon.and.the.Snow.Job.mkv',
     'E:/data/Penguins/46 英雄爱美 (The Falcon and the Sno).mp4'),
    ('E:/xunleiyunpan/S01E45.Jiggles.mkv', 'E:/data/Penguins/45 我爱绿绿 (Jiggles).mp4'),
    ('E:/xunleiyunpan/S01E44.Snakehead.mkv', 'E:/data/Penguins/44 大战怪怪鱼 (SnakeHead).mp4'),
    ('E:/xunleiyunpan/S01E43.Zoo.Tube.mkv', 'E:/data/Penguins/43 倒闭危机 (Zoo Tube).mp4'),
    ('E:/xunleiyunpan/S01E42.Otter.Things.Have.Happened.mkv',
     'E:/data/Penguins/42 乱点鸳鸯谱 (Otter Things Have Ha...).mp4'),
    ('E:/xunleiyunpan/S01E41.An.Elephant.Never.Forgets.mkv',
     'E:/data/Penguins/41 大象复仇记 (An Elephant Never Fo..).mp4'),
    ('E:/xunleiyunpan/S01E40.Over.Phil.mkv', 'E:/data/Penguins/40 我的好兄弟 (Over Phil).mp4'),
    ('E:/xunleiyunpan/S01E39.Miss.Understanding.mkv', 'E:/data/Penguins/39 我要当女生 (Miss Understanding).mp4'),
    ('E:/xunleiyunpan/S01E38.Untouchable.mkv', 'E:/data/Penguins/38 不要摸我 (Untouchable).mp4'),
    ('E:/xunleiyunpan/S01E37.All.King.No.Kingdom.mkv',
     'E:/data/Penguins/37 不能没有你 (All King, No Kingdom).mp4'),
    ('E:/xunleiyunpan/S01E36.Sting.Operation.mkv', 'E:/data/Penguins/36 防蜂大作战 (Sting Operation).mp4'),
    ('E:/xunleiyunpan/S01E35.I.Was.a.Penguin.Zombie.mkv', 'E:/data/Penguins/35 僵尸企鹅.mp4'),
    ('E:/xunleiyunpan/S01E34.Jungle.Law.mkv', 'E:/data/Penguins/34 天下大乱 (Jungle Law).mp4'),
    ('E:/xunleiyunpan/S01E33.Out.of.the.Groove.mkv', 'E:/data/Penguins/33 武功尽失 (Out of the Groove).mp4'),
    ('E:/xunleiyunpan/S01E32.Mask.of.the.Racoon.mkv', 'E:/data/Penguins/32 侠盗阿奇 (Mask Of The Raccoon).mp4'),
    ('E:/xunleiyunpan/S01E31.What.Goes.Around.mkv', 'E:/data/Penguins/31 好心有好报 (What Goes Around).mp4'),
    ('E:/xunleiyunpan/S01E30.Tagged.mkv', 'E:/data/Penguins/30 紧盯不放 (Tagged).mp4'),
    ('E:/xunleiyunpan/S01E29.Monkey.Love.mkv', 'E:/data/Penguins/29 恋爱绝招 (Monkey Love).mp4'),
    ('E:/xunleiyunpan/S01E28.Cats.Cradle.mkv', "E:/data/Penguins/28 救猫记 (Cat's Cradle).mp4"),
    ('E:/xunleiyunpan/S01E27.Otter.Gone.Wild.mkv', 'E:/data/Penguins/27 野性大发 (Otter Gone Wild).mp4'),
    ('E:/xunleiyunpan/S01E26.Skorka.mkv', 'E:/data/Penguins/26 飞虎鲸来袭 (Skorca).mp4'),
    ('E:/xunleiyunpan/S01E25.Roger.Dodger.mkv', 'E:/data/Penguins/25 以柔克刚 (Roger Dodger).mp4'),
    ('E:/xunleiyunpan/S01E24.Misfortune.Cookie.mkv', 'E:/data/Penguins/23 霉运签饼 (Misfortune Cookie).mp4'),
    ('E:/xunleiyunpan/S01E23.Lemur.See.Lemur.Do.mkv', 'E:/data/Penguins/24 我爱小安安 (Lemur See,Lemur Do).mp4'),
    ('E:/xunleiyunpan/S01E22.Roomies.mkv', 'E:/data/Penguins/22 欢迎新室友 (Roomies).mp4'),
    ('E:/xunleiyunpan/S01E21.Mort.Unbound.mkv', 'E:/data/Penguins/21 猛男小毛 (Mort Unbound).mp4'),
    ('E:/xunleiyunpan/S01E20.Needle.Point.mkv', 'E:/data/Penguins/19 打针记 (Needle Point).mp4'),
    ('E:/xunleiyunpan/S01E19.Eclipsed.mkv', 'E:/data/Penguins/20 日全食 (Eclipsed).mp4'),
    ('E:/xunleiyunpan/S01E18.Miracle.On.Ice.mkv', 'E:/data/Penguins/18 冰上奇迹 (Miracle on Ice).mp4'),
    ('E:/xunleiyunpan/S01E17.Go.Fish.mkv', 'E:/data/Penguins/17 捕鱼记 (Go Fish).mp4'),
    ('E:/xunleiyunpan/S01E16.Popcorn.Panic.mkv', 'E:/data/Penguins/16 我爱爆米花(Popcorn Panic).mp4'),
    ('E:/xunleiyunpan/S01E15.Little.Zoo.Coupe.mkv', 'E:/data/Penguins/15 动物园赛车 (Little Zoo Coupe).mp4'),
    ('E:/xunleiyunpan/S01E14.All.Choked.Up.mkv', 'E:/data/Penguins/14 不吐不快 (All Choked Up).mp4'),
    ('E:/xunleiyunpan/S01E13.Kingdom.Come.mkv', 'E:/data/Penguins/13 接受王国 (Kingdom Come).mp4'),
    ('E:/xunleiyunpan/S01E12.The.Hidden.mkv', 'E:/data/Penguins/12 看不见的敌人 (The Hidden).mp4'),
    ('E:/xunleiyunpan/S01E11.Crown.Fools.mkv', 'E:/data/Penguins/11 我要王冠(Crown Fools).mp4'),
    ('E:/xunleiyunpan/S01E10.Tangled.in.the.Web.mkv', 'E:/data/Penguins/10 我要红 (Tangled in the Web).mp4'),
    ('E:/xunleiyunpan/S01E09.Two.Feet.High.and.Rising.mkv',
     'E:/data/Penguins/9 恋脚癖大作战 (Two.Feet.High.and.Rising).mp4'),
    ('E:/xunleiyunpan/S01E08.Penguiner.Takes.All.mkv', 'E:/data/Penguins/8 企鹅的胜利 (Penguiner Takes All).mp4'),
    ('E:/xunleiyunpan/S01E07.Assault.and.Batteries.mkv',
     'E:/data/Penguins/7 抢电池大作战 (Assault & Batteries).mp4'),
    ('E:/xunleiyunpan/S01E06.Paternal.Egg-Stinct.mkv', 'E:/data/Penguins/6 最佳奶爸 (Paternal Egg-Stinct).mp4'),
    ('E:/xunleiyunpan/S01E05.Happy.King.Julien.Day.mkv',
     'E:/data/Penguins/5 快乐国王节 (Happy King Julien Day).mp4'),
    ('E:/xunleiyunpan/S01E04.Operation.Plush.and.Cover.mkv',
     'E:/data/Penguins/4 抢救小毛 (Operation Plush & Cover).mp4'),
    ('E:/xunleiyunpan/S01E03.Haunted.Habitat.mkv', 'E:/data/Penguins/3 鬼哭神嚎 (Haunted Habitat).mp4'),
    ('E:/xunleiyunpan/S01E02.Launchtime.mkv', 'E:/data/Penguins/2 月球度假记 LaunchTime.mp4'),
    ('E:/xunleiyunpan/S01E01.Gone.in.a.Flash.mkv', 'E:/data/Penguins/1 我爱大毛_(Gone In A Flash).mp4')]

videos_season2 = [
    ('E:/xunleiyunpan/S02E64.Endangerous.Species.mkv', 'F:/penguins season 2/64 大宝盔 (The Helmet).mp4'),
    ('E:/xunleiyunpan/S02E62.Operation.Antarctica.mkv',
     'F:/penguins season 2/62 以暴制暴 (badger Pride).mp4'), ('E:/xunleiyunpan/S02E61.The.Big.STANK.mkv',
                                                              'F:/penguins season 2/61 天即可不泄露 (Field Tripped).mp4'),
    ('E:/xunleiyunpan/S02E60.Arch-Enemy.mkv', 'F:/penguins season 2/60 除虫大作战 (Stop Bugging Me).mp4'),
    ('E:/xunleiyunpan/S02E59.I.Know.Why.the.Caged.Bird.Gies.Insane.mkv',
     'F:/penguins season 2/59 水泥丛林历险记 (Concrete Jungle..).mp4'),
    ('E:/xunleiyunpan/S02E10.Mr.Tux.mkv', 'F:/penguins season 2/10 黑白一哥 (Mr.Tux).mp4'), (
        'E:/xunleiyunpan/S02E09.Operation.Cooties.mkv',
        'F:/penguins season 2/9 不要碰我 (Operation Cooties).mp4'),
    ('E:/xunleiyunpan/S02E08.Fit.to.Print.mkv', 'F:/penguins season 2/8 曝光危机 (Fit to Print).mp4'), (
        'E:/xunleiyunpan/S02E07.The.Lost.Treasure.of.the.Golden.Squirrel.mkv',
        'F:/penguins season 2/7 特别篇 黄金松鼠的神秘宝藏 (The Squire).mp4'), (
        'E:/xunleiyunpan/S02E06.Hard.Boiled.Eggy.mkv',
        'F:/penguins season 2/6 无敌小蛋 (Hard Boiled Eggy).mp4'), (
        'E:/xunleiyunpan/S02E05.Cant.Touch.This.mkv',
        "F:/penguins season 2/5 抢救绵羊 (Can't Touch This).mp4"), (
        'E:/xunleiyunpan/S02E04.In.the.Line.of.Doody.mkv',
        'F:/penguins season 2/4 鸽子复仇记 (In the line of Doody).mp4'),
    ('E:/xunleiyunpan/S02E03.Gator.Watch.mkv', 'F:/penguins season 2/3  鳄鱼出没 (Gator Watch).mp4'), (
        'E:/xunleiyunpan/S02E02.Its.About.Time.mkv',
        "F:/penguins season 2/2 三个卡哇伊 (It's about Time).mp4"), (
        'E:/xunleiyunpan/S02E01.The.Red.Squirrel.mkv',
        'F:/penguins season 2/1 传奇特务 (The Red Squirrel).mp4')]

videos_season3 = [(
    "F:/xunleiyunpan/S02E06.Hard.Boiled.Eggy.mkv",
    "E:/360MoveData/Users/MrB/Desktop/企鹅特工孵化鸭子，用训练作为胎教，结果鸭子一出生就成为特工@不正经的小酥肉.mp4")]


def main():
    if len(sys.argv) > 1:
        argument = sys.argv[1]
        print(f'接收到的参数值: {argument}')

        avg = None

        if len(sys.argv) > 2:
            avg = int(sys.argv[2])
            print(f"设定的匹配标准是{avg}")

        compare_size = None  # 跳帧的长度
        if len(sys.argv) > 3:
            compare_size = int(sys.argv[3])
            print(f"设定的匹配长度是{compare_size}（此配置项表示跳帧的长度，过长会导致程序缓慢。）")

        index = -int(argument)
        target = videos_season3[index]

        print(target)

        input('回车开始')

        runner: RunnerI = VideoAlignTaskMadajiasijiaImpl(video_a_path=target[0],
                                                         video_b_path=target[1], reasonable_avg=avg,
                                                         compare_size=compare_size)

        runner.run()

    else:
        print('未提供任何参数')


from moviepy.config import change_settings

change_settings({"IMAGEIO_FFMPEG_EXE": "e:/MrB/Downloads/ffmpeg-6.0/bin/ffmpeg.exe", "IMAGEIO_USE_GPU": True})
if __name__ == '__main__':
    main()
