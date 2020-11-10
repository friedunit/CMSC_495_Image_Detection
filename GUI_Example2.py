from datetime import datetime as dt
import cv2
import numpy as np
from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk


target_dict = {'Waldo': 'waldo_face.jpeg', 'Wenda': 'wenda.jpg', 'Wizard': 'wizard.jpg', 'Odlaw': 'odlaw.jpg',
               'Woof': 'woofs_tail.jpg'}
puzzle_dict = {'Beach': 'puzzle3.jpeg', 'City': 'puzzle2.jpeg', 'Buffet': 'Waldo_Buffet.jpeg', 'Department Store': 'Waldo_Department_Store.jpeg',
               'Siege': 'Waldo_Siege.jpeg'}


def my_preview():
    print("Searching for {} in {}!".format(character_dd.get(), scene_dd.get()))
    scene = scene_dd.get()
    character = character_dd.get()
    master.show_scene = ImageTk.PhotoImage(resize_image(puzzle_images / puzzle_dict[scene], (800, 800)))
    master.show_character = ImageTk.PhotoImage(resize_image(target_images / target_dict[character], (200, 200)))
    scene_label.configure(image=master.show_scene)
    character_label.configure(image=master.show_character)


def search_image(target_pic, puzzle_pic):
    target = cv2.imread(target_pic)
    puzzle = cv2.imread(puzzle_pic)
    target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    puzzle_gray = cv2.cvtColor(puzzle, cv2.COLOR_BGR2GRAY)
    # target = cv2.Canny(target, int(max(0, (1.0 - 0.33) * np.median(target))), int(min(255, (1.0 - 0.33) *
                                                                                      # np.median(target))))
    # target = cv2.Canny(target, 100, 250)
    target_edge = cv2.adaptiveThreshold(target_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    (height, width) = target.shape[:2]
    found = None
    for scale in np.linspace(0.5, 1.8, 10)[::-1]:
        resized = resize_with_aspect_ratio(puzzle_gray, width=int(puzzle.shape[1] * scale))
        r = puzzle.shape[1] / float(resized.shape[1])
        if resized.shape[0] < height or resized.shape[1] < width:
            break
        # edged = cv2.Canny(resized, int(max(0, (1.0 - 0.33) * np.median(puzzle))), int(min(255, (1.0 - 0.33) *
                                                                                          # np.median(puzzle))))
        # edged = cv2.Canny(resized, 225, 230)
        edged = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        result = cv2.matchTemplate(edged, target_edge, cv2.TM_CCOEFF)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)

    (_, maxLoc, r) = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + width) * r), int((maxLoc[1] + height) * r))
    roi = puzzle[startY:endY, startX:endX]
    mask = np.zeros(puzzle.shape, dtype="uint8")
    puzzle = cv2.addWeighted(puzzle, 0.25, mask, 0.75, 0)
    puzzle[startY:endY, startX:endX] = roi
    puzzle = cv2.rectangle(puzzle, (startX, startY), (endX, endY), (0, 255, 0), 3)
    zoomed = puzzle[startY-100:endY+100, startX-100:endX+100]
    resize = resize_with_aspect_ratio(puzzle, height=int(screen_height*0.8))
    # convert from openCV BGR to RGB for displaying images
    resize = cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)
    zoomed = cv2.cvtColor(zoomed, cv2.COLOR_BGR2RGB)
    resize = Image.fromarray(resize)
    master.show_scene = ImageTk.PhotoImage(resize)
    target = resize_with_aspect_ratio(target, width=100)
    target = Image.fromarray(target)
    master.show_character = ImageTk.PhotoImage(target)
    zoomed = Image.fromarray(zoomed)
    master.show_zoomed = ImageTk.PhotoImage(zoomed)
    scene_label.configure(image=master.show_scene)
    character_label.configure(image=master.show_character)
    zoomed_label.configure(image=master.show_zoomed)


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


def resize_image(image_location, size_set):
    image = Image.open(image_location)
    image = image.resize(size_set, Image.ANTIALIAS)
    return image


master = Tk()

master.title("Where's Waldo Application")
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
master.geometry(f'{screen_width}x{screen_height}')
master.resizable(0, 0)

scene_dd = StringVar(master)
scene_dd.set('Buffet')
s_dd = OptionMenu(master, scene_dd, *puzzle_dict.keys())
s_dd.grid(row=0, column=0, sticky=W, pady=2)

character_dd = StringVar(master)
character_dd.set('Waldo')
c_dd = OptionMenu(master, character_dd, *target_dict.keys())
c_dd.grid(row=1, column=0, sticky=W, pady=2)

# imported pathlib to deal with file paths on Windows and Mac/Linux
puzzle_images = Path('Puzzle Images')
# scene_image = puzzle_images / puzzle_dict[scene_dd.get()]

target_images = Path('Target Images')
# character_image = target_images / target_dict[character_dd.get()]


def get_scene():
    return str(puzzle_images / puzzle_dict[scene_dd.get()])


def get_character():
    return str(target_images / target_dict[character_dd.get()])


preview_b = Button(master, text="Preview", command=my_preview, width=20)
preview_b.grid(row=0, column=1, sticky=W, pady=2)

search_b = Button(master, text="Search", command=lambda: search_image(get_character(), get_scene()), width=20)
search_b.grid(row=1, column=1, sticky=W, pady=2)

master.default = ImageTk.PhotoImage(resize_image(puzzle_images / puzzle_dict['Buffet'], (800, 800)))

scene_label = Label(master, image=master.default)
scene_label.grid(row=2, column=0, columnspan=2, rowspan=1, sticky=W, pady=2)

master.waldo = ImageTk.PhotoImage(resize_image(target_images / target_dict['Waldo'], (200, 200)))

character_label = Label(master, image=master.waldo)
character_label.grid(row=2, column=3, sticky=NW, pady=2)

zoomed_label = Label(master)
zoomed_label.grid(row=2, column=3, sticky=S, pady=2)


mainloop()
