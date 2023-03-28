#import bluetooth
#import time
import RPi.GPIO as GPIO
from bluedot import BlueDot
from gpiozero import Robot
from signal import pause

m11=17
m12=22
m21=23
m22=24
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.output(m11 , 0)
GPIO.output(m12 , 0)
GPIO.output(m21, 0)
GPIO.output(m22, 0)


def up():
    print("up")

def down():
    print("down")

def left():
    print("left")

def right():
    print("right")
    
def stop():
    print("stop")

bd = BlueDot(cols=4, rows=3)
bd.color = "green"
bd.square = True

bd[0,0].visible = False
bd[2,0].visible = False
bd[0,2].visible = False
bd[2,2].visible = False
bd[1,1].visible = False 

bd[1,0].when_pressed = up
bd[1,2].when_pressed = down
bd[0,1].when_pressed = left
bd[2,1].when_pressed = right
bd[3,1].when_pressed = stop

pause()




def left_side_forward():
    GPIO.output(m21 , 1)
    GPIO.output(m22 , 0)
    time.sleep(.5)
    GPIO.output(m11 , 1)
    GPIO.output(m12 , 0)

def right_side_forward():
   GPIO.output(m21 , 1)
   GPIO.output(m22 , 0)
   time.sleep(.5)
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 1)

def forward():
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 1)
   GPIO.output(m22 , 0)

def left_side_reverse():
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 1)
   time.sleep(.5)
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)

def right_side_reverse():

   GPIO.output(m21 , 0)
   GPIO.output(m22 , 1)
   time.sleep(.5)
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 1)

def reverse():
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 1)

def stop():
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 0)
 
data=""
while 1:
         data= client_socket.recv(1024)
         print "Received: %s" % data
         if (data == "F"):    
            forward()
         elif (data == "L"):    
            left_side_forward()
         elif (data == "R"):    
            right_side_forward()
         elif (data == "B"):    
            reverse()
         elif (data == "A"):    
            left_side_reverse()
         elif (data == "P"):    
            right_side_reverse()
         elif data == "S":
            stop()
         elif (data == "Q"):
            print ("Quit")
            break
        
stop()
