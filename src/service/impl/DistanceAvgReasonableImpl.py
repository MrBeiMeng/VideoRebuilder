import math
from typing import List, Tuple

import numpy as np

from src.service.distance_avg_reasonable_interface import DistanceAvgReasonableI


class DistanceAvgReasonableImpl(DistanceAvgReasonableI):
    def __init__(self, avg_size=10, reasonable_avg=90):
        self.avg_size = avg_size
        self.index_list: List[Tuple[int, int]] = []
        self.distance_list: List = []
        self.reasonable_avg = reasonable_avg

        # self._sorted_distances = []  # 排序的distance

    def upd_reasonable_avg(self, avg: int):
        self.reasonable_avg += avg

    # def insert_sorted(self, distance):
    #     # 如果sorted_distances为空或新的distance大于最后一个元素，直接将其添加到列表末尾
    #     if not self._sorted_distances or distance >= self._sorted_distances[-1]:
    #         self._sorted_distances.append(distance)
    #     else:
    #         # 遍历sorted_distances找到正确的插入位置
    #         for i, existing_distance in enumerate(self._sorted_distances):
    #             if distance < existing_distance:
    #                 self._sorted_distances.insert(i, distance)
    #                 break  # 找到正确的位置并插入后，退出循环

    def add_index_tuple_and_distance(self, index_a: int, index_b: int, distance) -> bool:
        self.index_list.append((index_a, index_b))
        self.distance_list.append(distance)

        # 去掉一个最大值，去掉一个最小值 # !! 这里和下面的逻辑不同，这里不会受数量影响。是一个随时变化的合理性
        sorted_distances = sorted(self.distance_list)
        trimmed_distances = sorted_distances[1:-1]  # 去掉一个最大值，去掉一个最小值

        if len(trimmed_distances) == 0:
            return False
        reasonable = (np.mean(trimmed_distances)) <= self.reasonable_avg

        return reasonable

    def avg_reasonable(self, stopping_flag: bool) -> bool:

        if not stopping_flag:
            if len(self.index_list) < self.avg_size:  # avg_size 表示取平均的数量。不达到数量，或者stopping_flag = False 即为合理
                return True
        sorted_distances = sorted(self.distance_list)
        trimmed_distances = sorted_distances[1:-1]  # 去掉一个最大值，去掉一个最小值

        if len(trimmed_distances) == 0:
            return False
        avg = int(np.mean(trimmed_distances))
        reasonable = avg <= self.reasonable_avg

        if not reasonable:
            print(f"匹配不通过。avg={avg} !<= {self.reasonable_avg}")

        return reasonable

    def pop_first_index_t(self) -> ((int, int), bool):  # 长度够的话再弹出 (索引对)，长度够不够

        if len(self.index_list) > self.avg_size:
            self.distance_list.pop(0)  # 同步清空
            return self.index_list.pop(0), True
        else:
            if len(self.index_list) != 0:
                return self.index_list[0], False

            return (-1, -1), False

    def pop_all(self) -> list[tuple[int, int]]:  # 长度够的话再弹出 (索引对)，长度够不够

        tmp_result = []
        for element in self.index_list:
            tmp_result.append(element)

        self.index_list.clear()
        self.distance_list.clear()

        return tmp_result

    def get_rb_list_and_b_index(self) -> (List[Tuple[int, int]], int):
        for i, distance in enumerate(self.distance_list):
            # 这里假设当distance大于reasonable_avg时，序列开始变得不合理
            if distance >= self.reasonable_avg:
                return self.index_list[:i], i  # 返回合理的序列和第一个不合理的b_index
        return self.index_list, len(self.index_list)  # 如果所有距离都合理，返回全部序列和序列长度
