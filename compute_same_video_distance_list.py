from src.heigher_service.impl.video_verify.same_video_ssim_calculate import SameVideoSsimCalculate
from src.heigher_service.runner_interface import RunnerI

if __name__ == '__main__':
    videos = [('E:/data/Penguins/9 恋脚癖大作战 (Two.Feet.High.and.Rising).mp4',
               'E:/360MoveData/Users/MrB/Desktop/penguins_finally/9 恋脚癖大作战 (Two Feet High and Right)(1).mp4'), (
                  'E:/data/Penguins/8 企鹅的胜利 (Penguiner Takes All).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/8 企鹅的胜利 (Penguiner Takes All)(1).mp4'), (
                  'E:/data/Penguins/7 抢电池大作战 (Assault & Batteries).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/7 抢电池大作战 (Assault & Batteries)(1).mp4'), (
                  'E:/data/Penguins/6 最佳奶爸 (Paternal Egg-Stinct).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/6 最佳奶爸 (Paternal Egg-Stinct).mp4'), (
                  'E:/data/Penguins/5 快乐国王节 (Happy King Julien Day).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/5 快乐国王节 (Happy King Julien Day)(1).mp4'), (
                  'E:/data/Penguins/47 我最可爱 (The Penguin Stays In the..).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/47 我最可爱 (The Penguin Stays In the..).mp4'), (
                  'E:/data/Penguins/46 英雄爱美 (The Falcon and the Sno).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/46 英雄爱美 (The Falcon and the Sno).mp4'), (
                  'E:/data/Penguins/45 我爱绿绿 (Jiggles).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/45 我爱绿绿 (Jiggles).mp4'),
              ('E:/data/Penguins/44 大战怪怪鱼 (SnakeHead).mp4', ''),
              ('E:/data/Penguins/43 倒闭危机 (Zoo Tube).mp4', ''), (
                  'E:/data/Penguins/42 乱点鸳鸯谱 (Otter Things Have Ha...).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/42 乱点鸳鸯谱 (Otter Things Have Ha...).mp4'), (
                  'E:/data/Penguins/41 大象复仇记 (An Elephant Never Fo..).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/41 大象复仇记 (An Elephant Never Fo..).mp4'), (
                  'E:/data/Penguins/40 我的好兄弟 (Over Phil).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/40 我的好兄弟 (Over Phil)(1).mp4'), (
                  'E:/data/Penguins/4 抢救小毛 (Operation Plush & Cover).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/4 抢救小毛 (Operation Plush & Cover)(1).mp4'), (
                  'E:/data/Penguins/39 我要当女生 (Miss Understanding).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/39 我要当女生 (Miss Understanding).mp4'), (
                  'E:/data/Penguins/38 不要摸我 (Untouchable).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/38 不要摸我 (Untouchable)(1).mp4'), (
                  'E:/data/Penguins/37 不能没有你 (All King, No Kingdom).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/37 不能没有你 (All King, No Kingdom).mp4'), (
                  'E:/data/Penguins/36 防蜂大作战 (Sting Operation).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/36 防蜂大作战 (Sting Operation).mp4'),
              ('E:/data/Penguins/35 僵尸企鹅.mp4', 'E:/360MoveData/Users/MrB/Desktop/penguins_finally/35 僵尸企鹅.mp4'),
              ('E:/data/Penguins/34 天下大乱 (Jungle Law).mp4',
               'E:/360MoveData/Users/MrB/Desktop/penguins_finally/34 天下大乱 (Jungle Law)(1).mp4'), (
                  'E:/data/Penguins/33 武功尽失 (Out of the Groove).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/33 武功尽失 (Out of the Groove).mp4'), (
                  'E:/data/Penguins/32 侠盗阿奇 (Mask Of The Raccoon).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/32 侠盗阿奇 (Mask Of The Raccoon)(1).mp4'), (
                  'E:/data/Penguins/31 好心有好报 (What Goes Around).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/31 好心有好报 (What Goes Around).mp4'), (
                  'E:/data/Penguins/30 紧盯不放 (Tagged).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/30 紧盯不放 (Tagged).mp4'), (
                  'E:/data/Penguins/3 鬼哭神嚎 (Haunted Habitat).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/3 鬼哭神嚎 (Haunted Habitat)(1).mp4'), (
                  'E:/data/Penguins/29 恋爱绝招 (Monkey Love).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/29 恋爱绝招 (Monkey Love)(1).mp4'), (
                  "E:/data/Penguins/28 救猫记 (Cat's Cradle).mp4",
                  "E:/360MoveData/Users/MrB/Desktop/penguins_finally/28 救猫记 (Cat's Cradle)(1).mp4"), (
                  'E:/data/Penguins/27 野性大发 (Otter Gone Wild).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/27 野性大发 (Otter Gone Wild).mp4'), (
                  'E:/data/Penguins/26 飞虎鲸来袭 (Skorca).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/26 飞虎鲸来袭 (Skorca).mp4'), (
                  'E:/data/Penguins/25 以柔克刚 (Roger Dodger).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/25 以柔克刚 (Roger Dodger).mp4'), (
                  'E:/data/Penguins/24 我爱小安安 (Lemur See,Lemur Do).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/24 我爱小安安 (Lemur See,Lemur Do)(1).mp4'), (
                  'E:/data/Penguins/23 霉运签饼 (Misfortune Cookie).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/23 霉运签饼 (Misfortune Cookie)(1).mp4'), (
                  'E:/data/Penguins/22 欢迎新室友 (Roomies).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/22 欢迎新室友 (Roomies)(1).mp4'), (
                  'E:/data/Penguins/21 猛男小毛 (Mort Unbound).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/21 猛男小毛 (Mort Unbound).mp4'), (
                  'E:/data/Penguins/20 日全食 (Eclipsed).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/20 日全食 (Eclipsed)(1).mp4'), (
                  'E:/data/Penguins/2 月球度假记 LaunchTime.mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/2 月球度假记 LaunchTime(1).mp4'),
              ('E:/data/Penguins/19 打针记 (Needle Point).mp4', ''), (
                  'E:/data/Penguins/18 冰上奇迹 (Miracle on Ice).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/18 冰上奇迹 (Miracle on Ice).mp4'), (
                  'E:/data/Penguins/17 捕鱼记 (Go Fish).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/17 捕鱼记 (Go Fish)(1).mp4'), (
                  'E:/data/Penguins/16 我爱爆米花(Popcorn Panic).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/16 我爱爆米花(Popcorn Panic)(1).mp4'), (
                  'E:/data/Penguins/15 动物园赛车 (Little Zoo Coupe).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/15 动物园赛车 (Little Zoo Coupe)(1).mp4'), (
                  'E:/data/Penguins/14 不吐不快 (All Choked Up).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/14 不吐不快 (All Choked Up)(1).mp4'), (
                  'E:/data/Penguins/13 接受王国 (Kingdom Come).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/13 接受王国 (Kingdom Come).mp4'),
              ('E:/data/Penguins/12 看不见的敌人 (The Hidden).mp4', ''), (
                  'E:/data/Penguins/11 我要王冠(Crown Fools).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/11 我要王冠(Crown Fools)(1).mp4'), (
                  'E:/data/Penguins/10 我要红 (Tangled in the Web).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/10 我要红 (Tangled in the Web)(1).mp4'), (
                  'E:/data/Penguins/1 我爱大毛_(Gone In A Flash).mp4',
                  'E:/360MoveData/Users/MrB/Desktop/penguins_finally/1 我爱大毛 Gone In A Flash(1).mp4')]

    runner: RunnerI = SameVideoSsimCalculate(videos)

    runner.run()
