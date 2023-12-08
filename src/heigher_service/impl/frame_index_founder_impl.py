import numpy as np

from src.heigher_service.frame_index_founder_interface import FrameIndexFounderI
from src.heigher_service.utils.multi_work_utils import MultiWorkUtilsFactory
from src.heigher_service.utils.util_interface.multi_work_interface import MultiWorkI


class FrameIndexFounderImpl(FrameIndexFounderI):
    """
    这个类负责从给定的视频或图片序列中找出与指定图片最相近的索引集合
    """

    def get_best_math_a_index_list(self, feature_b: np.ndarray, expect_num: int = 0, expect_distance: float = 0.0) -> \
            list[int]:

        possibly_a_starts = self.first_search(feature_b)

        # 接下来进行第二次查找
        possibly_a_starts_2 = self.second_search(feature_b, possibly_a_starts)

        # print(possibly_a_starts_2)

        # print('起点归一化')
        # final_possibly_a_starts = []
        # for p_a_s, distance in possibly_a_starts_2:
        #     new_p_a_s = p_a_s - p_a_s % 10
        #     if not final_possibly_a_starts.__contains__(new_p_a_s):
        #         final_possibly_a_starts.append(new_p_a_s)
        # print(f'剩余[{len(final_possibly_a_starts)}]个起点 [{final_possibly_a_starts}]')

        return [a_index for a_index, _ in possibly_a_starts_2]

    def second_search(self, feature_b, possibly_a_starts):
        MultiWorkUtilsFactory().process_utils.do_work('_second_search', (feature_b, possibly_a_starts))
        ten_flag_map = {}  # 以10帧为分界线保存 集合
        find_time = 0
        while True:
            try:
                (index, distance) = MultiWorkUtilsFactory().process_utils.get_result(0.1)
                find_time += 1

                if distance < 5:

                    ten_flag = index - index % 10
                    if ten_flag not in ten_flag_map:
                        ten_flag_map[ten_flag] = []

                    ten_flag_map[ten_flag].append((index, distance))

            except Exception:
                break

        found_result = []
        for pre_index_distances in ten_flag_map.values():
            pre_index_distances.sort(key=lambda x: x[1])
            found_result.append(pre_index_distances[0])

        found_result.sort(key=lambda x: x[1])

        found_result = found_result[:4] if len(found_result) >= 4 else found_result

        print(
            f'二次查找 [{len(found_result)}] 个 寻找[{find_time}]次 前五个最佳匹配{found_result}')

        return found_result

    def first_search(self, feature_b):
        MultiWorkUtilsFactory().process_utils.do_work('_first_search', feature_b)
        found_result = []
        possibly_a_starts = []
        find_time = 0
        while True:
            try:
                (index, distance) = MultiWorkUtilsFactory().process_utils.get_result(0.1)
                find_time += 1

                if distance < 10:
                    found_result.append((index, distance))
                    possibly_a_starts.append(index)
            except Exception:
                break
        found_result.sort(key=lambda x: x[1])
        print(
            f'\n初次查找 [{len(found_result)}] 个 寻找[{find_time}]次 前五个最佳匹配{found_result[:5] if len(found_result) > 5 else found_result}')
        return possibly_a_starts
