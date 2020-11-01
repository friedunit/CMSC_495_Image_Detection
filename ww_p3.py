# Author: John Kaiser
# Date: 10/23/2020
# ORB Feature Matching
# Findings: This was an attempt to combine multi-scaling with key point/descriptor matching. As of now
# it did not show key points or matching

import numpy as np
import cv2
from matplotlib import pyplot as plt
import imutils


def find_object(target_pic, puzzle_pic):
    MIN_MATCH_COUNT = 10
    target = cv2.imread(target_pic)
    puzzle = cv2.imread(puzzle_pic)

    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(puzzle, cv2.COLOR_BGR2GRAY)
    # target = cv2.Canny(target, int(max(0, (1.0 - 0.33) * np.median(target))), int(min(255, (1.0 - 0.33) *
                                                                                      # np.median(target))))
    # target = cv2.Canny(target, 100, 250)

    # Initiate ORB detector
    orb = cv2.ORB_create()

    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(target, None)

    img_kp = cv2.drawKeypoints(target, kp1, 0, color=(0, 255, 0), flags=0)
    plt.imshow(img_kp)
    plt.show()
    # cv2.imshow('edges', img_kp)

    #
    # # Draw first 10 matches.
    # img3 = cv2.drawMatches(target, kp1, puzzle, kp2, matches[:20], None, flags=2)
    #
    # plt.imshow(img3)
    # plt.show()

    # cv2.imshow('edges', target)
    (height, width) = target.shape[:2]
    found = None
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        resized = imutils.resize(gray, width=int(target.shape[1] * scale))
        r = puzzle.shape[1] / float(resized.shape[1])
        if resized.shape[0] < height or resized.shape[1] < width:
            break
        # edged = cv2.Canny(resized, int(max(0, (1.0 - 0.33) * np.median(puzzle))), int(min(255, (1.0 - 0.33) *
                                                                                          # np.median(puzzle))))
        # edged = cv2.Canny(resized, 225, 230)
        kp2, des2 = orb.detectAndCompute(resized, None)
        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Match descriptors.
        matches = bf.match(des2, des1)

        # Sort them in the order of their distance.
        matches = sorted(matches, key=lambda x: x.distance)
        good = []
        for m in matches:
            if m.distance < 0.7:
                good.append(m)
        # result = cv2.matchTemplate(edged, target, cv2.TM_CCOEFF)
        # (_, _, minLoc, maxLoc) = cv2.minMaxLoc(result)
        # (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        # VISUALIZE next 4 lines
        # clone = np.dstack([edged, edged, edged])
        # cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
        #               (maxLoc[0] + width, maxLoc[1] + height), (0, 0, 255), 2)
        # cv2.imshow("Visualize", clone)
        # cv2.waitKey(0)

        # if found is None or maxVal > found[0]:
        #     found = (maxVal, maxLoc, r)
        # if found is None or minLoc > found[0]:
        #     found = (minLoc, maxLoc, r)
        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matches_mask = mask.ravel().tolist()

            h, w = resized.shape[:2]
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            puzzle = cv2.polylines(puzzle, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

        else:
            print
            "Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT)
            matches_mask = None

        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matches_mask,  # draw only inliers
                           flags=2)

        img3 = cv2.drawMatches(target, kp2, puzzle, kp1, good, None, **draw_params)

        plt.imshow(img3), plt.show()

    # (_, maxLoc, r) = found
    # (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    # (endX, endY) = (int((maxLoc[0] + width) * r), int((maxLoc[1] + height) * r))
    # roi = puzzle[startY:endY, startX:endX]
    # # top_left = maxLoc
    # # bottom_right = (top_left[0] + width, top_left[1] + height)
    # mask = np.zeros(puzzle.shape, dtype="uint8")
    # puzzle = cv2.addWeighted(puzzle, 0.25, mask, 0.75, 0)
    # puzzle[startY:endY, startX:endX] = roi
    # puzzle = cv2.rectangle(puzzle, (startX, startY), (endX, endY), (0, 255, 0), 3)


find_object('waldo2.jpeg', 'puzzle2.jpeg')




