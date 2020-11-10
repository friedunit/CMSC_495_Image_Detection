from datetime import datetime as dt
import cv2
import numpy as np
from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk


target_dict = {'Waldo': 'waldo_face.jpeg', 'Wenda': 'wenda.jpeg', 'Wizard': 'wizard.jpeg', 'Odlaw': 'odlaw.jpeg',
               'Woof': 'woofs_tail.jpeg'}
puzzle_dict = {'City': 'Waldo_City.jpeg', 'Buffet': 'Waldo_Buffet.jpeg', 'Department Store': 'Waldo_Department_Store.jpeg',
               'Siege': 'Waldo_Siege.jpeg'}


def my_preview():
    print("Searching for {} in {}!".format(character_dd.get(), scene_dd.get()))
    scene = scene_dd.get()
    character = character_dd.get()
    master.show_scene = ImageTk.PhotoImage(resize_image(puzzle_images / puzzle_dict[scene], (800, 800)))
    master.show_character = ImageTk.PhotoImage(resize_image(target_images / target_dict[character], (200, 200)))
    scene_label.configure(image=master.show_scene)
    character_label.configure(image=master.show_character)
    # if scene_dd.get() == "City":
    #     scene_label.configure(image=master.city)
    # elif scene_dd.get() == "Buffet":
    #     scene_label.configure(image=master.buffet)
    # elif scene_dd.get() == "Department Store":
    #     scene_label.configure(image=master.department)
    # elif scene_dd.get() == "Siege":
    #     scene_label.configure(image=master.siege)
    # if character_dd.get() == "Waldo":
    #     character_label.configure(image=master.waldo)
    # elif character_dd.get() == "Wenda":
    #     character_label.configure(image=master.wenda)
    # elif character_dd.get() == "Wizard":
    #     character_label.configure(image=master.wizard)
    # elif character_dd.get() == "Odlaw":
    #     character_label.configure(image=master.odlaw)
    # elif character_dd.get() == "Woof":
    #     character_label.configure(image=master.woof)


def search_image(target_pic, puzzle_pic):
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
    found = None
    for scale in np.linspace(0.2, 1.0, 5)[::-1]:
        # resized = imutils.resize(puzzle, width=int(puzzle.shape[1] * scale))
        resized = resize_with_aspect_ratio(gray, width=int(puzzle.shape[1] * scale))
        r = puzzle.shape[1] / float(resized.shape[1])
        if resized.shape[0] < height or resized.shape[1] < width:
            break
        # edged = cv2.Canny(resized, int(max(0, (1.0 - 0.33) * np.median(puzzle))), int(min(255, (1.0 - 0.33) *
                                                                                          # np.median(puzzle))))
        # edged = cv2.Canny(resized, 225, 230)
        edged = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        result = cv2.matchTemplate(edged, target, cv2.TM_CCOEFF)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
        # VISUALIZE next 4 lines
        # clone = np.dstack([edged, edged, edged])
        # cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
        #               (maxLoc[0] + width, maxLoc[1] + height), (0, 0, 255), 2)
        # cv2.imshow("Visualize", clone)
        # cv2.waitKey(0)

        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)
        # if found is None or minLoc > found[0]:
        #     found = (minLoc, maxLoc, r)

    (_, maxLoc, r) = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + width) * r), int((maxLoc[1] + height) * r))
    roi = puzzle[startY:endY, startX:endX]
    mask = np.zeros(puzzle.shape, dtype="uint8")
    puzzle = cv2.addWeighted(puzzle, 0.25, mask, 0.75, 0)
    puzzle[startY:endY, startX:endX] = roi
    puzzle = cv2.rectangle(puzzle, (startX, startY), (endX, endY), (0, 255, 0), 3)
    resize = resize_with_aspect_ratio(puzzle, width=850)


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
master.geometry("1000x800")
master.resizable(0, 0)

scene_dd = StringVar(master)
scene_dd.set("Buffet")
s_dd = OptionMenu(master, scene_dd, "Buffet", "Department Store", "City", "Siege")
s_dd.grid(row=0, column=0, sticky=W, pady=2)

character_dd = StringVar(master)
character_dd.set("Waldo")
c_dd = OptionMenu(master, character_dd, "Waldo", "Wenda", "Wizard", "Odlaw", "Woof")
c_dd.grid(row=1, column=0, sticky=W, pady=2)

# imported pathlib to deal with file paths on Windows and Mac/Linux
puzzle_images = Path('Puzzle Images')

scene_image = puzzle_images / puzzle_dict[scene_dd.get()]

# city_image = puzzle_images / 'Waldo_City.jpeg'
# buffet_image = puzzle_images / "Waldo_Buffet.jpeg"
# department_image = puzzle_images / "Waldo_Department_Store.jpeg"
# siege_image = puzzle_images / "Waldo_Siege.jpeg"
# default_image = puzzle_images / "puzzle2.jpeg"

target_images = Path('Target Images')

character_image = target_images / target_dict[character_dd.get()]

# waldo_image = target_images / "waldo1.jpg"
# waldo_face = target_images / 'waldo_face.jpeg'
# odlaw_image = target_images / "odlaw.jpeg"
# wenda_image = target_images / "wenda.jpeg"
# wizard_image = target_images / "wizard.jpeg"
# woof_image = target_images / "woofs_tail.jpeg"


preview_b = Button(master, text="Preview", command=my_preview, width=20)
preview_b.grid(row=0, column=1, sticky=W, pady=2)

search_b = Button(master, text="Search", command=lambda: search_image(target_dict[str(character_dd.get())],
                                                                      puzzle_dict[str(scene_dd.get())]), width=20)
search_b.grid(row=1, column=1, sticky=W, pady=2)

# master.default = ImageTk.PhotoImage(resize_image(default_image, (800, 800)))
# master.city = ImageTk.PhotoImage(resize_image(city_image, (800, 800)))
# master.buffet = ImageTk.PhotoImage(resize_image(buffet_image, (800, 800)))
master.buffet = ImageTk.PhotoImage(resize_image(puzzle_images / puzzle_dict['Buffet'], (800, 800)))
# master.department = ImageTk.PhotoImage(resize_image(department_image, (800, 800)))
# master.siege = ImageTk.PhotoImage(resize_image(siege_image, (800, 800)))
# master.show_scene = ImageTk.PhotoImage(resize_image(scene_image, (800, 800)))

scene_label = Label(master, image=master.buffet)
scene_label.grid(row=2, column=0, columnspan=2, rowspan=1, sticky=W, pady=2)

master.waldo = ImageTk.PhotoImage(resize_image(target_images / target_dict['Waldo'], (200, 200)))
# master.odlaw = ImageTk.PhotoImage(resize_image(odlaw_image, (200, 200)))
# master.wenda = ImageTk.PhotoImage(resize_image(wenda_image, (200, 200)))
# master.wizard = ImageTk.PhotoImage(resize_image(wizard_image, (200, 200)))
# master.woof = ImageTk.PhotoImage(resize_image(woof_image, (200, 200)))
# master.show_character = ImageTk.PhotoImage(resize_image(character_image, (200, 200)))
# master.character_image = ImageTk.PhotoImage(resize_image(character_image, (200, 200)))

character_label = Label(master, image=master.waldo)
character_label.grid(row=2, column=3, sticky=W, pady=2)


mainloop()
