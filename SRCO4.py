import RPi.GPIO as gpio
import time

TRIG = 12
ECHO = 13

def distance(measure='cm'):
    gpio.setmode(gpio.BCM)
    gpio.setup(12, gpio.OUT)
    gpio.setup(13, gpio.IN)
    
    gpio.output(12, False)
    while gpio.input(13) ==0:
        nosignal = time.time()
        
    while gpio.input(13) ==1:
        signal = time.time()
        
    tl = signal-nosignal
    
    if measure == 'cm':
        distance = tl/0.000058
    elif measure == 'in':
        distance = tl/0.000148
    else:
        print('blhan')
        distance = None
        
    gpio.cleanup()
    return distance
print(distance ('cm'))