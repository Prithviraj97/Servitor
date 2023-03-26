from tkinter import *
from Graph import *
from Robot_Info import *
from collections import deque
import RPi.GPIO as gpio
import time

# Author: Prithvi Raj Singh, Blake Drost
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

compass = dict({'North': 0, 'East': 1, 'South': 2, 'West': 3})
g = Graph()
cell_size = 50
start_x = 50
start_y = 150
array_edges = []
mouse_instructions = []
robot = Robot("0", 'South')

hallway_width = 26.4 / 12
array_illustration = []
# ratio is formatted as seconds / feet
# this is used to tell how long the robot should run to reach a desired distance
ratio = 5/8.4
# rows = 5
# cols = 5
graph_file = "5X5_graph.txt"
array_file = "5X5_array.txt"
rows = 5
cols = 5
#graph_file = "7X7_graph.txt"
#array_file = "7X7_array.txt"

# Start GUI Section

window = Tk()
window.title("Waypoint Selector")
window.geometry("1050x650")


cur_position = Label(
    text="Current Location: None",
    font="Helvetica 16 bold",
    width=30,
    height=3,
    bg="#a9a9a9",
    fg="black")
cur_position.place(x=350, y=25)
prompt_label = Label(
    text="Place the robot facing south on the\ndesired starting location.\nSelect a destination for the robot\nby selecting two nodes below.",
    font="Helvetica 12 bold",
    width=30,
    height=5,
    bg="#a9a9a9",
    fg="black")
prompt_label.place(x=25, y=25)

# End GUI Section

def changetext(b):
    cur_position.config(text="Current Location: " + b)
    cur_position.config(font="Helvetica 16 bold")


def changetext2():
    stuff = reformat(g.get_node(robot.get_position()).get_name())
    cur_position.config(text="Current Location: " + stuff)
    cur_position.config(font="Helvetica 16 bold")


def instruction(start_name, location_name):
    start = g.get_index(start_name)
    location = g.get_index(location_name)
    print("Start: " + str(start) + " Goal: " + str(location))

    if start == location:
        return print("Already at desired location.")
    pathway = []
    pathway = get_breadth_first_search_solution(start, location)
    print_pathway(pathway)
    print(pathway)

    i = 0
    while robot.get_position() is not location:
        i = i + 1
        desired_position = pathway[i]
        edges = g.get_node(robot.get_position()).get_connections()
        index = 0
        for index1 in range(len(edges)):
            if edges[index1].get_edge_index() == desired_position:
                index = index1
        direction = edges[index].get_direction()
        face_robot(direction)
        dis = edges[index].get_distance()
        if dis == 8.0:
            forward(dis/2*ratio)
            time.sleep(.5)
            forward(dis/2*ratio)
            time.sleep(.5)
        else:
            ran = dis*ratio
            forward(ran)
            time.sleep(.5)
        print("Traverse: " + str(dis) + " feet")
        # prithvi's code
        robot.change_position(desired_position)
    changetext2()


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
        rotate_right(cur_dir, goal_dir)
        counter = counter + 1
        if counter == 4:
            print("Error when rotating")
            return


#   rotate_right() takes in the direction the robot is facing and the desired direction
def rotate_right(start, end):
    # represents an index value for a direction
    # character is key and integer is value
    key_list = list(compass.keys())
    i = compass[start]
    while not (robot.get_direction() == end):
        print("Execute right turn.")
        # prithvi's right turn
        right_pivot(0.98)
        time.sleep(0.5)
        i = (i + 1) % 4
        robot.change_direction(key_list[i])
        print("Current robot direction: " + robot.get_direction())


def get_breadth_first_search_solution(start, goal):
    explored = []
    queue = [[start]]

    if start == goal:
        return True

    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in explored:
            connect = g.get_node(node).get_connections()
            index_connections = []
            for index in range(len(connect)):
                index_connections.append(connect[index].get_edge_index())
            for connection in index_connections:
                new_path = list(path)
                new_path.append(connection)
                queue.append(new_path)
                if connection == goal:
                    return new_path
            explored.append(node)
    return False


def read_in_graph(f):
    file = open(f, "r")
    node_edges = file.readlines()
    num_edges = len(node_edges)
    for j in range(num_edges):
        array_edges.append(node_edges[j])
        cur_edge = node_edges[j].split(',')
        node1 = cur_edge[0]
        node1coord = node1.split(':')
        node1x = node1coord[0]
        node1y = node1coord[1]
        node2 = cur_edge[1]
        node2coord = node2.split(':')
        node2x = node2coord[0]
        node2y = node2coord[1]
        width = cur_edge[2].strip("\n")
        g.add_node(node1, ' ', hallway_width)
        g.add_node(node2, ' ', hallway_width)
        # find if x is the same value or y is the same value
        if node1x == node2x:
            # if node1y > nodey2
            # node1y is South node2y is North
            if node1y > node2y:
                g.add_connection(node1, node2, 'South', 'North', float(width))
            else:
                g.add_connection(node1, node2, 'North', 'South', float(width))
        if node1y == node2y:
            # if node1x > node2x
            # node1x is East node2x is West
            if node1x > node2x:
                g.add_connection(node1, node2, 'East', 'West', float(width))
            else:
                g.add_connection(node1, node2, 'West', 'East', float(width))

    file.close()


def read_in_array(f):
    file = open(f, "r")
    cur_rows = file.readlines()
    num_rows = len(cur_rows)
    for index2 in range(num_rows):
        col_list = []
        cur_cols = cur_rows[index2].split(' ')
        num_cols = len(cur_cols)
        if len(cur_cols) > cols:
            del cur_cols[num_cols-1]
        for index3 in range(len(cur_cols)):
            col_list.append(cur_cols[index3])
        array_illustration.append(col_list)
    file.close()


read_in_graph(graph_file)
read_in_array(array_file)


def time_travel(dis):
    return dis * ratio


c = Canvas(window, width=cols*cell_size, height=rows*cell_size, background='black')
c.place(x=start_x, y=start_y)
str_x = 0
str_y = 0

# Creating blank grid of hallways and walls

for i in range(rows):
    for j in range(cols):
        if array_illustration[i][j] == 'h':
            c.create_rectangle(str_x+j*cell_size, str_y+i*cell_size,
            str_x+(j+1)*cell_size, str_y+(i+1)*cell_size, fill='green')
        if array_illustration[i][j] == 'w':
            c.create_rectangle(str_x+j*cell_size, str_y+i*cell_size,
            str_x+(j+1)*cell_size, str_y+(i+1)*cell_size, fill='brown')

str_x = 20
str_y = 20
radius = 10

# Creating nodes on the grid

for i in range(g.num_nodes):
    cur_node = g.get_node(i)
    cur_name = cur_node.get_name()
    x_y_position = cur_name.split(':')
    c.create_oval(str_x+int(x_y_position[0])*cell_size, str_y+int(x_y_position[1])*cell_size,
    str_x+(int(x_y_position[0]))*cell_size+radius, str_y+(int(x_y_position[1]))*cell_size+radius, fill='blue')
    # print(x_y_position[0] + "," + x_y_position[1])

# Creating lines between nodes

str_x = 25
str_y = 25
line_width = 5

for i in range(len(array_edges)):
    cur_edge = array_edges[i].split(',')
    node1 = cur_edge[0].split(':')
    node1_x = int(node1[0])
    node1_y = int(node1[1])
    node2 = cur_edge[1].split(':')
    node2_x = int(node2[0])
    node2_y = int(node2[1])
    distance = cur_edge[2]
    c.create_line(str_x+(node1_x*cell_size), str_y+(node1_y*cell_size), str_x+node2_x*cell_size, str_y+node2_y*cell_size, fill='blue')


def left_click(event):
    x = int(event.x / cell_size)
    y = int(event.y / cell_size)
    if not g.is_node(str(x) + ":" + str(y)):
        print("Not a valid node.")
        return
    cur_click = str(x) + ":" + str(y)
    mouse_instructions.append(cur_click)
    if len(mouse_instructions) == 1:
        cur_node_index = g.get_index(mouse_instructions[0])
        changetext(reformat(g.get_node(cur_node_index).get_name()))
    if len(mouse_instructions) == 2:
        start_position = mouse_instructions[0]
        print("start position: " + start_position)
        robot.change_position(g.get_index(start_position))
        goal_position = mouse_instructions[1]
        print("goal position: " + goal_position)
        instruction(start_position, goal_position)
        mouse_instructions.clear()


def reformat(stuff):
    x_y_coord = stuff.split(':')
    new_stuff = "(" + x_y_coord[0] + "," + x_y_coord[1] + ")"
    return new_stuff


def print_pathway(p):
    length_p = len(p)
    string_acc = ""
    for index in range(length_p):
        graph_index = p[index]
        unformatted_coord = g.get_node(graph_index).get_name()
        new_format = reformat(unformatted_coord)
        if index == length_p-1:
            string_acc += new_format
            return print(string_acc)
        string_acc += new_format + " -> "


c.bind("<Button-1>", left_click)

mainloop()
