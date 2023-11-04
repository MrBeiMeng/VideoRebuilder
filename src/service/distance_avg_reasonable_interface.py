import abc
from typing import Tuple, List


class DistanceAvgReasonableI(metaclass=abc.ABCMeta):
    reasonable_avg: int

    @abc.abstractmethod
    def __init__(self, avg_size):
        ...

    @abc.abstractmethod
    def upd_reasonable_avg(self, avg: int): ...

    @abc.abstractmethod
    def add_index_tuple_and_distance(self, index_a: int, index_b: int, distance) -> bool: ...

    @abc.abstractmethod
    def avg_reasonable(self, stopping_flag: bool, op_reasonable_avg: int) -> bool: ...

    @abc.abstractmethod
    def pop_first_index_t(self) -> ((int, int), bool): ...

    @abc.abstractmethod
    def pop_all(self) -> list[tuple[int, int]]: ...

    @abc.abstractmethod
    def get_rb_list_and_b_index(self) -> (List[Tuple[int, int]], int): ...  # 获取合理序列，和第一个不合理的b索引
