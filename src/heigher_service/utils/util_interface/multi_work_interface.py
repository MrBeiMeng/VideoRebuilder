import abc


class MultiWorkI(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def do_work(self, work_name: str, work_data):
        """
        指定多进程 任务，这个任务需要事先在具体的实现类中声明。不持支传入任务函数的形式
        :param work_name:
        :param work_data:
        :return:
        """
        pass

    @abc.abstractmethod
    def get_result(self, time_out: int) -> object:
        """
        获取指定工作的结果
        :param time_out:
        :return:
        """
        pass
