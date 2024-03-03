import datetime
import os.path

import cv2
from tqdm import tqdm

from src.heigher_service.utils.common import BLUtils
from src.heigher_service.utils.frame_cut_util import FrameCutUtilXiGua
from src.service.impl.video_iterator_impl import VideoIteratorImpl

from paddleocr import PaddleOCR, draw_ocr
import tkinter


class Recognition:
    def __init__(self):
        # Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
        # 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
        self.ocr = PaddleOCR(use_angle_cls=True,
                             lang="ch")  # need to run only once to download and load model into memory

    def text_recognition(self, frame):

        result = self.ocr.ocr(frame, cls=True)
        result_text = []
        for idx in range(len(result)):
            res = result[idx]
            if res is None:
                continue
            for line in res:
                result_text.append(f'{line[-1][0]}')
        return str.join('', result_text)

    @staticmethod
    def resize_image(image, target_width=1080):
        # 获取图像的原始宽度和高度
        original_width, original_height = image.shape[1], image.shape[0]

        # 计算新的高度，以保持宽高比不变
        new_height = int((target_width / original_width) * original_height)

        # 使用cv2.resize放大图像
        resized_image = cv2.resize(image, (target_width, new_height), interpolation=cv2.INTER_LINEAR)

        return resized_image


def get_subtitle_list_2():
    return [('胎教到底有多重要？', 0, 1458.0078125),
            ('这是一只企鹅孵化的鸭子', 1458.0078125, 3291.015625),
            ('瞒天过海兄弟们', 3458.0078125, 5458.0078125),
            ('在企鹅胎教的影响下', 6374.0234375, 7791.015625),
            ('小蛋一出生就进入了叛逆期', 7791.015625, 9708.0078125),
            ('不仅对周围的一切暴力相向', 9708.0078125, 11749.0234375),
            ('还觉得鸭妈妈的劝阻', 11749.0234375, 13208.0078125),
            ('是在恶意打压他', 13208.0078125, 14416.015625),
            ('到底是谁在指示你老妈', 14416.015625, 16666.015625),
            ('老大见状抱住了他', 16791.015625, 18166.015625),
            ('并向鸭妈妈承诺', 18166.015625, 19249.0234375),
            ('会让小蛋变成乖小子', 19249.0234375, 20874.0234375),
            ('可要知道', 20874.0234375, 21582.03125),
            ('企鹅的身份是特工', 21582.03125, 22957.03125),
            ('他们的日常危险无比', 22957.03125, 24541.015625),
            ('只是简单调个水温', 24541.015625, 25832.03125),
            ('就要过五关斩六将', 25832.03125, 27166.015625),
            ('那只是为了调整一下', 30457.03125, 31874.0234375),
            ('我们饮用水的水温而已', 31999.0234375, 33249.0234375),
            ('因为菜鸟鸟嘴过敏', 33249.0234375, 34749.0234375),
            ('那么没面子的事情你也说', 35707.03125, 37457.03125),
            ('然而在看见企鹅执行任务之后', 37582.03125, 39541.015625),
            ('小蛋非但没有被吓退', 39541.015625, 40999.0234375),
            ('反而抢走了老大的扳手', 40999.0234375, 42582.03125),
            ('长官任务再次成功更快', 46707.03125, 50457.03125),
            ('虽然小蛋身手敏捷', 50457.03125, 51874.0234375),
            ('是当特工的好料子', 51874.0234375, 53332.03125),
            ('但由于他年纪还小', 53332.03125, 54790.0390625),
            ('老大就劝他安分一点', 54790.0390625, 56249.0234375),
            ('可小蛋却说', 56249.0234375, 57165.0390625),
            ('可以给我炸药吗?', 57207.03125, 58415.0390625),
            ('好的', 58582.03125, 59040.0390625),
            ('不行', 60207.03125, 60624.0234375),
            ('危急时刻老大抢走了炸药', 60624.0234375, 62457.03125),
            ('然后对小蛋一通训斤', 62457.03125, 63957.03125),
            ('不过正所谓初生牛续不怕虎', 63957.03125, 66040.0390625),
            ('小蛋执着地认为', 66040.0390625, 67165.0390625),
            ('自己是天生的特工', 67165.0390625, 68540.0390625),
            ('好在这时老大发现了卡片', 68540.0390625, 70372.96549479166),
            ('公共交通卡', 70497.96549479166, 71665.0390625),
            ('是证书', 72082.03125, 73040.0390625),
            ('正式的企鹅特种兵证书', 73540.0390625, 75582.03125),
            ('不不我确定那是交通卡', 75997.96549479166, 77872.96549479166),
            ('上面有标志的', 77872.96549479166, 79332.03125),
            ('知道老大是想欺骗小蛋', 79372.96549479166, 80997.96549479166),
            ('凉快和卡哇伊立马配合', 80997.96549479166, 82665.0390625),
            ('可惜菜鸟还是', 82665.0390625, 83955.97330729166),
            ('真的？我怎么没...', 84040.0390625, 85580.97330729166),
            ('啊对了', 86122.96549479166, 87665.0390625),
            ('企鹅特种兵的证书很重要的', 87872.96549479166, 91122.96549479166),
            ('老大我领会你的精神了', 91290.0390625, 92915.0390625),
            ('吃了四个大比兜才反应过来', 93080.97330729166, 94705.97330729166),
            ('不得不说菜鸟是真的反应迟钝', 94705.97330729166, 96915.0390625),
            ('成功骗过小蛋后', 96915.0390625, 97915.0390625),
            ('老大告诉他', 97915.0390625, 98705.97330729166),
            ('必须打倒所有动物才能拿到放引', 98705.97330729166, 100997.96549479166),
            ('本以为这样就能让小蛋退缩', 100997.96549479166, 102747.96549479166),
            ('谁知没过多久', 102747.96549479166, 103665.0390625),
            ('他们就听到了一声惨叫', 103665.0390625, 105247.96549479166),
            ('是大毛突然遭到偷袭', 105247.96549479166, 106788.98111979166),
            ('导致朱利安失去帮手', 106788.98111979166, 108122.96549479166),
            ('只能自己贴上眼膜', 108122.96549479166, 109580.97330729166),
            ('小毛替我哭', 109580.97330729166, 110997.96549479166),
            ('我眼睛敷小黄瓜', 111205.97330729166, 112622.96549479166),
            ('敷得好累', 112622.96549479166, 113538.98111979166),
            ('哦老天我的眼膜好刺眼', 117038.98111979166, 119955.97330729166),
            ('洋葱敷眼我敬你是条汉子', 119955.97330729166, 121955.97330729166),
            ('然而就在这时', 121955.97330729166, 122872.96549479166),
            ('小蛋从天而降', 122872.96549479166, 124038.98111979166),
            ('好痛', 125330.97330729166, 126080.97330729166),
            ('怎么？', 126080.97330729166, 126413.98111979166),
            ('小毛你有痛觉了？', 126413.98111979166, 127371.98893229166),
            ('为了拿到特工证书', 127371.98893229166, 128580.97330729166),
            ('小蛋打算在日落前打败所有动物', 128580.97330729166, 130955.97330729166),
            ('于是他不顾老大的阻拦', 130955.97330729166, 132496.98893229166),
            ('径直闯进了霸哥的家', 132496.98893229166, 134038.98111979166),
            ('要知道大象是陆地小上最大的运性', 134038.98111979166, 136413.98111979166),
            ('就算老大出马都很难取胜', 136413.98111979166, 138246.98893229166),
            ('所以他们认为', 138246.98893229166, 139330.97330729166),
            ('小蛋一定会知难而退', 139330.97330729166, 140871.98893229166),
            ('可就在老大说着', 140871.98893229166, 141871.98893229166),
            ('该如何对付霸哥时', 141871.98893229166, 143413.98111979166),
            ('小蛋居然在后面', 143413.98111979166, 144538.98111979166),
            ('完美复刻了战斗', 144538.98111979166, 145663.98111979166),
            ('可那是招牌必杀技', 148496.98893229166, 150579.99674479166),
            ('我的必杀技', 151079.99674479166, 152204.99674479166),
            ('这时卡哇伊分析道', 152204.99674479166, 153496.98893229166),
            ('在小蛋还是蛋的时候', 153496.98893229166, 154954.99674479166),
            ('就从他们的训练中吸取经验', 154954.99674479166, 156871.98893229166),
            ('变成了四人的合体', 156871.98893229166, 158204.99674479166),
            ('事实证明卡哇伊的推测没错', 158204.99674479166, 159954.99674479166),
            ('小蛋不仅能用物理知识设置陷', 159954.99674479166, 162121.98893229166),
            ('轻松打败了大猩猩', 162121.98893229166, 163246.98893229166),
            ('还继承了凉快的神经质', 163246.98893229166, 164829.99674479166),
            ('让拳王袋鼠只能吃', 164829.99674479166, 166371.98893229166),
            ('最后又模仿菜鸟卖萌', 166371.98893229166, 167788.00455729166),
            ('将玛琳打倒在地', 167788.00455729166, 169079.99674479166),
            ('他居然装出人见人爱的可爱模格', 169079.99674479166, 171538.00455729166),
            ('跟菜鸟一模一样', 171621.98893229166, 172996.98893229166),
            ('装可爱？', 173288.00455729166, 174079.99674479166),
            ('我本来就很可爱啊', 174163.00455729166, 175538.00455729166),
            ('对了对了小可爱', 175579.99674479166, 177621.98893229166),
            ('很快动物都被打败', 177621.98893229166, 179329.99674479166),
            ('其中包括了老大四人', 179329.99674479166, 180913.00455729166),
            ('在这诺大的动物园里', 180913.00455729166, 182121.98893229166),
            ('就只剩朱利安一根独苗', 182121.98893229166, 183704.99674479166),
            ('没办法企鹅只能找他求助', 183704.99674479166, 185704.99674479166),
            ('可就在他们说话之际', 185704.99674479166, 187079.99674479166),
            ('小蛋找到了这里', 187079.99674479166, 188288.00455729166),
            ('并出手摆倒了企鹅', 188288.00455729166, 189663.00455729166),
            ('望着小蛋和朱利安的战斗', 189663.00455729166, 191079.99674479166),
            ('老大突然感到欣慰', 191079.99674479166, 192371.01236979166),
            ('那只鸭子会变成超猛的企鹅5', 192454.99674479166, 195204.99674479166),
            ('什么？', 195871.01236979166, 196329.99674479166),
            ('我的小朱朱想要当一只企鹅？', 196663.00455729166, 199704.99674479166),
            ('为了不让小蛋变成企鹅', 199704.99674479166, 201079.99674479166),
            ('朱利安打开了收音机', 201079.99674479166, 202538.00455729166),
            ('并跟着音乐舞动身体', 202538.00455729166, 203788.00455729166),
            ('成功躲过了所有攻击', 203788.00455729166, 205246.01236979166),
            ('最后小蛋累倒地', 205246.01236979166, 206913.00455729166),
            ('你是这个世上最神勇无敌的动物', 207079.99674479166, 212288.00455729166),
            ('而你可以是第二神勇无敌的', 212788.00455729166, 216079.02018229166),
            ('在朱利安的教育下', 216079.02018229166, 217204.02018229166),
            ('小蛋不再是企鹅小蛋', 217204.02018229166, 218621.01236979166),
            ('而是变成了二号朱利安', 218621.01236979166, 220246.01236979166),
            ('非常感谢你们这些呆呆小企鹅', 220246.01236979166, 223413.00455729166)]


def get_subtitle_list():
    # 先迭代完整的视频，切割出要识别得部分，去重保存（注意要保存时间戳）就可以了吧
    b_path = 'E:/data/202312071923.mp4'
    crop_info_path = '../tests/crop_info_xi_gua_zi_mu.json'
    iterator = VideoIteratorImpl(b_path)
    tbar = tqdm(desc='正在识别视频字幕', unit='帧', total=iterator.get_total_f_num())
    recognition_utils = Recognition()
    last_uncolor_feature = None
    last_text = None
    subtitle_text_list = []
    while True:
        try:
            frame = next(iterator)

            frame = Recognition.resize_image(frame, 720)
            underline_subtitle_on_frame(crop_info_path, frame)
            cv2.imshow('frame', frame)
            cv2.waitKey(1)

            feature = BLUtils.crop_feature(frame, crop_info_path)

            uncolor_feature = cv2.cvtColor(feature, cv2.COLOR_BGR2GRAY)

            if last_uncolor_feature is None or BLUtils.get_distance(last_uncolor_feature, uncolor_feature) > 3:
                msec_start = iterator.cap.get(cv2.CAP_PROP_POS_MSEC)  # 时间戳

                # 将上次识别结果进行保存
                if last_text is not None:
                    real_text, real_msec_start = last_text
                    last_text = (real_text, real_msec_start, msec_start)
                    subtitle_text_list.append(last_text)
                    last_text = None

                text = recognition_utils.text_recognition(feature)

                if text == '':
                    abandon = True
                else:
                    # abandon = user_abandon()
                    abandon = False

                if not abandon:
                    # 保存这一次识别结果
                    last_text = (text, msec_start)

                last_uncolor_feature = uncolor_feature

            tbar.update(1)
            tbar.set_postfix_str(
                f'保存数量[{len(subtitle_text_list)}] 识别结果: {subtitle_text_list[-1] if len(subtitle_text_list) > 0 else ""}\t{"丢弃" if abandon else "保留"}')
        except StopIteration:
            break
    iterator.release()
    tbar.close()
    return subtitle_text_list


def user_abandon():
    abandon = False
    char = input('保留[enter/1] 丢弃[2/\\]')
    if char == '\n' or char == '1':
        abandon = False
    elif char == '2' or char == '\\':
        abandon = True
    return abandon


def underline_subtitle_on_frame(crop_info_path, frame):
    crop_info = FrameCutUtilXiGua(crop_info_path).crop_info
    height, width = frame.shape[:2]
    x_start = int(crop_info['x_ratio_start'] * width)
    y_start = int(crop_info['y_ratio_start'] * height)
    x_end = int(crop_info['x_ratio_end'] * width)
    y_end = int(crop_info['y_ratio_end'] * height)
    cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)


def save_str_to_files(final_rst_str, final_text_str, save_dir):
    rst_file_path = 'rst_subtitle.srt'
    txt_file_path = 'rst_subtitle.txt'
    final_rst_file_path = BLUtils.get_unique_filename(os.path.join(save_dir, rst_file_path))
    final_txt_file_path = BLUtils.get_unique_filename(os.path.join(save_dir, txt_file_path))
    with open(final_rst_file_path, 'w', encoding='utf-16') as rst_file:
        rst_file.write(final_rst_str)
        print(f'保存至 >> {final_rst_file_path}')
    with open(final_txt_file_path, 'w', encoding='utf-16') as txt_file:
        txt_file.write(final_text_str)
        print(f'保存至 >> {final_txt_file_path}')


def generate_final_str(subtitle_text_list):
    final_rst_str = ""
    final_text_str = ""
    count = 0
    for real_text, real_msec_start, real_msec_end in subtitle_text_list:
        start_time_str = get_time_str(real_msec_start)
        end_time_str = get_time_str(real_msec_end)

        temp_rst = f"""{count}
{start_time_str} --> {end_time_str}
{real_text}

"""

        final_rst_str += temp_rst
        final_text_str += f"{real_text}\n"

        count += 1
    return final_rst_str, final_text_str


def get_time_str(real_msec_start):
    real_msec_start = int(real_msec_start)
    # 毫秒转化为时分秒
    msec = real_msec_start % 1000
    sec = int(real_msec_start / 1000) % 60
    minute = int(real_msec_start / (60 * 1000)) % 60
    hour = int(real_msec_start / (60 * 60 * 1000))
    # start_time = datetime.datetime.utcfromtimestamp(real_msec_start)
    # start_time_str = start_time.strftime("%H:%M:%S,%f")
    start_time_str = f"{hour}:{minute}:{sec},{msec}"
    return start_time_str


def main():
    subtitle_text_list = get_subtitle_list_2()

    """
    0
    00:00:01,460 --> 00:00:16,020
    No wanna be hardests of storytelling is establishing the world to create thes the rules set up the narrative.
    """

    final_rst_str, final_text_str = generate_final_str(subtitle_text_list)

    print(final_rst_str)
    print(final_text_str)

    save_dir = '../static/result/rst/'
    save_str_to_files(final_rst_str, final_text_str, save_dir)


if __name__ == '__main__':
    main()
