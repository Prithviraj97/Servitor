import RPi.GPIO as gpio
import time
import sys
import tkinter as tk
from Sonic import distance
import random
# from Camera import *
 
#Initiate the GPIO pins for running wheels
def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT) 
    gpio.setup(24, gpio.OUT)
    
def forward(tf):
    init() 
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(tf)
    gpio.cleanup()
    
def reverse(tf):
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(tf)
    gpio.cleanup()
    
def right_turn(tf):
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)
    time.sleep(tf)
    gpio.cleanup()
    
def left_turn(tf):
    init()
    gpio.output(17, True)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(tf)
    gpio.cleanup()
    
def left_pivot(tf):
    init()
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(tf)
    gpio.cleanup()
    
def right_pivot(tf):
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(tf)
    gpio.cleanup()
    
def stop(tf):
    init()
    gpio.output(17, True)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, True)
    time.sleep(tf)
    gpio.cleanup()
    
# right_pivot(3)    
# left_pivot(2)
#right_turn(2)
'''
def key_input(event):
    init()
    print ('Key:', event.char)
    key_press = event.char
    sleep_time = 0.30
    
    if key_press.lower()=='s':
        forward(sleep_time)
    elif key_press.lower()=='w':
        reverse(sleep_time)
    elif key_press.lower()=='a':
        left_turn(sleep_time)
    elif key_press.lower()=='d':
        right_turn(sleep_time)
    elif key_press.lower()=='q':
        left_pivot(sleep_time)
    elif key_press.lower()=='e':
        right_pivot(sleep_time)
    else:
        stop(sleep_time)
        
    curDis = distance('cm')
    print('curdis is', curDis)
    
    if curDis < 20:
        init()
        reverse(2)
        
          
command = tk.Tk()
command.bind('<KeyPress>', key_input)
command.mainloop()
'''

#Ckeck front before moving. Front is the one where ultrasonic sensors is facing
def front():
    init()
    dist = distance()
    if dist < 30:
        print('Too Close,',dist)
        init()
        reverse(1.5)
        dist= distance()
        if dist < 30:
            print('Too CLose,',dist)
            init()
            left_pivot(2)
            init()
            reverse(1.5)
            dist = distance()
            if dist < 30:
                print('Too Close,',dist)
                init()
                right_pivot(2)
                init()
                reverse(1.5)
                
            if dist < 30:
                print('Too Close', dist)
                sys.exit()
                
    else:
        forward(5) #will go forward unless obsatcle is detected.
        init()
        if dist<30:
            stop(1.5)
        if dist>30:
            forward(3)
            
#Autnomy will control the robot self-movement.
def Autonomy():
    tf=0.030 #30 millisecond time frame.
    x= random.randrange(0,4)
    
    if x==0:
        for y in range(30): #Every 30 Milli second it will check the distance
            front()
            init()
            forward(tf)
    elif x == 1:  
        for y in range(30):
            front()
            init()
            left_pivot(tf)
    elif x == 2:
        for y in range(30):
            front()
            init()
            right_turn(tf)
    elif x == 3:
        for y in range(30):
            front()
            init()
            left_turn(tf)
    
            
for z in range(10):
    Autonomy()


    

     
