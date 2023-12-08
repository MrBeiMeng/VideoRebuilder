import abc


class WorkI(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def do_work(self):
        pass

    # @staticmethod
    @abc.abstractmethod
    def check_attributes(self):
        pass
