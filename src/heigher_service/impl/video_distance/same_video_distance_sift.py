import warnings

import cv2
import numpy as np
from numpy import deprecate

from src.heigher_service.impl.video_distance.same_video_distance_vgg16 import SameVideoDistanceVgg16


class SameVideoDistanceSift(SameVideoDistanceVgg16):
    def __init__(self, v_a_path, v_b_path, draw_name=''):
        super().__init__(v_a_path, v_b_path, draw_name)
        # Initialize SIFT detector
        self.model = cv2.SIFT_create()

    def generate_distance(self, frame_a, frame_b, w, h):

        frame_a = cv2.resize(frame_a, (int(w / 2), int(h / 2)))  # 调整帧大小以匹配VGG16的输入大小
        frame_b = cv2.resize(frame_b, (int(w / 2), int(h / 2)))  # 调整帧大小以匹配VGG16的输入大小

        # Find the keypoints and descriptors with SIFT
        keypoints1, descriptors1 = self.model.detectAndCompute(frame_a, None)
        keypoints2, descriptors2 = self.model.detectAndCompute(frame_b, None)

        # Use BFMatcher to find matches
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(descriptors1, descriptors2, k=2)

        # Apply ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        # Print the number of good matches
        # print(len(good_matches))

        similarity = 0
        if (len(keypoints1) + len(keypoints2)) != 0:
            similarity = len(good_matches) / (len(keypoints1) + len(keypoints2))

        print(similarity)

        # Draw matches
        img_matches = cv2.drawMatches(frame_a, keypoints1, frame_b, keypoints2, good_matches, outImg=None)
        cv2.imshow('Matches', img_matches)
        cv2.waitKey(1)

        return similarity


class SameVideoDistanceSiftRANSAC(SameVideoDistanceVgg16):
    def __init__(self, v_a_path, v_b_path, draw_name=''):
        super().__init__(v_a_path, v_b_path, draw_name)
        # Initialize SIFT detector
        self.model = cv2.SIFT_create()

    def generate_distance(self, frame_a, frame_b, w, h):

        # Find the keypoints and descriptors with SIFT
        keypoints1, descriptors1 = self.model.detectAndCompute(frame_a, None)
        keypoints2, descriptors2 = self.model.detectAndCompute(frame_b, None)

        # Use BFMatcher to find matches
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(descriptors1, descriptors2, k=2)

        # Apply ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        # Convert keypoints to an array of points
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        if len(good_matches) == 0:
            return 0

        # Find homography
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        # Convert mask to a list of booleans
        mask = mask.ravel().tolist()

        # Filter good matches using the mask
        final_matches = [good_matches[i] for i, val in enumerate(mask) if val]

        # Draw final matches
        img_matches = cv2.drawMatches(frame_a, keypoints1, frame_b, keypoints2, final_matches, outImg=None)
        cv2.imshow('Final Matches', img_matches)
        cv2.waitKey(1)

        similarity = 0
        if min(len(keypoints1), len(keypoints2)) != 0:
            similarity = len(final_matches) / min(len(keypoints1), len(keypoints2))

        return similarity
