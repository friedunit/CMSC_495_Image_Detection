# Author: John Kaiser
# Date: 10/24/2020
# ORB feature Matching with Brute Force Matcher
# Based off of https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_orb/py_orb.html
# Findings: When using waldo2.jpeg as target image, it found several good keypoints but the matching to
# puzzle2.jpeg did not give good results. Using waldo_face.jpeg did not produce keypoints, maybe the quality
# was not good enough. I tried using waldo2.jpeg with smaller cropper images of puzzle2.jpeg to see if
# the keypoint matching would be better, but the matches were still all over the place.

import numpy as np
import cv2
import matplotlib.pyplot as plt
import imutils

target = cv2.imread('waldo2.jpeg', 0)
puzzle = cv2.imread('puzzle2.jpeg', 0)

(height, width) = target.shape[:2]

orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(target, None)
kp2, des2 = orb.detectAndCompute(puzzle, None)

img_kp = cv2.drawKeypoints(target, kp1, 0, color=(0, 255, 0), flags=0)
plt.imshow(img_kp)
plt.show()

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

matches = bf.match(des1, des2)
matches = sorted(matches, key=lambda x: x.distance)
good = []
for m in matches:
    if m.distance < 0.7:
        good.append(m)

img3 = cv2.drawMatches(target, kp1, puzzle, kp2, matches[:50], None, flags=2)
plt.imshow(img3)
plt.show()
