# Author: John Kaiser
# Date: 10/25/2020
# TM_CCOEFF_NORMED template matching method
# Findings: This method compares the results to a threshold between 0 and 1.
# Threshold 0.5 produced 17 results but none were correct faces when looking for waldo_face.jpeg in puzzle 2
# The higher threshold, the better. Adjustments would need to be made to improve accuracy

import cv2
import numpy as np
from matplotlib import pyplot as plt


def find_object(target_pic, puzzle_pic):
    # second parameter 0 reads in as grayscale
    target = cv2.imread(target_pic)
    puzzle = cv2.imread(puzzle_pic)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(puzzle, cv2.COLOR_BGR2GRAY)
    # target = cv2.adaptiveThreshold(target, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # target = cv2.Canny(target, int(max(0, (1.0 - 0.33) * np.median(target))), int(min(255, (1.0 - 0.33) *
                                                                                      # np.median(target))))
    # edged = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # edged = cv2.Canny(gray, int(max(0, (1.0 - 0.33) * np.median(gray))), int(min(255, (1.0 - 0.33) *
                                                                                 # np.median(gray))))
    # gray_puzzle = cv2.cvtColor(puzzle, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Waldo', target)
    threshold = 0.5

    matching = cv2.matchTemplate(gray, target, cv2.TM_CCOEFF_NORMED)

    # width, height = target.shape[::-1]
    (height, width) = target.shape[:2]
    print(target.shape)

    finding = np.where(matching >= threshold)

    match_count = 0

    for match in zip(*finding[::-1]):
        match_count += 1
        puzzle = cv2.rectangle(puzzle, match, (match[0] + width, match[1] + height), (0, 255, 0), 2)

    print(match_count)
    # plt.imshow(puzzle)
    # plt.show()
    resize = resize_with_aspect_ratio(puzzle, width=850)
    # resize = imutils.resize(puzzle, width=800)
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


find_object('waldo_face.jpeg', 'puzzle2.jpeg')
