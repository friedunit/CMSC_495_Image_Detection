# Author: John Kaiser
# Date: 10/30/2020
# Multi-scale template matching branch from ww_p2.py to add scaling option for both target and puzzle

import cv2
import numpy as np
from matplotlib import pyplot as plt

found = None
target = None


def find_object(target_pic, puzzle_pic):
    global target
    target = cv2.imread(target_pic)
    puzzle = cv2.imread(puzzle_pic)
    # target = resize_with_aspect_ratio(target, width=70)
    # target = cv2.medianBlur(target, 5)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(puzzle, cv2.COLOR_BGR2GRAY)
    # gray = cv2.medianBlur(gray, 5)
    # target = cv2.Canny(target, int(max(0, (1.0 - 0.33) * np.median(target))), int(min(255, (1.0 - 0.33) *
                                                                                      # np.median(target))))
    # target = cv2.Canny(target, 100, 250)
    target = cv2.adaptiveThreshold(target, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imshow('edges', target)
    (height, width) = target.shape[:2]
    scale_and_match(gray)
    scale_and_match(target)
    (_, maxLoc, r) = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + width) * r), int((maxLoc[1] + height) * r))
    roi = puzzle[startY:endY, startX:endX]
    # top_left = maxLoc
    # bottom_right = (top_left[0] + width, top_left[1] + height)
    mask = np.zeros(puzzle.shape, dtype="uint8")
    puzzle = cv2.addWeighted(puzzle, 0.25, mask, 0.75, 0)
    puzzle[startY:endY, startX:endX] = roi
    puzzle = cv2.rectangle(puzzle, (startX, startY), (endX, endY), (0, 255, 0), 3)
    resize = resize_with_aspect_ratio(puzzle, width=850)
    # resize = imutils.resize(puzzle, width=800)
    while True:
        cv2.imshow('Puzzle', resize)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            break
    cv2.destroyAllWindows()


def scale_and_match(image_to_scale):
    for scale in np.linspace(0.2, 1.0, 5)[::-1]:
        resized = resize_with_aspect_ratio(image_to_scale, width=int(image_to_scale.shape[1] * scale))
        r = image_to_scale.shape[1] / float(resized.shape[1])
        # if resized.shape[0] < height or resized.shape[1] < width:
            # break
        # edged = cv2.Canny(resized, int(max(0, (1.0 - 0.33) * np.median(puzzle))), int(min(255, (1.0 - 0.33) *
                                                                                          # np.median(puzzle))))
        # edged = cv2.Canny(resized, 225, 230)
        edged = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        result = cv2.matchTemplate(edged, target, cv2.TM_CCOEFF)
        # (_, _, minLoc, maxLoc) = cv2.minMaxLoc(result)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
        # VISUALIZE next 4 lines
        # clone = np.dstack([edged, edged, edged])
        # cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
        #               (maxLoc[0] + width, maxLoc[1] + height), (0, 0, 255), 2)
        # cv2.imshow("Visualize", clone)
        # cv2.waitKey(0)
        global found
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)
        # if found is None or minLoc > found[0]:
        #     found = (minLoc, maxLoc, r)


def resize_with_aspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)


find_object('waldo1.jpg', 'puzzle2.jpeg')
