import cv2
import numpy as np

from src.heigher_service.impl.two_p_align import TwoPointAlignImpl
from src.service.impl.video_creator_impl import VideoCreatorImpl
from src.service.video_creator_interface import VideoCreatorI


class TwoPointAlignSiftImpl(TwoPointAlignImpl):

    def __init__(self, video_a_path, video_b_path, a_iterator=None):
        super().__init__(video_a_path, video_b_path)
        self.model = cv2.SIFT_create()
        if a_iterator is not None:
            self.a_iterator = a_iterator

    def get_feature(self, frame) -> np.ndarray:

        if frame.shape[1] != self.common_size[0] and frame.shape[0] != self.common_size[1]:
            # 计算视频B的长宽比
            aspect_ratio_b = self.common_size[0] / self.common_size[1]  # 宽度/高度

            # 计算中间截取区域的宽度和高度
            center_y, center_x = frame.shape[0] // 2, frame.shape[1] // 2
            if frame.shape[1] / frame.shape[0] > aspect_ratio_b:
                # 如果视频A的长宽比大于视频B的长宽比，则保持高度不变，调整宽度
                crop_height = frame.shape[0]
                crop_width = int(crop_height * aspect_ratio_b)
            else:
                # 如果视频A的长宽比小于等于视频B的长宽比，则保持宽度不变，调整高度
                crop_width = frame.shape[1]
                crop_height = int(crop_width / aspect_ratio_b)

            # 计算裁剪区域的边界
            crop_x_start = center_x - crop_width // 2
            crop_x_end = center_x + crop_width // 2
            crop_y_start = center_y - crop_height // 2
            crop_y_end = center_y + crop_height // 2

            # 从视频A的中间按照视频B的长宽比截取
            cropped_frame_a = frame[crop_y_start:crop_y_end, crop_x_start:crop_x_end]

            # 调整截取后的frame_a的分辨率以匹配frame_b
            resized_frame_a = cv2.resize(cropped_frame_a, (self.common_size[0], self.common_size[1]),
                                         interpolation=cv2.INTER_AREA)
            # resized_frame_b = cv2.resize(frame_b, (cropped_frame_a.shape[1], cropped_frame_a.shape[0]),
            #                              interpolation=cv2.INTER_AREA)

            return resized_frame_a
        else:
            frame = cv2.resize(frame,
                               (int(self.common_size[0] / 1), int(self.common_size[1] / 1)))  # 调整帧大小来降低计算量
        return frame

    def _cut_frame(self, frame_a, frame_b):

        # 计算裁剪区域的边界（如果需要进一步裁剪）
        height, width = frame_b.shape[:2]
        crop_width_start = width // 5
        crop_width_end = 4 * width // 5
        crop_height_start = height // 5
        crop_height_end = 4 * height // 5

        # 裁剪调整分辨率后的frame_a和frame_b的中间3/5的区域
        final_cropped_frame_a = frame_a[crop_height_start:crop_height_end, crop_width_start:crop_width_end]
        final_cropped_frame_b = frame_b[crop_height_start:crop_height_end, crop_width_start:crop_width_end]

        return final_cropped_frame_a, final_cropped_frame_b

    def get_distance(self, feature_a, feature_b) -> int:

        feature_a, feature_b = self._cut_frame(feature_a, feature_b)

        # Find the keypoints and descriptors with SIFT
        keypoints1, descriptors1 = self.model.detectAndCompute(feature_a, None)
        keypoints2, descriptors2 = self.model.detectAndCompute(feature_b, None)

        if descriptors1 is None or descriptors2 is None or descriptors1.size == 0 or descriptors2.size == 0:
            # print("Descriptors are empty.")
            if descriptors1 is None:
                return 0
            if descriptors2 is None:
                return 1
        try:
            # Use BFMatcher to find matches
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(descriptors1, descriptors2, k=2)

            # Apply ratio test
            good_matches = []
            for m, n in matches:
                if m.distance < 0.88 * n.distance:
                    good_matches.append(m)

            # Print the number of good matches
            # print(len(good_matches))

            similarity = 1  # 如果黑屏则确认匹配
            if (len(keypoints1) + len(keypoints2)) != 0:
                similarity = len(good_matches) / (len(keypoints1) + len(keypoints2))

            # print(similarity)

            # Draw matches
            img_matches = cv2.drawMatches(feature_a, keypoints1, feature_b, keypoints2, good_matches, outImg=None)
            cv2.imshow('Matches', img_matches)
            cv2.waitKey(1)
        except Exception as e:
            print(f"出现错误！！{e.args}")
            return 1

        return similarity

    @staticmethod
    def check_value(distance):
        return distance > 0.15
        # return super().check_value(distance)


class TwoPointAlignSiftImplMaDaJiaSiJia(TwoPointAlignSiftImpl):

    def __init__(self, video_a_path, video_b_path, a_iterator=None):
        super().__init__(video_a_path, video_b_path, a_iterator)

    def get_video_creator(self) -> VideoCreatorI:
        fps_a, (a_w, a_h) = self.a_iterator.get_video_info()
        fps_b, (b_w, b_h) = self.b_iterator.get_video_info()

        higher_size = (a_w, a_h)
        lower_fps = fps_a
        # if b_w > a_w and b_h > a_h:
        #     higher_size = (b_w, b_h)
        #     higher_fps = fps_b

        if fps_a > fps_b:
            lower_fps = fps_b

        # out_put_path, fps, video_size
        print(f"set output info: output_path {self.video_b_path},fps {23.976}, size {higher_size}")

        return VideoCreatorImpl(self.video_b_path, 23.976, higher_size)
