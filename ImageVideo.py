from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (800, 640)
camera.vflip = True

camera.start_preview()
#time.sleep(3)  #UnComment Two follwoing lines and comment the recording parts to capture pic. 
#camera.capture("/home/pi/Pictures/imgCapture.jpg")
camera.start_recording("/home/pi/Videos/piVideo.h264")
time.sleep(10)
camera.stop_recording()
camera.stop_preview()