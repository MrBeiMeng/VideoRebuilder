import abc


class RunnerI(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self):
        pass
