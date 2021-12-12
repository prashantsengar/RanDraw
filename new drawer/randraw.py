import collections
import csv
import datetime
import logging
import os
import random
import shutil
import threading
import turtle
from abc import abstractmethod, ABC
from typing import List

import keyboard
import pyautogui
from PIL import Image

temp_path = ''


def create_temp_folder():
    global temp_path
    if ".randtemp" in os.listdir():
        temp_path = ".randtemp"
        return

    try:
        os.mkdir(".randtemp")
        temp_path = ".randtemp"
    except Exception as e:
        logging.warning(e)
        print(e)

        temp_path = ""


def get_canvas_dimensions():
    height, width = open("size.txt").read().split(":")
    height = int(height)
    width = int(width)
    return height, width


class DrawCanvas:
    def __init__(self, height, width, path, data=[]):
        self.HEIGHT = height
        self.WIDTH = width
        self.data = data
        self.started = False
        self.path = path
        self.keys_dict = {}
        self.stamps = []

    def get_x(self):
        return random.randint(-self.WIDTH // 8, self.WIDTH // 8)

    def add_image(self):
        """
    	Add a random image present in the create_folder
    	"""
        files = os.listdir()
        files.remove('temp.gif')
        logging.warning(files)
        if len(files) > 0:
            tries = 0
            while tries < 30:
                try:
                    file = random.choice(files)
                    # print(file)
                    img = Image.open(file)
                    img.resize(
                        (
                            random.randint(self.HEIGHT // 8, self.HEIGHT // 4),
                            random.randint(self.WIDTH // 8, self.WIDTH // 4),
                        )
                    )
                    filename = f'{temp_path}/{datetime.datetime.now().strftime("%Y-%m-%d--%HH-%MM-%SS")}.gif'
                    print(filename)
                    img.save(filename)
                    return filename

                    # show_image()
                    # img = tkinter.PhotoImage(master=screen, file='temp.gif', width = 150, height = 150)
                    # screen.create_image((40, 60), image = img, state = "normal", anchor = tkinter.NW)

                except IOError:
                    tries += 1
        else:
            logging.warning("There is no image")
            return 'temp.gif'

    def view(self, my_turtle, my_mouse):
        logging.warning(f"List before popping: {self.data}")

        if not self.started:
            my_turtle.start()

        logging.warning(f"Saved")

        my_turtle.speed(0)
        data_bak = []

        while self.data:
            fun = self.data.pop()
            data_bak.append(fun)
            if fun == "circle":
                sh = Circle(my_turtle)
                sh.draw()
            elif fun == "inc_circle":
                sh = Circle(my_turtle)
                sh.increase()
            elif fun == "rectangle":
                sh = Rectangle(my_turtle)
                sh.draw()
            elif fun == "inc_rectangle":
                sh = Rectangle(my_turtle)
                sh.increase()
            elif fun == "triangle":
                sh = Triangle(my_turtle)
                sh.draw()
            elif fun == "inc_tri":
                sh = Triangle(my_turtle)
                sh.increase()
            elif fun == "line":
                sh = Line(my_turtle)
                sh.draw()
            elif fun == "inc_line":
                sh = Line(my_turtle)
                sh.increase()

            elif fun == "insert_img":
                sh = CanvasImage(my_turtle)
                sh.draw()

            elif fun == "ellipse":
                sh = Ellipse(my_turtle)
                sh.draw()
            elif fun == "inc_elli":
                sh = Ellipse(my_turtle)
                sh.increase()
            elif fun == "polygon":
                sh = Polygon(my_turtle, sides=0)
                sh.draw()
            elif fun == "inc_polygon":
                sh = Polygon(my_turtle, sides=0)
                sh.increase()
            elif fun == "pentagon":
                sh = Polygon(my_turtle, sides=5)
                sh.draw()
            elif fun == "hexagon":
                sh = Polygon(my_turtle, sides=6)
                sh.increase()
            elif fun == "mouse_stop":
                mouse_positions = my_mouse.draw()
                print(f"Number of mouse positions: {len(mouse_positions)}")
                for position in mouse_positions:
                    my_turtle.goto(position)
                print("finished drawing mouse positions")

            elif fun == "toggle_clr":
                my_turtle.toggle_should_color()
            elif fun == "inc_thick":
                my_turtle.increase_pen_size()
            elif fun == "dec_thick":
                my_turtle.decrease_pen_size()

        logging.warning(f"Fun li after popping: {self.data}")

    def get_keys(self):
        """
    	Get the keys defined in the csv filename
    	"""
        file = open("keys.csv")
        data = csv.reader(file)
        data = list(data)
        logging.warning(data)

        self.keys_dict["save"] = data[0][0]
        self.keys_dict["exit"] = data[1][0]
        self.keys_dict["view"] = data[2][0]
        self.keys_dict["circle"] = data[3][0]
        self.keys_dict["triangle"] = data[4][0]
        self.keys_dict["rectangle"] = data[5][0]
        self.keys_dict["hexagon"] = data[6][0]
        self.keys_dict["polygon"] = data[7][0]
        self.keys_dict["line"] = data[8][0]
        self.keys_dict["pentagon"] = data[9][0]
        self.keys_dict["ellipse"] = data[10][0]
        self.keys_dict["inc_circle"] = data[11][0]
        self.keys_dict["inc_poly"] = data[12][0]
        self.keys_dict["inc_tri"] = data[13][0]
        self.keys_dict["inc_rect"] = data[14][0]
        self.keys_dict["inc_elli"] = data[15][0]
        self.keys_dict["inc_line"] = data[16][0]
        self.keys_dict["insert_img"] = data[17][0]
        self.keys_dict["toggle_clr"] = data[18][0]

        self.keys_dict["inc_thick"] = data[19][0]
        self.keys_dict["dec_thick"] = data[20][0]
        # self.keys_dict['polygon'] = data[6][0]
        self.keys_dict["save_render"] = data[21][0]

        self.keys_dict["combo1"] = data[22][0]
        self.keys_dict["combo1shapes"] = data[22][1].strip(' ').split(' ')
        logging.warning(f'Combo1 shapes: {self.keys_dict["combo1shapes"]}')
        self.keys_dict["combo2"] = data[23][0]
        self.keys_dict["combo2shapes"] = data[23][1].strip(' ').split(' ')
        logging.warning(f'Combo2 shapes: {self.keys_dict["combo2shapes"]}')

        self.keys_dict["realtime"] = data[24][0]
        self.keys_dict["mouse"] = data[25][0]
        self.keys_dict['mouse_stop'] = data[26][0]

    def push_fun(self, fun, my_turtle, my_mouse):
        if type(fun) != list:
            self.data.append(fun)
        else:
            self.data.extend(fun)
        if my_turtle.realtime:
            self.view(my_turtle, my_mouse)

    def save(self, my_turtle, my_mouse):
        self.view(my_turtle, my_mouse)
        ts = my_turtle.getscreen()
        filename = f"{datetime.datetime.now().strftime('%Y-%m-%d--%HH-%MM-%SS')}.eps"
        ts.getcanvas().postscript(file=self.path + filename)
        my_turtle.clear()
        logging.warning("saved everything")

    def key_fun(self, my_turtle, my_mouse):
        try:
            keyboard.add_hotkey(self.keys_dict["save"], self.save, args=(my_turtle, my_mouse,))
            keyboard.add_hotkey(self.keys_dict["view"], self.view, args=(my_turtle, my_mouse,))

            for key in self.keys_dict:
                try:
                    keyboard.add_hotkey(self.keys_dict[key], self.push_fun, args=(key, my_turtle, my_mouse,))
                except:
                    print(key)

            keyboard.add_hotkey(self.keys_dict["realtime"], my_turtle.toggle_realtime)
            keyboard.add_hotkey(self.keys_dict["mouse"], my_mouse.start_recording,
                                args=(self.keys_dict, self.HEIGHT, self.WIDTH))
            while True:
                if keyboard.is_pressed(self.keys_dict["exit"]):
                    break
                pass
        finally:
            print("recorded")
            shutil.rmtree(temp_path)

    def generate_events(self):
        while True:
            if keyboard.is_pressed("ctrl+shift+e"):
                exit()
            elif keyboard.is_pressed("ctrl+shift+s"):
                self.save()
                logging.warning("returned")
            # elif keyboard.is_pressed("ctrl+shift+p"):
            #     send_to_server()
            else:
                yield keyboard.read_event()


def get_color():
    """
        Get RGB values of a random color
    """
    color = (
        random.uniform(0.00, 0.99),
        random.uniform(0.00, 0.99),
        random.uniform(0.00, 0.99),
    )
    # print(color)
    return color


class MyTurtle(turtle.RawTurtle):
    def __init__(self, screen: DrawCanvas):
        self.last_drawn_shape = None
        self.sides = collections.deque(maxlen=12)
        self.last_position = (0, 0)
        self.drawer = screen
        self.color = (0, 0, 0)
        self.last_color = (0, 0, 0)
        self.should_color = True
        self.realtime = False
        self.stamps = []
        self.canvas = None

        # super().__init__(screen)
        # super().__init__()

    def start(self):
        screen = turtle.Screen()
        self.canvas = screen
        super().__init__(screen)
        self.ht()
        self.drawer.started = True

    def get_screen_dimensions(self):
        return self.drawer.HEIGHT, self.drawer.WIDTH

    def randomize_position(self):
        """
        Randomize the position of the turtle
        """
        self.color = get_color()
        self.up()
        self.goto(self.drawer.get_x(), self.drawer.get_x())
        self.down()

    def move_to(self, x, y):
        self.up()
        self.goto(x, y)
        self.down()

    def increase_pen_size(self):
        size = self.pensize()
        self.pensize(size + 1)

    def decrease_pen_size(self):
        size = self.pensize()
        if size > 1:
            self.pensize(size - 1)

    def undo_steps(self, num, abso=False):
        if not abso:
            num = 2 * num + 1

        for __ in range(num):
            turtle.undo()

    def set_last_shape(self, num):
        """
    	Set the last drawn shape equal to the number of sides
    	num=0 -> circle
    	num=3 -> triangle
    	"""
        self.last_drawn_shape = num

    def set_last_side(self, pos):
        """
    	Push the length of side drawn in the deque
    	"""
        self.sides.append(pos)

    def get_last_shape(self) -> int:
        """
    	Get the last drawn shape
    	"""
        return self.last_drawn_shape

    def get_last_side(self) -> int:
        """
    	Get the length of last drawn side of the shape.
    	For circle, it is the radius
    	"""
        if self.sides:
            return self.sides.pop()
        return 40

    def set_last_color(self, col):
        """
    	Set the last used color
    	"""
        if not self.should_color:
            col = (0, 0, 0)
        self.last_color = col

    def get_last_color(self):
        """
    	Get the last used color
    	"""
        return self.last_color

    def toggle_should_color(self):
        """
    	Toggle if color should be used or not
    	"""
        self.should_color = not self.should_color
        # print(self.should_color)
        # View is called here so that the effects take place before the next toggle

    def toggle_realtime(self):
        self.realtime = not self.realtime

    # def draw(self, shape: Shape):
    #     shape.draw(self)


class Shape(ABC):
    def __init__(self, my_turtle: MyTurtle, length=0, color=0):
        self.turtle = my_turtle
        self.length = self.get_length(length)
        self.color = self.get_color(color)
        self.shape: int
        self.undo_steps: List

    def get_length(self, length: int) -> int:
        if not length:
            length = self.turtle.drawer.get_x()
        return length

    def get_color(self, color):
        if not color:
            color = get_color()
        return color

    def pre_draw(self):
        self.turtle.randomize_position()
        color = self.turtle.color if self.turtle.should_color else ""
        print(f'Colouring {color}')
        self.turtle.fillcolor(color)
        self.turtle.begin_fill()

    def post_draw(self):
        self.turtle.end_fill()
        self.turtle.set_last_color(self.color)
        self.turtle.set_last_shape(self.shape)
        self.turtle.set_last_side(self.length)

    def get_last_details(self):
        if self.turtle.get_last_shape() == self.shape:
            self.length = self.turtle.get_last_side()
            self.color = self.turtle.get_last_color()
            return True
        else:
            return False

    def increase(self):
        if not self.get_last_details():
            return

        self.turtle.undo_steps(*self.undo_steps)
        self.increase_length()
        self.draw()

    def increase_length(self):
        self.length = self.length * random.uniform(1, 3)

    @abstractmethod
    def draw(self):
        pass


class Circle(Shape):
    def __init__(self, my_turtle, *args, **kwargs):
        self.shape = 1
        self.undo_steps = [4, True]
        super(Circle, self).__init__(my_turtle, *args, **kwargs)

    def draw(self):
        self.pre_draw()

        self.turtle.circle(self.length)

        self.post_draw()


class Rectangle(Shape):
    def __init__(self, my_turtle, breadth=0, turn=0, *args, **kwargs):
        super().__init__(my_turtle, *args, **kwargs)
        self.breadth = self.get_length(breadth)
        self.turn = turn
        self.shape = 4 
        self.undo_steps = [10, True]

    def draw(self):
        self.pre_draw()

        for _ in range(2):
            self.turtle.forward(self.length)
            self.turtle.left(90) if self.turn == 0 else self.turtle.right(90)
            self.turtle.forward(self.breadth)
            self.turtle.left(90) if self.turn == 0 else self.turtle.right(90)

        self.post_draw()

    def post_draw(self):
        turtle.end_fill()
        self.turtle.set_last_color(self.color)
        self.turtle.set_last_shape(self.shape)
        self.turtle.set_last_side([self.length, self.breadth])

    def get_last_details(self):
        if self.turtle.get_last_shape() == self.shape:
            self.length, self.breadth = self.turtle.get_last_side()
            self.color = self.turtle.get_last_color()
            return True
        else:
            return False

    def increase_length(self):
        self.length = self.length * random.uniform(1, 3)
        self.breadth = self.breadth * random.uniform(1, 3)


class Ellipse(Shape):
    def __init__(self, my_turtle, turn=0, *args, **kwargs):
        super().__init__(my_turtle, *args, **kwargs)
        self.radius = self.get_length(0)
        self.turn = turn
        self.shape = 1
        self.undo_steps = [6, True]

    def draw(self):
        self.pre_draw()
        self.turtle.right(45) if self.turn else turtle.left(45)
        for loop in range(2):
            self.turtle.circle(self.radius, 90)
            self.turtle.circle(self.radius / 2, 90)
        self.post_draw()


class Line(Shape):
    def __init__(self, my_turtle, *args, **kwargs):
        self.shape = 0
        self.undo_steps = [0, False]
        super().__init__(my_turtle, *args, **kwargs)

    def draw(self):
        self.pre_draw()

        if random.choice([True, False]):
            return self.draw_full_length_line()

        self.turtle.forward(self.length)
        self.post_draw()

    def draw_full_length_line(self):
        height, width = self.turtle.get_screen_dimensions()

        x = -1 * width
        y = random.randint(-1 * height, height)
        self.turtle.move_to(x, y)

        yn = random.randint(-1 * height, height)
        self.turtle.goto(x, yn)


class Triangle(Shape):
    def __init__(self, my_turtle, *args, **kwargs):
        super().__init__(my_turtle, *args, **kwargs)
        self.shape = 3
        self.undo_steps = [5, True]
        # coods have -> [[x1, y1], [x2, y2], [x3, y3]]
        self.coods = self.get_coods()

    def get_coods(self):
        coods = []
        for _ in range(3):
            coods.append(
                [self.turtle.drawer.get_x(),
                 self.turtle.drawer.get_x()]
            )
        return coods

    def draw(self):
        self.pre_draw()

        turtle.goto(self.coods[1][0], self.coods[1][1])
        turtle.goto(self.coods[2][0], self.coods[2][1])
        turtle.goto(self.coods[0][0], self.coods[0][1])

        self.post_draw()

    def post_draw(self):
        turtle.end_fill()
        self.turtle.set_last_color(self.color)
        self.turtle.set_last_shape(self.shape)
        for cood in self.coods:
            self.turtle.set_last_side(cood)


class Polygon(Shape):
    def __init__(self, my_turtle, *args, **kwargs):
        self.sides = kwargs['sides']
        if self.sides == 0:
            self.sides = random.randint(5, 12)
        self.exteriorAngle = 360 / self.sides
        self.shape = 5
        self.undo_steps = [2 * self.sides + 3, True]
        super().__init__(my_turtle, *args)

    def draw(self):
        self.pre_draw()

        for i in range(self.sides):
            self.turtle.forward(self.exteriorAngle)
            self.turtle.right(self.exteriorAngle)

        self.post_draw()

    def get_last_details(self):
        if self.turtle.get_last_shape() and self.turtle.get_last_shape() >= self.shape:
            self.length = self.turtle.get_last_side()
            self.color = self.turtle.get_last_color()
            return True
        else:
            return False


class CanvasImage:
    def __init__(self, my_turtle: MyTurtle):
        self.turtle = my_turtle
        self.height = random.randint(self.turtle.drawer.HEIGHT // 8, self.turtle.drawer.WIDTH // 4)
        self.width = random.randint(self.turtle.drawer.HEIGHT // 8, self.turtle.drawer.WIDTH // 4)
        self.image = self.add()

    def add(self):
        """
        Add a random image present in the create_folder
        """
        files = os.listdir()
        files.remove('temp.gif')
        logging.warning(files)
        if len(files) > 0:
            tries = 0
            while tries < 30:
                try:
                    file = random.choice(files)
                    img = Image.open(file)
                    img.resize(
                        (
                            self.height, self.width
                        )
                    )
                    filename = f'{temp_path}/{datetime.datetime.now().strftime("%Y-%m-%d--%HH-%MM-%SS")}.gif'
                    print(filename)
                    img.save(filename)
                    return filename
                except IOError:
                    tries += 1
        logging.warning("There is no image")
        return 'temp.gif'

    def draw(self):
        self.turtle.randomize_position()
        self.turtle.canvas.register_shape(self.image)
        self.turtle.shape(self.image)
        stamp = self.turtle.stamp()
        self.turtle.drawer.stamps.append(stamp)


class MouseDrawer:
    def __init__(self):
        self.positions = []

    def record(self, keys_dict, height, width):
        ##        ts = turtle.getscreen()
        ##        mycanvas = ts.getcanvas()
        X, Y = pyautogui.size()
        centre_x, centre_y = X // 2, Y // 2

        while not keyboard.is_pressed(keys_dict['mouse_stop']):
            ##            x, y = mycanvas.winfo_pointerx(), mycanvas.winfo_pointery()
            ##            x = x if x < width else width - 1
            ##            y = y if y < height else height - 1
            x, y = pyautogui.position()
            x -= centre_x
            y -= centre_y

            if self.positions and self.positions[-1] != (x, y):
                self.positions.append((x, y))
            elif not self.positions:
                self.positions.append((x, y))

    def draw(self):
        data = []
        for position in self.positions:
            data.append(position)
        return data

    def start_recording(self, keys_dict, height, width):
        t = threading.Thread(target=self.record, args=(keys_dict, height, width,))
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    create_temp_folder()
    height, width = get_canvas_dimensions()
    path = "myRanDrawings"
    canvas = DrawCanvas(height, width, path)
    canvas.get_keys()

    my_turtle = MyTurtle(canvas)
    mouse = MouseDrawer()

    canvas.key_fun(my_turtle, mouse)
