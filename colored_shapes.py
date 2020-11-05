# Author: John Kaiser
# Date: 11/4/2020
# Same GUI as shape_gui.py to select 1 of 3 colored stars to search for in colored_stars.png image
#
# Findings: This program uses openCV template matching with TM_SQDIFF_NORMED instead of TM_CCOEFF
# as the template matching method. SQDIFF uses minLoc instead of maxLoc for best results and detected the
# different colored stars

from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np


def find_object(target_pic, puzzle_pic):
    global show_target, show_image
    target = cv2.imread(target_pic)
    puzzle = cv2.imread(puzzle_pic)
    (height, width) = target.shape[:2]
    result = cv2.matchTemplate(puzzle, target, cv2.TM_SQDIFF_NORMED)
    (_, _, minLoc, maxLoc) = cv2.minMaxLoc(result)
    top_left = minLoc
    bottom_right = (top_left[0] + width, top_left[1] + height)
    puzzle = cv2.rectangle(puzzle, top_left, bottom_right, (0, 255, 0), 3)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)
    puzzle = cv2.cvtColor(puzzle, cv2.COLOR_BGR2RGB)
    # Resize both target and puzzle images to fit on screen
    target = resize_with_aspect_ratio(target, width=200)
    puzzle = resize_with_aspect_ratio(puzzle, width=600)
    # convert the images to PIL format...
    target = Image.fromarray(target)
    puzzle = Image.fromarray(puzzle)
    # ...and then to ImageTk format
    target = ImageTk.PhotoImage(target)
    puzzle = ImageTk.PhotoImage(puzzle)
    # if the panels are None, initialize them
    if show_target is None or show_image is None:
        # the first panel will store our target image
        show_target = Label(image=target)
        show_target.image = target
        show_target.pack(side="left", padx=10, pady=10)
        # while the second panel will store the image to search
        show_image = Label(image=puzzle)
        show_image.image = puzzle
        show_image.pack(side="right", padx=10, pady=10)
    # otherwise, update the image panels
    else:
        # update the panels
        show_target.configure(image=target)
        show_image.configure(image=puzzle)
        show_target.image = target
        show_image.image = puzzle


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


# Create tkinter GUI
window = Tk()
window.geometry('1000x700+10+10')
window.title('Image Detection')
show_target = None
show_image = None
target_dict = {'Red': 'Shape Templates/red_star.png', 'Green': 'Shape Templates/green_star.png',
               'Blue': 'Shape Templates/blue_star.png'}
target_label = Label(window, text='Select color to search for:')
target_label.place(x=5, y=40)
target_list_box = Listbox(window, height=4, selectmode='single', exportselection=0)
for t in target_dict:
    target_list_box.insert(END, t)
target_list_box.place(x=5, y=60)
find_button = Button(window, text='Find', command=lambda: find_object(target_dict[target_list_box.get(ANCHOR)],
                                                                      'Images to Search/colored_stars.png'))
find_button.place(x=200, y=40)
# target_list_box.selection_clear(0, 'end')

window.mainloop()
