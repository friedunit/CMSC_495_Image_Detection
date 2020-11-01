# Author: John Kaiser
# Date: 10/20/2020
# First Where's Waldo practice with template matching
# Information from Adrian Rosebrock
# https://web.archive.org/web/20170918035306/https://machinelearningmastery.com/using-opencv-python-and-template-matching-to-play-wheres-waldo/
# Findings: This initial template matching is simplified to find a template taken directly
# from the puzzle and same scale. It works, but requires you to first find Waldo in the puzzle
# so this is not adequate. It is a good starting spot though. Added in was the method
# resize_with_aspect_ratio() since the puzzle image was too large for the screen.

import cv2
import numpy as np


def find_object(target_pic, puzzle_pic):
    target = cv2.imread(target_pic)
    puzzle = cv2.imread(puzzle_pic)
    (height, width) = target.shape[:2]
    result = cv2.matchTemplate(puzzle, target, cv2.TM_CCOEFF)
    (_, _, minLoc, maxLoc) = cv2.minMaxLoc(result)
    top_left = maxLoc
    bottom_right = (top_left[0] + width, top_left[1] + height)
    puzzle = cv2.rectangle(puzzle, top_left, bottom_right, (0, 255, 0), 3)
    resize = resize_with_aspect_ratio(puzzle, width=900)
    while True:
        cv2.imshow('Puzzle', resize)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            break
    cv2.destroyAllWindows()


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


find_object('waldo4.jpeg', 'puzzle2.jpeg')


