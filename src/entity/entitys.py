import numpy as np


class KeyFrame:
    frame: np.ndarray
    startIndex: int
    endIndex: int

    def __init__(self, frame, start_index, end_index):
        self.frame = frame
        self.startIndex = start_index
        self.endIndex = end_index

    def get_frame(self):
        return self.frame

    def set_frame(self, frame):
        self.frame = frame

    def get_start_index(self):
        return self.startIndex

    def set_start_index(self, start_index):
        self.startIndex = start_index

    def get_end_index(self):
        return self.endIndex

    def set_end_index(self, end_index):
        self.endIndex = end_index
