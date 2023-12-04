import cv2
from tqdm import tqdm

from src.entity.entitys import KeyFrame
from src.heigher_service.impl.two_p_fast_dtw_orb_impl import TwoPFastDtwOrbImpl
from src.heigher_service.impl.two_p_fast_dtw_sift_impl import TwoPFastDtwSiftImpl
from src.heigher_service.runner_interface import RunnerI
from src.heigher_service.utils.common import BLUtils
from src.heigher_service.utils.common_sequence import CSUtils
from src.heigher_service.utils.frame_cut_util import FrameCutUtilXiGua
from src.service.impl.video_creator_impl import VideoCreatorImpl
from src.service.impl.video_iterator_impl import VideoIteratorPrefixImpl, VideoIteratorImpl
from src.service.impl.video_key_frames_impl import VideoKeyFramesImpl
from src.service.video_iterator_interface import VideoIteratorI
from src.service.video_key_frames_interface import VideoKeyFramesI


class VideoRebuildFindInAImpl(RunnerI):

    def __init__(self, dst_path: str, target_path: str, output_path=None):
        self.dst_path = dst_path
        self.target_path = target_path

        if output_path is not None:
            self.output_path = output_path
        else:
            self.output_path = BLUtils.get_unique_filename(self.target_path)

        self.crop_info_path = 'static/crop_info_xi_gua.json'

        # self.video_creator = self._get_video_creator()

    def run(self):

        # 获取两个视频的最小公共 size
        common_size = BLUtils.get_common_size(self.dst_path, self.target_path)
        print(f'计算common_size = [{common_size}]')

        iterator_b = VideoIteratorImpl(self.target_path)
        tbar = tqdm(desc='整体进度', unit='帧', total=iterator_b.get_total_f_num())
        total_distance = 0

        # 直接拿B的帧去A中寻找，第一步找到多个可能值，第二步从这些可能值中找到最长的，保存下来。从这个点继续向后匹配
        while True:
            try:
                frame_b = next(iterator_b)
                feature_b = BLUtils.get_cropped_feature(frame_b, common_size, self.crop_info_path)
            except StopIteration:
                break

            # 第一步
            possibly_a_starts = self.find_possibly_a_starts(common_size, feature_b)

            # 第二步，寻找最长的正确匹配
            # 2.1 从多个起点处获得多个迭代器以及匹配好的长度,不要忘了释放资源
            working_a_iterators = self._generate_working_a_iterators(common_size, iterator_b, possibly_a_starts)

            # 2.2 筛选出最合理的a迭代器
            best_a_iterator, longest_len, distance = self._get_best_a_iterator(working_a_iterators)

            # --- 可以在这类保存
            iterator_b.set_current_index(iterator_b.get_current_index() + longest_len)
            # ---<

            best_a_iterator.release()

            # log
            tbar.update(longest_len)
            total_distance += distance
            tbar.set_postfix_str(
                f'整体差异值[total:{int(total_distance)} pre:{int(total_distance / iterator_b.get_current_index())}]')
        tbar.close()
        iterator_b.release()

    def _get_best_a_iterator(self, working_a_iterators):
        working_a_iterators.sort(key=lambda x: x[1], reverse=True)  # 由大到小排序
        best_a_iterator, longest_len, total_distance = working_a_iterators[0]

        for item in working_a_iterators:
            temp_w_a_iterator, long, _ = item
            if long != longest_len:
                temp_w_a_iterator.release()
        working_a_iterators.clear()
        print(
            f'最长成功匹配长度为[{longest_len}],distance[total:{total_distance}/pre:{int(total_distance / longest_len)}]')
        return best_a_iterator, longest_len, total_distance

    def _generate_working_a_iterators(self, common_size, iterator_b, possibly_a_starts):
        print('即将从每个大致起点向下迭代寻找最佳起点')
        working_a_iterators = []  # (iter,len,total_distance)
        for p_a_s in possibly_a_starts:
            # 这是的a起点为 p_a_s b起点为fb.current_index
            temp_iterator_a, temp_iterator_b = VideoIteratorImpl(self.dst_path), VideoIteratorImpl(self.target_path)
            temp_iterator_a.set_current_index(p_a_s)
            temp_iterator_b.set_current_index(iterator_b.get_current_index())

            # 逐帧比较两个迭代器，遇到第一个合理的值之后，从十个中选一个最合理的再向后匹配
            temp_frame_b = next(temp_iterator_b)
            temp_feature_b = BLUtils.get_cropped_feature(temp_frame_b, common_size, self.crop_info_path)

            # 寻找最合理的A起点
            self._set_temp_a_iterator_index_to_best_compare(common_size, temp_feature_b, temp_iterator_a)

            temp_len = 1
            temp_distance = 0

            # 这一帧B已经比对过了
            while True:
                try:
                    temp_frame_a = next(temp_iterator_a)
                    temp_feature_a = BLUtils.get_cropped_feature(temp_frame_a, common_size, self.crop_info_path)
                    temp_frame_b = next(temp_iterator_b)
                    temp_feature_b = BLUtils.get_cropped_feature(temp_frame_b, common_size, self.crop_info_path)
                except StopIteration:
                    break

                distance = BLUtils.get_distance(temp_feature_a, temp_feature_b)
                if not distance < 18:
                    break

                temp_len += 1
                temp_distance += distance

            working_a_iterators.append((temp_iterator_a, temp_len, temp_distance))
            temp_iterator_b.release()
        print(f'生成迭代器数量:[{len(working_a_iterators)}]')
        return working_a_iterators

    def _set_temp_a_iterator_index_to_best_compare(self, common_size, temp_feature_b, temp_iterator_a):
        print('寻找最合理的A起点')
        short_a_start_list = []  # 候选a起点列表
        found = False
        while True:
            try:
                temp_frame_a = next(temp_iterator_a)
                temp_feature_a = BLUtils.get_cropped_feature(temp_frame_a, common_size, self.crop_info_path)
            except StopIteration:
                break

            distance = BLUtils.get_distance(temp_feature_a, temp_feature_b)
            if not distance < 20 and not found:
                continue

            found = True
            short_a_start_list.append((temp_iterator_a.get_current_index(), distance))

            if len(short_a_start_list) >= 10:
                short_a_start_list.sort(key=lambda x: x[1])  # 由小到大排序
                # print('起点差异值数组', short_a_start_list)

                # 选择差异值最小的点作为起点
                final_a_start, min_distance = short_a_start_list[0]
                temp_iterator_a.set_current_index(final_a_start)
                print(f'最小差异值[{min_distance}]')
                break

    def find_possibly_a_starts(self, common_size, feature_b):
        iterator_a = VideoIteratorImpl(self.dst_path)

        tbar = tqdm(desc='寻找可能的A起点', unit='帧', total=iterator_a.get_total_f_num())

        possibly_a_starts = []
        min_distance = 999
        # 第一步，寻找所有可能的起点
        while True:
            try:
                frame_a = next(iterator_a)
                feature_a = BLUtils.get_cropped_feature(frame_a, common_size, self.crop_info_path)

                tbar.update(1)
            except StopIteration:
                break
            distance = BLUtils.get_distance(feature_a, feature_b)
            if distance < 20:
                if distance < min_distance:
                    min_distance = distance
                possibly_a_starts.append(iterator_a.get_current_index())
                tbar.set_postfix_str(
                    f'找到了[{len(possibly_a_starts)}]个起点，当前起点差异值[{int(distance)}]，最小差异值[{int(min_distance)}]')

        tbar.close()
        # 起点归一化
        print('起点归一化')
        final_possibly_a_starts = []
        for p_a_s in possibly_a_starts:
            new_p_a_s = p_a_s - p_a_s % 10
            if not final_possibly_a_starts.__contains__(new_p_a_s):
                final_possibly_a_starts.append(new_p_a_s)
        print(f'剩余[{len(final_possibly_a_starts)}]个起点')

        iterator_a.release()
        return final_possibly_a_starts

    def _get_video_creator(self):
        fps_a, (a_w, a_h) = VideoIteratorImpl(self.dst_path).get_video_info()
        print(f"A info {fps_a},({a_w},{a_h})")
        fps_b, (b_w, b_h) = VideoIteratorImpl(self.target_path).get_video_info()
        print(f"B info {fps_b},({b_w},{b_h})")

        # 使用高画质，算法原因只能使用低帧率
        output_path = self.output_path
        output_fps = fps_b

        size = (a_w, a_h) if a_w * a_h > b_w * b_h else (b_w, b_h)
        output_size = size

        print(f"output info {output_fps},{output_size}")

        return VideoCreatorImpl(output_path, output_fps, output_size)
