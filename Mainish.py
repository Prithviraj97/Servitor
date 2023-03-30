from tkinter import *
from Testing import *
from robot_info import *
import RPi.GPIO as gpio
import time
from time import sleep
from collections import deque


compass = dict({'North': 0, 'East': 1, 'South': 2, 'West': 3})
robot = Robot()
g = Graph()
num_nodes = 5
ratio = 0.2 #ratio formatted as seconds/feet


def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT) 
    gpio.setup(24, gpio.OUT)
    gpio.output(17, False)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)
    
    
def forward(tf):
    init()
    gpio.output(17, True)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(tf)
    gpio.cleanup()

def right_pivot(tf):
    init()
    gpio.output(17, True)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(tf)
    gpio.cleanup()
    
def left_pivot(tf):
    init()
    gpio.output(17,True)
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(tf)
    gpio.cleanup()


##########      BEGINNING OF GUI SECTION     ##########

window = Tk()
window.title("Waypoint Selector")
window.geometry("1050x650")
image = PhotoImage(file="WestWingDrew.png")
image_label = Label(
    image = image
)
image_label.place(x=360, y=170)
cur_position = Label(
    text="Current Location: Room " + g.get_node(robot.get_position()).get_name(),
    font="Helvetica 16 bold",
    width=35,
    height=5,
    bg="#a9a9a9",
    fg="black")
cur_position.place(x=350, y=25)
orders_button = Button(
    command=lambda: [reverse(3)],
    text="Deliver Orders",
    font="Helvetica 12 bold",
    width=20,
    height=5,
    bg="green",
    fg="white")
orders_button.place(x=830, y=25)
prompt_label = Label(
    text = "Select a destination for the robot.",
    font="Helvetica 12 bold",
    width=30,
    height=3,
    bg="#a9a9a9",
    fg="black")
prompt_label.place(x=25, y=25)
button0 = Button(
    command=lambda: [instruction(0),changetext(button0),changecolor(button0)],
    text="Room 320",
    font="Helvetica 12 bold",
    width=30,
    height=3,
    bg="red",
    fg="white")
button0.place(x=25, y=110)
button1 = Button(
    command=lambda: [instruction(1),changetext(button1),changecolor(button1)],
    text="Room 317",
    font="Helvetica 12 bold",
    width=30,
    height=3,
    bg="blue",
    fg="white")
button1.place(x=25, y=205)
button2 = Button(
    command=lambda: [instruction(2),changetext(button2),changecolor(button2)],
    text="Rooms 311-316",
    font="Helvetica 12 bold",
    width=30,
    height=3,
    bg="blue",
    fg="white")
button2.place(x=25, y=300)
button3 = Button(
    command=lambda: [instruction(3),changetext(button3),changecolor(button3)],
    text="West Wing Water Fountain",
    font="Helvetica 12 bold",
    width=30,
    height=3,
    bg="blue",
    fg="white")
button3.place(x=25, y=395)
button4 = Button(
    command=lambda: [instruction(4),changetext(button4),changecolor(button4)],
    text="West Wing Main Hallway",
    font="Helvetica 12 bold",
    width=30,
    height=3,
    bg="blue",
    fg="white", )
button4.place(x=25, y=490)


def changetext(b):
    cur_position.config(text = "Current Location: " + b['text'])
    cur_position.config(font = "Helvetica 16 bold")


def changecolor(b):
    button0.config(bg = "blue")
    button1.config(bg = "blue")
    button2.config(bg = "blue")
    button3.config(bg = "blue")
    button4.config(bg = "blue")
    b.config(bg = "red")


##########      END OF GUI SECTION     ##########

def instruction(location):
    if location == robot.get_position():
        return print("Already at desired location.")
    pathway = []
    visited = []
    path = deque()
    
    if getBFSSolution(robot.get_position(),location, visited, path):
       pathway=list(path)

    #[1, 2, 3]
    
    if robot.in_room():
        leave_room()
    
    while robot.get_position() is not location:
        i = 0
        desired_position = pathway[i+1]
        edges = g.get_node(robot.get_position()).get_connections()
        index = 0
        for j in range(len(edges)):
            if edges[j].get_index() == desired_position:
                index = j
        direction = edges[index].get_direction()
        #print("direction from edges[index].get_direction(): " + direction)
        distance = edges[index].get_distance()
        #print("distance from edges[index].get_distance(): " + str(distance))
        face_robot(direction)
        print("Traverse: " + str(distance) + " feet")
        forward(time_travel(distance)) #new code
        time.sleep(1)
        #prithvi's code
        robot.change_position(desired_position)
        pathway.pop(0)
        
    if robot.get_position() == location:
        if g.get_node(location).get_doorway_direction() != ' ':
            face_robot(g.get_node(location).get_doorway_direction())
            robot.change_in_room(True)
            print("robot has entered the room")
            forward(time_travel(g.get_node(location).get_hallway_width())) #new code
            time.sleep(1)
       
'''
def find_path(start, goal):
    start_index = start
    goal_index = goal
    print("starting node: " + g.get_node(start_index).get_name())
    print("goal node: " + g.get_node(goal_index).get_name())
    if g.get_node(start_index).num_edges() == 1:
        path = []
        visited = []
        path.append(start_index)
        visited.append(start_index)
        queue = g.get_node(start_index).get_connections().copy()
        while queue:
            cur_index = queue.pop(0).get_index()
            path.append(cur_index)
            visited.append(cur_index)
            if cur_index == goal_index:
                return path
            new_connections = g.get_node(cur_index).get_connections().copy()
            for i in new_connections:
                if i.get_index() in visited:
                    continue
                else:
                    queue.append(i)
    if g.get_node(start_index).num_edges() == 2:
        initial_connections = g.get_node(start_index).get_connections().copy()
        first_path = initial_connections[0]
        path = []
        visited = []
        path.append(start_index)
        visited.append(start_index)
        queue = [first_path]
        while queue:
            cur_index = queue.pop(0).get_index()
            path.append(cur_index)
            visited.append(cur_index)
            if cur_index == goal_index:
                return path
            new_connections = g.get_node(cur_index).get_connections().copy()
            for i in new_connections:
                if i.get_index() not in visited:
                    queue.append(i)
        second_path = initial_connections[1]
        path = []
        visited = []
        path.append(start_index)
        visited.append(start_index)
        queue = [second_path]
        while queue:
            cur_index = queue.pop(0).get_index()
            path.append(cur_index)
            visited.append(cur_index)
            if cur_index == goal_index:
                return path
            new_connections = g.get_node(cur_index).get_connections().copy()
            for i in new_connections:
                if i.get_index() in visited:
                    continue
                else:
                    queue.append(i)
'''
#   face_robot() takes in the direction the robot needs to face to reach the next node in its traversal
def face_robot(direct):
    counter = 0
    cur_dir = robot.get_direction()
    goal_dir = direct
    if cur_dir == goal_dir:
        return
        print("No change in direction.")
    else:
        print("Direction Change Imminent.")
        print("Current Direction: " + str(cur_dir))
        print("Required Direction: " + str(goal_dir))
        #check for optimal turn
        #if optimal_turn(cur_dir,goal_dir):
        #    rotate_left(cur_dir)
        #    return
        rotate_right(cur_dir,goal_dir)


#   rotate_right() takes in the direction the robot is facing and the desired direction
def rotate_right(start, end):
    #represents an index value for a direction
    #character is key and integer is value
    key_list = list(compass.keys())
    i = compass[start]
    while not (robot.get_direction() == end):
        print("Execute right turn.")
        right_pivot(.92)
        time.sleep(1)
        i = (i+1) % 4
        robot.change_direction(key_list[i])
        print("Current robot direction: " + robot.get_direction())

def rotate_left(start):
    key_list = list(compass.keys())
    i = compass[start]
    #prithvi's left turn
    print("Execute left turn.")
    left_pivot(1)
    stop()
    i = (i-1) % 4
    robot.change_direction(key_list[i])
    print("Current robot direction: " + robot.get_direction())

def optimal_turn(start, end):
    key_list = list(compass.keys())
    i = compass[start]
    if compass[end] == ((i+3) % 4):
        return True

def leave_room():
    cur_dir = robot.get_direction()
    key_list = list(compass.keys())
    i = compass[cur_dir]
    print("Execute right turn.")
    right_pivot(1.7)
    time.sleep(1)
    i = (i+1) % 4
    robot.change_direction(key_list[i])
    print("Current robot direction: " + robot.get_direction())
    print("Execute right turn.")
    #right_pivot(1.65)
    #time.sleep(1)
    i = (i + 1) % 4
    robot.change_direction(key_list[i])
    print("Current robot direction: " + robot.get_direction())
    forward(g.get_node(robot.get_position()).get_hallway_width())
    time.sleep(1)
    print("Leave the room.")
    robot.change_in_room(False)


def deliver_orders():
    print("open file.")
    order_file = open("SimpleOrder.txt", "r")
    orders = order_file.readlines()
    num_of_delivers = len(orders)
    for i in range(num_of_delivers):
        cur_order = orders[i].split(',')
        instruction(g.get_index(cur_order[0]))
        print("Deliver the order for room: " + str(orders[i]))
        print("Deliver Item: " + cur_order[1])
        #implement wait function until order has been confirmed
       
def getBFSSolution(start,goal,cur_path,visited):
    
    visited.append(start)
    cur_path.append(start)
       
    if start == goal:
       return True
       
    connections = g.get_node(start).get_connections()
    num_connections = g.get_node(start).num_edges()
    for index in range(num_connections):
        if connections[index].get_index() not in visited:
            if getBFSSolution(connections[index].get_index(), goal, visited, cur_path):
                return True

    cur_path.pop()
    return False

def time_travel(dis):
    return dis * ratio


mainloop()

