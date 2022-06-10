from encodings import utf_8
from turtle import Turtle, Screen
import os
import random
from math import isclose
import pynput
from threading import Thread


x, y = 0, 0
SPEEDOF = 1
Counter = 0
size = 1
name = "test"
path = "\\".join(__file__.split("\\")[:-1]) + "\\"


# tries to make a directory to contain the files
try:
    os.mkdir(path + name)
except FileExistsError:
    name = name + f"{random.randint(0, 100000000000000000000000)}"
    os.mkdir(path + name)


rendercode = [
    "from turtle import *\n",
    "from math import isclose\n",
    "#change this value for a faster but less acurate render\n",
    "detail = 100\n",
    "\n",
    "detail = 100 - detail\n",
    f"name = '{name}'\n",
    "path = '\\\\'.join(__file__.split('\\\\')[:-1]) + '\\\\'\n",
    "screen = Screen()\n",
    "x, y = 0, 0\n",
    "i, j = 0, 0\n",
    "\n",
    "t = Turtle()\n",
    "t.speed('fastest')\n",
    "t.hideturtle()\n",
    "target = path + name + '.txt'\n",
    "\n",
    "with open(target, 'r') as f:\n",
    "    lines = f.readlines()\n",
    "    strlines = ''.join(f.readlines())\n",
    "\n",
    "\n",
    "       \n",
    "for line in lines:\n",
    "    if line.split('(')[0] == 't.goto':\n",
    "        #extracts the coordinates from the lines\n",
    "        newline = line.split('(')\n",
    "        newline.pop(0)\n",
    "        newline = ''.join(newline).split(')')\n",
    "        newline.pop(1)\n",
    "        newline = ''.join(newline)\n",
    "        newline = newline.split(',')\n",
    "\n",
    "        #assigns i and j the coords\n",
    "        try:\n",
    "            i , j = float(newline[0]), float(newline[1])\n",
    "        except: pass\n",
    "\n",
    "\n",
    "        #check for proximity\n",
    "        if not isclose(x, i, abs_tol=detail):\n",
    "            exec(line)\n",
    "            x = i\n",
    "        elif not isclose(y, j, abs_tol=detail):\n",
    "            exec(line)\n",
    "            y = j\n",
    "    else:\n",
    "        exec(line)\n",
    "       \n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "screen.mainloop()",
]


# turtle parameters
ws = Screen()
t = Turtle()
t.speed("fastest")
t.shape("circle")
t.turtlesize(0.1)


# writes the renderer
with open(path + name + "\\" + name + "_renderer.py", "w") as f:
    f.writelines(rendercode)

# adds the new directory to the name
name = path + name + "\\" + name


# writes the first thing to set things of
with open(name + ".txt", "w") as f:
    f.write("")


def mouse_tp(i, j):
    """this is the function that teleports the turtle to the mouse"""
    # execute actions on the viewer

    t.penup()
    t.goto(i, j)
    t.pendown()

    # log the actions
    with open(name + ".txt", "a") as f:
        f.write("t.penup()\n")
        f.write(f"t.goto({i},{j})\n")
        f.write("t.pendown()\n")


def drag(i, j):
    """it keeps the turtle with the mouse"""
    global x, y

    # execute actions on the viewer
    t.ondrag(None)
    t.goto(i, j)
    t.ondrag(drag)

    # log the actions
    with open(name + ".txt", "a") as f:

        if not isclose(x, i, abs_tol=SPEEDOF):
            f.write(f"t.goto({i},{j})\n")
            x = i
        elif not isclose(y, j, abs_tol=SPEEDOF):
            f.write(f"t.goto({i},{j})\n")
            y = j


def start():
    """it starts the listeners to keep track of the actions"""
    listener1 = pynput.keyboard.Listener(on_press=on_press)
    listener1.start()
    listener2 = pynput.mouse.Listener(on_scroll=on_scroll)
    listener2.start()
    listener1.join()


def on_scroll(event, meaningshit, megashit, orientation):
    """it defines what to do when the mouse scrolls"""
    global size

    if orientation > 0:
        size = size + 1
        t.pensize(size)
        t.turtlesize(size / 20)

    elif orientation < 0:
        if size != 1:
            size = size - 1
        t.pensize(size)
        t.turtlesize(size / 20)

    with open(name + ".txt", "a") as f:
        f.write(f"t.pensize('{size}')\n")


def on_press(event):
    """defines what to do when the mouse is pressed"""
    global Counter

    if event == pynput.keyboard.Key.up:
        color = ""
        Counter += 1

        if Counter > 4:
            Counter = 0

        if Counter == 0:
            t.color("black")
            color = "black"

        elif Counter == 1:
            t.color("red")
            color = "red"

        elif Counter == 2:
            t.color("green")
            color = "green"

        elif Counter == 3:
            t.color("yellow")
            color = "yellow"

        elif Counter == 4:
            t.color("orange")
            color = "orange"

        # logs the color
        with open(name + ".txt", "a") as f:
            f.write(f"t.color('{color}')\n")


for i in range(1):
    tr = Thread(target=start)
    tr.start()


ws.onclick(mouse_tp)
t.ondrag(drag)
ws.mainloop()
