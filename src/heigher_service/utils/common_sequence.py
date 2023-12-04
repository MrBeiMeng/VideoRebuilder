import typing

import numpy as np
from tqdm import tqdm

from src.heigher_service.utils.common import BLUtils
from src.service.video_iterator_interface import VideoIteratorI


class CSUtils:
    @staticmethod
    def find_all_common_sequence(iterator_a: VideoIteratorI, iterator_b: VideoIteratorI, common_size,
                                 is_equal: typing.Callable[[int], bool],
                                 crop_info_path):  # 保证A是长的

        # a迭代器，只需要迭代一次，而B迭代器需要迭代好多次

        arr_b = CSUtils._conv_iterator_to_arr(common_size, crop_info_path, iterator_b)

        len_a, len_b = iterator_a.get_total_f_num(), len(arr_b)
        max_map = {}  # b: [mx_arr]
        #               mx_arr = [][start_a,start_b,len,b,distance] (k 固定为1，b是直线和x轴的交点) # y = x + b => b = y-x
        dp = np.zeros((len_a + 1, len_b + 1), dtype=np.int_)

        tbar = tqdm(desc='计算匹配序列', unit='帧', total=len_a * len_b)
        found_equal_sequence_num = 0

        for i in range(1, len_a + 1):
            feature_a = BLUtils.get_cropped_feature(next(iterator_a), common_size=common_size,
                                                    crop_info_path=crop_info_path)
            for j in range(1, len_b + 1):
                distance = BLUtils.get_distance(feature_a, arr_b[j - 1])
                # 判断相等
                if is_equal(distance):
                    dp[i][j] = dp[i - 1][j - 1] + 1

                found_equal_sequence_num += CSUtils._handle_dp(distance, dp, i, j, max_map)
                # log
                tbar.update(1)
                found_frame_num, total_finding_frame_num = 0, len_b
                for val in max_map.values():
                    for items in val:
                        found_frame_num += items[2]
                tbar.set_postfix_str(
                    f'已匹配成功[{found_equal_sequence_num}]条')

        tbar.close()

        # for key, val in max_map.items():
        #     for items in val:
        #         print(iterator_a[items[0]:items[0] + items[2]])
        return max_map

    @staticmethod
    def _conv_iterator_to_arr(common_size, crop_info_path, iterator_b):
        tbar = tqdm(desc='获取视频关键帧序列', unit='帧', total=iterator_b.get_total_f_num())
        arr_b = []
        while True:
            try:
                feature_b = BLUtils.get_cropped_feature(next(iterator_b), common_size=common_size,
                                                        crop_info_path=crop_info_path)
                arr_b.append(feature_b)
                tbar.update(1)
            except StopIteration:
                break
        tbar.close()
        return arr_b

    @staticmethod
    def _handle_dp(distance, dp, i, j, max_map):
        # 判断是否是最大的就可以了对吧
        if dp[i][j] > 0:
            if (j - i) not in max_map:  # 初始化字典的key
                max_map[j - i] = []

            found = False

            max_arr = max_map[j - i]
            mx = dp[i][j]
            start_a, start_b = i - mx, j - mx
            for items in max_arr:  # abced    abbc
                if start_a == items[0] and start_b == items[1]:
                    items[2] = mx
                    items[4] = items[4] + distance
                    found = True

            if not found:
                max_map[j - i].append([start_a, start_b, mx, j - i, distance])
                return 1

        return 0

    @staticmethod
    def cover_interval(segments, interval):
        """
        Find the minimum number of segments to cover a given interval.

        :param segments: List of tuples representing the segments (start_b, end) start_a, start_b, equal_len, b, distance = tuple(items)
        :param interval: Tuple representing the target interval (iterator_b_start, iterator_b_end)
        :return: List of segments that cover the interval
        """
        # Sort the segments based on their starting point
        segments.sort(key=lambda x: x[1])

        # Initialize variables
        result = []
        current_end = interval[0]
        idx = 0
        n = len(segments)

        while current_end < interval[1] and idx < n:
            # Find the segment that covers the current end and reaches the farthest
            farthest_reach = current_end
            chosen_segment = None
            while idx < n and segments[idx][1] <= current_end:
                if (segments[idx][2] + segments[idx][1]) > farthest_reach:
                    farthest_reach = (segments[idx][2] + segments[idx][1])
                    chosen_segment = segments[idx]
                idx += 1

            # If no segment can extend the coverage, break the loop
            if chosen_segment is None:
                break

            # Update the current end and add the chosen segment to the result
            current_end = farthest_reach
            result.append(chosen_segment)

        # Check if the entire interval is covered
        # if current_end < interval[1]:
        #     return None  # The interval can't be fully covered

        return result
