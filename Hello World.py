"""
import os
import shutil
from tkinter import *
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image, ImageDraw
"""

from concurrent.futures.process import _MAX_WINDOWS_WORKERS
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter.colorchooser import askcolor


def on_resize(self,event):
    # determine the ratio of old width/height to new width/height
    wscale = float(event.width)/self.width
    hscale = float(event.height)/self.height
    self.width = event.width
    self.height = event.height
    # resize the canvas 
    self.config(width=self.width, height=self.height)
    # rescale all the objects tagged with the "all" tag
    self.scale("all",0,0,wscale,hscale)

"""
def resize(self):
    if ( app_window.geometry != '910x600'):
        w = app_window.winfo_width
        h = app_window.winfo_height
        app_window.geometry(f'{w}x{h}')
"""

# base window
app_window = Tk()
app_window.title("Python Project")
app_window.geometry('910x600')
app_window.resizable(1, 1)
app_window.minsize(910, 600)
app_window.bind('<Configure>', on_resize)

# generating canvas
class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = app_window

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)
        
        self.triangle_button = Button(self.root, text='triangle', command=self.use_triangle)
        self.triangle_button.grid(row=1, column=0)

        self.rectangle_button = Button(self.root, text='rectangle', command=self.use_rectangle)
        self.rectangle_button.grid(row=2, column=0)    

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=3, column=0)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=4, column=0)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=5, column=0)

        # generating canvas
        self.c = Canvas(self.root, bg='white', width=400, height=600)
        self.c.grid(row=0, rowspan=6, column = 1)

        # generating right screen
        self.screen_right = Canvas(self.root, bg="white", width=400, height=600)
        self.screen_right.grid(row=0, rowspan=6, column= 2, sticky=W)

        self.addtag_all("all")
        self.setup()
        self.root.mainloop()

    def setup(self):
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<ButtonPress-1>', self.get_coords)
        self.c.bind('<ButtonRelease-1>', self.get_coords2)

    # pen button
    def use_pen(self):
        self.activate_button(self.pen_button)

    # coordinates function 2
    def get_coords2(self, event):
        # get x2, y2 co-ordinates
        self.x2, self.y2 = event.x, event.y
        # get x3, y3 coordinates
        self.x3 = ((2*self.x1) - self.x2)
        self.y3 = self.y2

    # coordinates function 1
    def get_coords(self, event):
        # get x1, y1 co-ordinates
        self.x1, self.y1 = event.x, event.y

    # triangle button
    def use_triangle(self):
        self.activate_button(self.triangle_button)
        self.points = [self.x1, self.y1, self.x2, self.y2, self.x3, self.y3]
        self.c.create_polygon(self.points, width=self.choose_size_button.get())
        self.reset

    # rectangle button
    def use_rectangle(self):
        self.activate_button(self.rectangle_button)
        self.c.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.color, width=self.choose_size_button.get())
        self.reset

    # color chooser button
    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    # eraser button
    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    # makes buttons sunken or raised when pressed and detects for eraser mode
    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    # drawing code
    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    # clears variable input after button use
    def reset(self, event):
        # resets coordinates
        self.var_list = [self.x1, self.x2, self.x3, self.y1, self.y2, self.y3]
        for x in self.var_list:
            x = None
        # resets points for triangle
        self.points = []

if __name__ == '__main__':
    Paint()