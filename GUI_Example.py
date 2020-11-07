from datetime import datetime as dt
from tkinter import *
from PIL import Image, ImageTk


def myPreview():
    print("Searching for {} in {}!".format(character_dd.get(), scene_dd.get()))
    if scene_dd.get() == "City":
        scene_label.configure(image=master.city)
    elif scene_dd.get() == "Buffet":
        scene_label.configure(image=master.buffet)
    elif scene_dd.get() == "Department Store":
        scene_label.configure(image=master.department)
    elif scene_dd.get() == "Siege":
        scene_label.configure(image=master.siege)
    if character_dd.get() == "Waldo":
        character_label.configure(image=master.waldo)
    elif character_dd.get() == "Wenda":
        character_label.configure(image=master.wenda)
    elif character_dd.get() == "Wizard":
        character_label.configure(image=master.wizard)
    elif character_dd.get() == "Odlaw":
        character_label.configure(image=master.odlaw)
    elif character_dd.get() == "Woof":
        character_label.configure(image=master.woof)


def resize_image(image_location, size_set):
    image = Image.open(image_location)
    image = image.resize(size_set, Image.ANTIALIAS)
    return image


city_image = r"Puzzle Images\Waldo_City.jpeg"
buffet_image = r"Puzzle Images\Waldo_Buffet.jpeg"
department_image = r"Puzzle Images\Waldo_Department_Store.jpeg"
siege_image = r"Puzzle Images\Waldo_Siege.jpeg"
default_image = r"Puzzle Images\puzzle2.jpeg"

waldo_image = r"Target Images\waldo1.jpg"
odlaw_image = r"Target Images\odlaw.jpeg"
wenda_image = r"Target Images\wenda.jpeg"
wizard_image = r"Target Images\wizard.jpeg"
woof_image = r"Target Images\woofs_tail.jpeg"

master = Tk()

master.title("Where's Waldo Application")
master.geometry("1000x1000")
master.resizable(0, 0)

scene_dd = StringVar(master)
scene_dd.set("Buffet")
s_dd = OptionMenu(master, scene_dd, "Buffet", "Department Store", "City", "Siege")
s_dd.grid(row=0, column=0, sticky=W, pady=2)

character_dd = StringVar(master)
character_dd.set("Waldo")
c_dd = OptionMenu(master, character_dd, "Waldo", "Wenda", "Wizard", "Odlaw", "Woof")
c_dd.grid(row=1, column=0, sticky=W, pady=2)

preview_b = Button(master, text="Preview", command=myPreview, width=20)
preview_b.grid(row=0, column=1, sticky=W, pady=2)

search_b = Button(master, text="Search", width=20)
search_b.grid(row=1, column=1, sticky=W, pady=2)

master.default = ImageTk.PhotoImage(resize_image(default_image, (800, 800)))
master.city = ImageTk.PhotoImage(resize_image(city_image, (800, 800)))
master.buffet = ImageTk.PhotoImage(resize_image(buffet_image, (800, 800)))
master.department = ImageTk.PhotoImage(resize_image(department_image, (800, 800)))
master.siege = ImageTk.PhotoImage(resize_image(siege_image, (800, 800)))

scene_label = Label(master, image=master.buffet)
scene_label.grid(row=2, column=0, columnspan=2, rowspan=1, sticky=W, pady=2)

master.waldo = ImageTk.PhotoImage(resize_image(waldo_image, (200, 200)))
master.odlaw = ImageTk.PhotoImage(resize_image(odlaw_image, (200, 200)))
master.wenda = ImageTk.PhotoImage(resize_image(wenda_image, (200, 200)))
master.wizard = ImageTk.PhotoImage(resize_image(wizard_image, (200, 200)))
master.woof = ImageTk.PhotoImage(resize_image(woof_image, (200, 200)))

character_label = Label(master, image=master.waldo)
character_label.grid(row=2, column=3, sticky=W, pady=2)

mainloop()
