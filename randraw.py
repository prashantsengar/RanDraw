import keyboard
import turtle as tur
# import turtle
import random
from PIL import Image
import os
import logging
import sys
import tkinter
import datetime
import collections
import shutil

logging.basicConfig(filename='log.log', filemode='w', level='WARNING', format='%(name)s - %(levelname)s - %(message)s')

logging.warning('hello')
data = []

HEIGHT, WIDTH = open('size.txt').read().split(':')
HEIGHT = int(HEIGHT)
WIDTH = int(WIDTH)
started=False
# turtle = 0
tk = 0
ti=0
stamps=[]
should_color = True

screen=0
keys_dict = {}
IMAGE=None
last_drawn_shape=0
last_position=(0,0)
sides = collections.deque(maxlen=12)
temp_path = ''

def create_temp_folder():
	global temp_path
	if '.randtemp' in os.listdir():
		temp_path = '.randtemp'
		return
	
	try:
		os.mkdir('.randtemp')
		temp_path = '.randtemp'
	except Exception as e:
		logging.warning(e)
		print(e)
		
		temp_path = ''


def get_x():
    """returns random integer with max and min width"""
    return random.randint(-WIDTH // 8, WIDTH // 8)



def start():
	"""
	Creates a canvas and hides the turtle
	"""
    global screen
    screen = tur.Screen()
    global turtle
    turtle = tur.RawTurtle(screen)
    turtle.ht()
    global started
    started = True


def randomize_position():
	"""
	Randomize the position of the turtle
	"""
    global turtle
    turtle.color(get_color())
    turtle.up()
    turtle.goto(get_x(), get_x())
    turtle.down()

def move_to(x,y):
	turtle.up()
	turtle.goto(x,y)
	turtle.down()

def undo_steps(num, abso=False):
	if not abso:
		num = 2*num + 1

	global turtle
	for __ in range(num):
		turtle.undo()

def set_last_shape(num):
	"""
	Set the last drawn shape equal to the number of sides
	num=0 -> circle
	num=3 -> triangle
	"""
	global last_drawn_shape
	last_drawn_shape = num

def set_last_side(pos):
	"""
	Push the length of side drawn in the deque
	"""
	global sides
	sides.append(pos)

def get_last_shape():
	"""
	Get the last drawn shape
	"""
	global last_drawn_shape
	try:
		return last_drawn_shape
	except:
		return

def get_last_side():
	"""
	Get the length of last drawn side of the shape. 
	For circle, it is the radius
	"""
	global sides
	try:
		return sides.pop()
	except:
		return 40

def set_last_color(col):
	"""
	Set the last used color
	"""
	global last_color
	last_color = col

def get_last_color():
	"""
	Get the last used color
	"""
	global last_color
	return last_color

def get_color():
	"""
	Get RGB values of a random color
	"""
	color = (random.uniform(0.00,0.99), random.uniform(0.00,0.99), random.uniform(0.00,0.99))
	return color

def toggle_should_color():
	"""
	Toggle if color should be used or not
	"""
	global should_color
	if should_color:
		should_color=False
	else:
		should_color=True
	#View is called here so that the effects take place before the next toggle
	view()

def draw_rectangle(color=False, length=False, breadth=False, turn=0):
	if not length:
		#If length is not given, draw a rectangle of
		#random size
		randomize_position()
		length = get_x()
		breadth = get_x()
		color = get_color()
		logging.warning("not length")

	global turtle
	set_last_side(breadth)
	set_last_side(length)
	set_last_shape(4)
	set_last_color(color)

	global should_color
	if not should_color:
		color = ''
	turtle.fillcolor(color)
	turtle.begin_fill()
	turtle.forward(length)
	turtle.left(90) if turn == 0 else turtle.right(90)
	turtle.forward(breadth)
	turtle.left(90) if turn == 0 else turtle.right(90)
	turtle.forward(length)
	turtle.left(90) if turn == 0 else turtle.right(90)
	turtle.forward(breadth)
	turtle.left(90) if turn == 0 else turtle.right(90)
	turtle.end_fill()

def increase_rectangle():
	"""
	Increase the size of the rectangle
	"""
	if get_last_shape()==4:
		length = get_last_side()
		breadth = get_last_side()
		color = get_last_color()

		undo_steps(10, abso=True)
		factor = random.uniform(1.01,2.99)
		draw_rectangle(color, length* factor, breadth* factor)


def draw_ellipse():
	"""
	Draws an ellipse
	"""
	randomize_position()
	radius = get_x()
	choice = random.choice([0,1])
	set_last_side(choice)
	set_last_side(radius)
	set_last_shape(1)

	color = get_color()
	set_last_color(color)
	turtle.right(45) if choice else turtle.left(45)

	global should_color
	if not should_color:
		color = ''
	turtle.fillcolor(color)
	turtle.begin_fill()
	for loop in range(2):
	    turtle.circle(radius,90)
	    turtle.circle(radius/2,90)
	turtle.end_fill()

def increase_ellipse():
	"""
	Increase the size of the last drawn ellipse
	"""
	if get_last_shape()==1:
		radius = get_last_side()#Get the radius to be used
		choice = get_last_side()#Get the direction, left or right
		set_last_side(choice)#Then set it again for use again
		undo_steps(6, abso=True)

		color = get_last_color()
		radius = radius* random.uniform(1.01,2.99)
		global turtle
		set_last_side(radius)
		set_last_shape(1)
		set_last_color(color)
		
		global should_color
		if not should_color:
			color = ''
		turtle.fillcolor(color)
		turtle.begin_fill()
		for loop in range(2):
		    turtle.circle(radius,90)
		    turtle.circle(radius/2,90)
		turtle.end_fill()

def draw_line():
	"""
	Draw a line of random length
	"""
	randomize_position()
	length = abs(get_x())

	set_last_side(length)
	set_last_shape(0)
	global turtle
	turtle.forward(length)

def increase_line():
	"""
	Increase the length of the last drawn line
	"""
	if get_last_shape()==0:
		length = get_last_side()
		length = length* random.uniform(1.01,2.99)
		undo_steps(0)
		
		set_last_shape(0)
		set_last_side(length)
		global turtle
		turtle.forward(length)

		logging.warning("done")

def draw_triangle():
	"""
	Draw a triangle of random size
	"""
    global turtle
    color = get_color()
    randomize_position()

    x1, y1 = get_x(), get_x()
    x2, y2 = get_x(), get_x()
    x3, y3 = get_x(), get_x()

    set_last_side((x1,y1))
    set_last_side((x2,y2))
    set_last_side((x3,y3))
    set_last_shape(3)
    set_last_color(color)

    turtle.up()
    turtle.goto(x1, y1)
    turtle.down()
    global should_color
    if not should_color:
    	color = ''
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.goto(x2, y2)
    turtle.goto(x3, y3)
    turtle.goto(x1, y1)
    turtle.end_fill()

def increase_triangle():
	"""
	Increase the size of the last drawn triangle
	"""
	if get_last_shape()==3:
		logging.warning("yes")
		undo_steps(5, abso=True)
		x1,y1 = get_last_side()
		x2,y2 = get_last_side()
		x3, y3 = get_last_side()

		x1,y1 = random.uniform(1.01, 2.9) * x1, random.uniform(1.01, 2.9) * y1
		x2,y2 = random.uniform(1.01, 2.9) * x2, random.uniform(1.01, 2.9) * y2
		x3,y3 = random.uniform(1.01, 2.9) * x3, random.uniform(1.01, 2.9) * y3

		color = get_last_color()

		set_last_side((x1,y1))
		set_last_side((x2,y2))
		set_last_side((x3,y3))
		set_last_shape(3)
		set_last_color(color)
		global turtle
		turtle.up()
		turtle.goto(x1, y1)
		turtle.down()
		global should_color
		if not should_color:
			color = ''
		turtle.fillcolor(color)
		turtle.begin_fill()
		turtle.goto(x2, y2)
		turtle.goto(x3, y3)
		turtle.goto(x1, y1)
		turtle.end_fill()


def increase_circle():
	"""
	Increase the length of the last draw circle
	"""
	if get_last_shape()==1:
		radius = get_last_side()
		undo_steps(4, abso=True)
		global turtle
		draw_circle(radius * random.uniform(1,3))


def draw_circle(radius=False):
	"""
	Draw a circle
	"""
	global turtle
	if not radius:
		radius = min(get_x(), get_x())
		randomize_position()
		color = get_color()

		global should_color
		if not should_color:
			color=''
		set_last_color(color)
		turtle.fillcolor(color)
	set_last_shape(1)

	set_last_side(radius)
	turtle.begin_fill()
	turtle.circle(radius)
	turtle.end_fill()

def draw_polygon(num_of_sides=0):
	"""
	Draw a regular polygon
	"""
    global turtle
    randomize_position()
    if num_of_sides==0:
	    num_of_sides = random.randint(4, 12)

    set_last_shape(num_of_sides)

    length = min(get_x(), get_x())

    set_last_side(length)
    color = get_color()
    set_last_color(color)

    exteriorAngle = 360 / num_of_sides
    global should_color
    if not should_color:
    	color = ''
    turtle.fillcolor(color)
    turtle.begin_fill()
    for i in range(num_of_sides):
        turtle.forward(length)
        turtle.right(exteriorAngle)
    turtle.end_fill()

def increase_polygon():
	"""
	Increase the last drawn polygon's size
	"""
	if get_last_shape() > 4:
		num_of_sides = get_last_shape()
		color = get_last_color()

		set_last_color(color)
		undo_steps(2*num_of_sides+3,abso=True)
		length = random.uniform(1.1,2.9) * get_last_side()
		set_last_side(length)
		set_last_shape(num_of_sides)
		exteriorAngle = 360 / num_of_sides

		global should_color
		if not should_color:
			color = ''
		turtle.fillcolor(color)
		turtle.begin_fill()
		for i in range(num_of_sides):
			turtle.forward(length)
			turtle.right(exteriorAngle)
		turtle.end_fill()

def add_image():
	"""
	Add a random image present in the create_folder
	"""
	files = os.listdir()
	logging.warning(files)
	if len(files)>0:
		global screen
		global turtle
		global HEIGHT, WIDTH

		tries=0
		while tries<30:
			try:
				file = random.choice(files)
				print(file)
				img = Image.open(file)
				img.resize((random.randint(HEIGHT//8,HEIGHT//4),random.randint(WIDTH//8,WIDTH//4)))
				filename = f'{temp_path}/{datetime.datetime.now().strftime("%Y-%m-%d--%HH-%MM-%SS")}.gif'
				print(filename)
				img.save(filename)
				return filename

				# show_image()
				# img = tkinter.PhotoImage(master=screen, file='temp.gif', width = 150, height = 150)
				# screen.create_image((40, 60), image = img, state = "normal", anchor = tkinter.NW)
				
			except IOError:
				tries+=1
	else:
		logging.warning("There is no image")

def show_image():
	global turtle
	global screen
	screen.register_shape('temp.gif')
	turtle.shape('temp.gif')
	turtle.st()
	print("done")

def paste_image(file):
	global path
	add_image()
	img = Image.open(path+file)
	im = Image.open('temp.gif')
	img.paste(im)
	img.save(path+f'{file.split(".")[0]}.png')


def insert_image():
	# global ti
	img = add_image()
	ti = tur.Turtle()
	ti.color(get_color())
	ti.up()
	ti.goto(get_x(), get_x())
	ti.down()
	global screen
	screen.register_shape(img)
	ti.shape(img)
	ti.stamp()
	global stamps
	stamps.append(ti.stamp())
	# print(stamps)


def save():
    global turtle
    view()
    ts = turtle.getscreen()
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d--%HH-%MM-%SS')}.eps"
    ts.getcanvas().postscript(file=path+filename)
    tur.clearscreen()
    logging.warning('saved everything')



def view():
	global data
	logging.warning(f'Fun li before popping: {data}')
	global started
	if not started:
		start()
	logging.warning(f'Saved')
	global turtle
	turtle.speed(0)

	while data:
		fun = data.pop()
		data_bak.append(fun)
		if fun == 'c':
		    draw_circle()
		elif fun == 'r':
		    draw_rectangle()
		elif fun == 'p':
		    draw_polygon()
		elif fun == 'h':
		    draw_polygon(6)
		elif fun == 't':
		    draw_triangle()
		elif fun == 'm':
		    draw_polygon(5)
		elif fun == 'i':
			increase_circle()
		elif fun == 'd':
			increase_rectangle()
		elif fun == 'y':
			increase_triangle()
		elif fun == 'f':
			increase_polygon()
		elif fun=='e':
			draw_ellipse()
		elif fun=='l':
			draw_line()
		elif fun=='q':
			increase_ellipse()
		elif fun=='w':
			increase_line()
		elif fun=='a':
			insert_image()
			# pass
		elif fun=='x':
			toggle_should_color()

	logging.warning(f'Fun li after popping: {data}')
	
def exit():
    print("exiting")
    sys.exit(0)

def generate_events():
    while True:
        if keyboard.is_pressed('ctrl+shift+e'):
            exit()
        elif keyboard.is_pressed('ctrl+shift+s'):
            global data
            save()
            logging.warning("returned")
        elif keyboard.is_pressed('ctrl+shift+p'):
            send_to_server()
        else:
            yield keyboard.read_event()

def show(data):
    logging.warning(str(data))


def push_fun(fun):
    global data
    data.append(fun)


def get_keys():
	"""
	Get the keys defined in the csv filename
	"""
	import csv
	global keys_dict

	file = open('keys.csv')
	data = csv.reader(file)
	data = list(data)
	logging.warning(data)

	keys_dict['save'] = data[0][0]
	keys_dict['exit'] = data[1][0]
	keys_dict['view'] = data[2][0]
	keys_dict['circle'] = data[3][0]
	keys_dict['triangle'] = data[4][0]
	keys_dict['rectangle'] = data[5][0]
	keys_dict['hexagon'] = data[6][0]
	keys_dict['polygon'] = data[7][0]
	keys_dict['line'] = data[8][0]
	keys_dict['pentagon'] = data[9][0]
	keys_dict['ellipse'] = data[10][0]
	keys_dict['inc_circle'] = data[11][0]
	keys_dict['inc_poly'] = data[12][0]
	keys_dict['inc_tri'] = data[13][0]
	keys_dict['inc_rect'] = data[14][0]
	keys_dict['inc_elli'] = data[15][0]
	keys_dict['inc_line'] = data[16][0]
	keys_dict['insert_img'] = data[17][0]
	keys_dict['toggle_clr'] = data[18][0]0

def key_fun():
    try:
        global keys_dict

        data = []
        keyboard.add_hotkey(keys_dict['save'], save)
        keyboard.add_hotkey(keys_dict['view'], view)
        keyboard.add_hotkey(keys_dict['circle'], push_fun, args=('c',))
        keyboard.add_hotkey(keys_dict['triangle'], push_fun, args=('t',))
        keyboard.add_hotkey(keys_dict['hexagon'], push_fun, args=('h',))
        keyboard.add_hotkey(keys_dict['polygon'], push_fun, args=('p',))
        keyboard.add_hotkey(keys_dict['rectangle'], push_fun, args=('r',))
        keyboard.add_hotkey(keys_dict['pentagon'], push_fun, args=('m',))
        keyboard.add_hotkey(keys_dict['inc_circle'], push_fun, args=('i',))
        keyboard.add_hotkey(keys_dict['inc_rect'], push_fun, args=('d',))
        keyboard.add_hotkey(keys_dict['inc_poly'], push_fun, args=('f',))
        keyboard.add_hotkey(keys_dict['inc_tri'], push_fun, args=('y',))
        keyboard.add_hotkey(keys_dict['ellipse'], push_fun, args=('e',))
        keyboard.add_hotkey(keys_dict['inc_elli'], push_fun, args=('q',))
        keyboard.add_hotkey(keys_dict['line'], push_fun, args=('l',))
        keyboard.add_hotkey(keys_dict['inc_line'], push_fun, args=('w',))
        keyboard.add_hotkey(keys_dict['insert_img'], push_fun, args=('a',))
        keyboard.add_hotkey(keys_dict['toggle_clr'], toggle_should_color)
        while True:
            if keyboard.is_pressed(keys_dict['exit']):
                break
            pass
    finally:
        print('recorded')
        shutil.rmtree('.randtemp')

path='myRanDrawings/'

def create_folder():
	if 'myRanDrawings' in os.listdir():
		return
	try:
		os.mkdir('myRanDrawings')
	except:
		global path
		path = ''


if __name__ == '__main__':

	create_folder()
	create_temp_folder()
	get_keys()
	key_fun()
