from src.heigher_service.impl.two_p_fast_dtw_sift_impl import TwoPFastDtwSiftImpl
import cv2
import numpy as np


class OrbModelSingleImpl:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = cv2.ORB_create()
            print("inited model")
        return cls._instance

    def get_model(self):
        return self.model


class TwoPFastDtwOrbImpl(TwoPFastDtwSiftImpl):
    @staticmethod
    def get_distance(feature_a, feature_b) -> float:
        feature_a = feature_a.astype(np.uint8)
        feature_b = feature_b.astype(np.uint8)

        # Find the keypoints and descriptors with SURF
        keypoints1, descriptors1 = OrbModelSingleImpl().get_model().detectAndCompute(feature_a, None)
        keypoints2, descriptors2 = OrbModelSingleImpl().get_model().detectAndCompute(feature_b, None)

        if descriptors1 is None or descriptors2 is None or descriptors1.size == 0 or descriptors2.size == 0:
            # print("Descriptors are empty.")
            if descriptors1 is None:
                return 60
            if descriptors2 is None:
                return 40
        try:
            # Use BFMatcher to find matches
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(descriptors1, descriptors2, k=2)

            # Apply ratio test
            good_matches = []
            for m, n in matches:
                if m.distance < 0.93 * n.distance:
                    good_matches.append(m)

            # Print the number of good matches
            # print(len(good_matches))

            similarity = 0  # 如果黑屏则确认匹配
            if (len(keypoints1) + len(keypoints2)) != 0:
                similarity = len(good_matches) / (len(keypoints1) + len(keypoints2))

            # print(similarity)

            # Draw matches
            # img_matches = cv2.drawMatches(feature_a, keypoints1, feature_b, keypoints2, good_matches, outImg=None)
            # cv2.imshow('Matches', img_matches)
            # cv2.waitKey(1)
        except Exception as e:
            print(f"出现错误！！{e.args}")
            return 30

        distance = 1 - similarity  # 可以加上一个 判断。

        if distance > 0.8:
            distance = 1

        return distance * 100
