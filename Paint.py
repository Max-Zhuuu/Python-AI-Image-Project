from tkinter import *
from tkinter.colorchooser import askcolor


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.title("Architect AI Design")
        self.root.geometry('800x1000')
        self.root.resizable(1, 1)
        self.root.minsize(500, 600)
        self.resize()
        self.root.bind('<Configure>', self.resize)

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        #self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        self.triangle_button = Button(self.root, text='triangle', command=self.use_triangle)
        self.triangle_button.grid(row=1, column=0)

        self.rectangle_button = Button(self.root, text='rectangle', command=self.use_rectangle)
        self.rectangle_button.grid(row=2, column=0)

        #self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=3, column=0)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=4, column=0)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=5, column=0)

        self.c = Canvas(self.root, bg='white', width=1000, height=800)
        self.c.grid(row=0, column=1, rowspan=6)

        self.setup()
        self.root.mainloop()

    def resize(self):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        self.root.geometry(f'{w}x{h}')

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.x1 = None
        self.x2 = None
        self.x3 = None
        self.y1 = None
        self.y2 = None
        self.y3 = None
        self.button_pressed = 1   # 1 = pen, 2 = triangle, 3 = rectangle
        self.points = []
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<Button-1>', self.pressed )
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.button_pressed = 1
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def pressed(self, event):
        self.old_x = event.x
        self.old_y = event.y
        self.x1 = event.x
        self.y1 = event.y

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.button_pressed == 1:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.old_x = event.x
            self.old_y = event.y
        elif self.button_pressed == 2:
            self.get_coords2(event)
            self.points = [self.x1, self.y1, self.x2, self.y2, self.x3, self.y3]
            self.c.create_polygon(self.points, width=self.line_width, fill=paint_color)
            self.reset
        elif self.button_pressed == 3:
            self.get_coords(event)
            self.c.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=paint_color, width=self.line_width)
            self.reset

    def reset(self, event):
        self.old_x, self.old_y = None, None
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
        self.x2, self.y2 = event.x, event.y

    # triangle button
    def use_triangle(self):
        self.button_pressed = 2
        self.activate_button(self.triangle_button)
        #self.points = [self.x1, self.y1, self.x2, self.y2, self.x3, self.y3]
        #self.c.create_polygon(self.points, width=self.choose_size_button.get())
        #self.reset

    # rectangle button
    def use_rectangle(self):
        self.button_pressed = 3
        self.activate_button(self.rectangle_button)
        #self.c.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.color, width=self.choose_size_button.get())
        #self.reset



if __name__ == '__main__':
    Paint()
