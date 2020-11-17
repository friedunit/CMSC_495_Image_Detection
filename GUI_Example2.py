# CMSC 495 Current Trends and Projects
# Fall 2020
# Contributors: John Kaiser, Orry Newell, Cody Ambrose, Rodney French
# Our Capstone project was to research different Computer Vision algorithms and techniques to produce an image
# detection program that would find a target image in a larger 'puzzle' image. We used Where's Waldo puzzles as test
# data to find Waldo and his friends in various scenes from the book.

import cv2
import numpy as np
from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk


target_dict = {'Waldo': 'waldo_face.jpeg', 'Wenda': 'wenda.jpg', 'Wizard': 'wizard.jpg', 'Odlaw': 'odlaw.jpg',
               'Woof': 'woofs_tail.jpg'}

puzzle_dict = {'Beach': 'puzzle3.jpeg', 'City': 'puzzle2.jpeg', 'Zoo': 'zoo.jpeg',
               'Department Store': 'Waldo_Department_Store.jpeg', 'Ski Resort': 'ski.jpeg',
               'Train Station': 'train.jpeg', 'Museum': 'museum.jpeg'}


# the my_preview method is called when the 'Preview' button is pressed
def my_preview():
    print("Searching for {} in {}!".format(character_dd.get(), scene_dd.get()))
    scene = scene_dd.get()
    character = character_dd.get()
    # openCV read in the scene image selected from dropdown menu
    scene_image = cv2.imread(str(puzzle_images / puzzle_dict[scene]))
    # resize the scene image to 80% of the user's screen width
    scene_image = resize_with_aspect_ratio(scene_image, height=int(screen_height*0.8))
    # process the image and return it, set it to master.show_scene for tkinter GUI
    master.show_scene = process_image(scene_image)
    target_image = cv2.imread(str(target_images / target_dict[character]))
    target_image = resize_with_aspect_ratio(target_image, width=100)
    master.show_character = process_image(target_image)
    # configure scene_label and character_label to show both images
    scene_label.configure(image=master.show_scene)
    character_label.configure(image=master.show_character)
    # remove the zoomed in feature when Preview is used
    zoomed_label.grid_remove()


# method to process images by converting them from openCV BGR to RGB, then PIL format, then ImageTk format
def process_image(image):
    # Convert image from openCV BGR to RGB for displaying
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Convert to PIL format
    image = Image.fromarray(image)
    # ImageTk format to show in TkInter
    image = ImageTk.PhotoImage(image)
    return image


# search_image method is called when clicking the 'Search' button
def search_image(target_pic, puzzle_pic):
    # read in the 2 images (template image to search for and the larger image to search
    target = cv2.imread(target_pic)
    puzzle = cv2.imread(puzzle_pic)
    # convert both images to grayscale
    target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    puzzle_gray = cv2.cvtColor(puzzle, cv2.COLOR_BGR2GRAY)
    # use adaptive thresholding for the target image
    # this had better results than Canny edge detection for template matching
    target_edge = cv2.adaptiveThreshold(target_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # get and assign the height and width of the target image
    (height, width) = target.shape[:2]
    found = None
    # np.linspace(start, stop, number) returns a list of 'number' evenly spaced numbers between start and stop
    # the list slicing [::-1] goes in reverse to start with the largest scale to the smallest
    for scale in np.linspace(0.5, 2.0, 10)[::-1]:
        # resize the grayscale puzzle image for each scale in the list
        resized = resize_with_aspect_ratio(puzzle_gray, width=int(puzzle.shape[1] * scale))
        # set ratio to puzzle width divided by resized width
        ratio = puzzle.shape[1] / float(resized.shape[1])
        # if the resized image gets smaller than the target image, break from for loop
        if resized.shape[0] < height or resized.shape[1] < width:
            break
        # now apply adaptive thresholding to the resized image
        edged = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # perform the template matching on the 'edged' target and puzzle images
        # different matching methods can produce different results
        # we have mostly used TM_CCOEFF
        result = cv2.matchTemplate(edged, target_edge, cv2.TM_CCOEFF)
        # when using TM_CCOEFF, maxLoc from minMaxLoc() gives best matching results
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
        # check to see if found is still set to None or if maxVal is better than found's maxVal
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, ratio)
    (maxVal, maxLoc, ratio) = found
    # x and y of maxLoc are best results from template matching method
    (startX, startY) = (int(maxLoc[0] * ratio), int(maxLoc[1] * ratio))
    (endX, endY) = (int((maxLoc[0] + width) * ratio), int((maxLoc[1] + height) * ratio))
    # region of interest is the section of puzzle with best results
    roi = puzzle[startY:endY, startX:endX]
    # create a darkened mask over the puzzle to easily see the located target
    mask = np.zeros(puzzle.shape, dtype="uint8")
    puzzle = cv2.addWeighted(puzzle, 0.25, mask, 0.75, 0)
    puzzle[startY:endY, startX:endX] = roi
    # draw a green box around the target (ROI)
    puzzle = cv2.rectangle(puzzle, (startX, startY), (endX, endY), (0, 255, 0), 3)
    # expand the ROI to create a zoomed-in feature
    zoomed = puzzle[startY-100:endY+100, startX-100:endX+100]
    # resize the new image to 80% of the screen height
    resize = resize_with_aspect_ratio(puzzle, height=int(screen_height*0.8))
    # process the 3 images for displaying in TkInter GUI and configure them
    master.show_scene = process_image(resize)
    target = resize_with_aspect_ratio(target, width=100)
    master.show_character = process_image(target)
    master.show_zoomed = process_image(zoomed)
    scene_label.configure(image=master.show_scene)
    character_label.configure(image=master.show_character)
    zoomed_label.configure(image=master.show_zoomed)
    # set zoomed_label.grid to be under the target image, 'South' to stick at the bottom
    zoomed_label.grid(row=2, column=3, sticky=S, pady=2)


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


# create the TkInter GUI
master = Tk()

master.title("Where's Waldo Application")
# get screen height and width
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
# set GUI window to full screen
master.geometry(f'{screen_width}x{screen_height}')
master.resizable(0, 0)

# scene drop down menu
scene_dd = StringVar(master)
scene_dd.set('City')
# option menu selection sets variable scene_dd, loaded from puzzle_dict keys
s_dd = OptionMenu(master, scene_dd, *puzzle_dict.keys())
s_dd.grid(row=0, column=0, sticky=W, pady=2)

character_dd = StringVar(master)
character_dd.set('Waldo')
c_dd = OptionMenu(master, character_dd, *target_dict.keys())
c_dd.grid(row=1, column=0, sticky=W, pady=2)

# imported pathlib to deal with file paths on Windows and Mac/Linux
puzzle_images = Path('Puzzle Images')

target_images = Path('Target Images')


def get_scene():
    return str(puzzle_images / puzzle_dict[scene_dd.get()])


def get_character():
    return str(target_images / target_dict[character_dd.get()])


preview_b = Button(master, text="Preview", command=my_preview, width=20)
preview_b.grid(row=0, column=1, sticky=W, pady=2)

search_b = Button(master, text="Search", command=lambda: search_image(get_character(), get_scene()), width=20)
search_b.grid(row=1, column=1, sticky=W, pady=2)

default_image = cv2.imread(str(puzzle_images / puzzle_dict['City']))
default_image = resize_with_aspect_ratio(default_image, height=int(screen_height*0.8))
master.default = process_image(default_image)

scene_label = Label(master, image=master.default)
scene_label.grid(row=2, column=0, columnspan=2, rowspan=1, sticky=W, pady=2)

waldo_image = cv2.imread(str(target_images / target_dict['Waldo']))
waldo_image = resize_with_aspect_ratio(waldo_image, width=100)
master.waldo = process_image(waldo_image)

character_label = Label(master, image=master.waldo)
character_label.grid(row=2, column=3, sticky=NW, pady=2)

zoomed_label = Label(master)
zoomed_label.grid(row=2, column=3, sticky=S, pady=2)

mainloop()
