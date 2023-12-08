import multiprocessing
from multiprocessing import Queue, Manager

import numpy as np

from src.heigher_service.utils.util_interface.multi_work_interface import MultiWorkI
from src.heigher_service.utils.workers.bl_process_worker import BlProcessWorker
from src.service.impl.video_iterator_impl import VideoIteratorImpl


class MultiWorkUtilsFactory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.process_utils = MultiWorkUtils(5)
            print("inited model")
        return cls._instance

    def get_multi_work_utils(self):
        return self.process_utils


class MultiWorkUtils(MultiWorkI):
    """
    这将是一个全局的多进程任务处理器，使用前，在本类中注册对应的方法，再通过do_work得形式,交由全局得workers去处理
    这个类需要维护指定数量得进程
    """

    def __init__(self, worker_num=5):
        """
        指定worker的数量，这个数量要低于cpu核心数量，并且，当前进程也算一个进程。
        ！！！过高的进程数量可能会导致程序卡死！！！
        :param worker_num:
        """

        self.worker_num = worker_num

        # self.worker_list, self.input_queues, self.output_q = self.generate(worker_num)

        self.worker_list = []
        self.input_queues = []
        # manager = Manager()
        self.output_q = Queue()

        for i in range(worker_num):
            name = f'worker-{i}'
            input_q = Queue()
            worker = BlProcessWorker(name=name, input_q=input_q, output_q=self.output_q)
            worker.start()

            self.worker_list.append(worker)
            self.input_queues.append(input_q)

        self.total_frames = 0

        print("inited multiprocess worker")

    @staticmethod
    def generate(worker_num=5):
        worker_list = []
        input_queues = []
        output_q = Queue()

        for i in range(worker_num - 1):
            input_q, worker = MultiWorkUtils._generate_worker(i, output_q)

            worker_list.append(worker)
            input_queues.append(input_q)

        return worker_list, input_queues, output_q

    @staticmethod
    def _generate_worker(i, output_q: Queue):
        name = f'worker-{i}'
        input_q = Queue()
        worker = BlProcessWorker(name=name, input_q=input_q, output_q=output_q)
        worker.start()

        return input_q, worker

    def get_result(self, time_out: int = 5) -> object:
        return self.output_q.get(timeout=time_out)

    def empty(self) -> bool:
        return self.output_q.empty()

    def do_work(self, work_name: str, work_data):
        """
        这个函数比较累，因为还需要负责分发数据   !!!所有定义方法请放在此函数下面，其他函数放之上
        :param work_name:
        :param work_data:
        :return:
        """

        if work_name == '_load_frames_from_video':
            self._load_frames_from_video(work_data)
        if work_name == '_first_search':
            self._first_search(work_data)
        if work_name == '_second_search':
            self._second_search(work_data)
        if work_name == '':
            self._shut_down_all()

    def _load_frames_from_video(self, video_path):
        iterator = VideoIteratorImpl(video_path)
        total_frames = iterator.get_total_f_num()
        self.total_frames = total_frames

        pre_task = int(total_frames / self.worker_num)

        for i, input_queue in enumerate(self.input_queues):
            pre_start = i * pre_task
            pre_end = pre_start + pre_task
            if i == len(self.input_queues) - 1:
                pre_end = total_frames
            input_queue.put(('_load_frames_from_video', (video_path, pre_start, pre_end)))

        iterator.release()

    def _first_search(self, feature_b):
        for i, input_queue in enumerate(self.input_queues):
            input_queue.put(('_first_search', feature_b))

    def _shut_down_all(self):
        for i, input_queue in enumerate(self.input_queues):
            input_queue.put(('', None))

    def _second_search(self, work_data):
        feature_b, possibly_a_starts = work_data

        # 分发任务

        pre_task = int(self.total_frames / self.worker_num)

        workers_data = []  # 二维数组
        for _ in range(self.worker_num):
            workers_data.append([])

        # 17008 5 3400 整理任务
        for a_index in possibly_a_starts:
            work_index = int(a_index / pre_task)
            if work_index > self.worker_num - 1:
                work_index = self.worker_num - 1
            workers_data[work_index].append(a_index)

        for pre_search_scope, input_q in zip(workers_data, self.input_queues):
            input_q.put(('_second_search', (feature_b, pre_search_scope)))
