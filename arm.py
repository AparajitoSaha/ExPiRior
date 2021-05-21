import RPi.GPIO as GPIO
import time
from gpiozero import Servo

def move_arm():
    claw = Servo(19,0)
    updown = 12
    elbow = Servo(13)

    rotate = 21
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(rotate, GPIO.OUT)
    GPIO.setup(updown, GPIO.OUT)
    r = GPIO.PWM(rotate, 50)
    p = GPIO.PWM(updown, 50)

    #p.start(9.5)
    r.start(2.5)

    claw.mid()
    r.ChangeDutyCycle(2.5)
    print("Moved towards tubes")
    time.sleep(2)
    print("Grabbing tube")
    time.sleep(2)
    claw.max()
    time.sleep(5)

    print("Moving to user")
    r.ChangeDutyCycle(12.5)
    time.sleep(2)
    print("Closing claw")
    time.sleep(2)

    #GPIO.cleanup()
    #claw.stop()

def calibrate_updown():
    p.ChangeDutyCycle(7.5)

def calibrate_rotate():
    r.ChangeDutyCycle(2.5)

def calibrate():
    r.ChangeDutyCycle(7.5)
    claw.max()
    elbow.mid()
    p.ChangeDutyCycle(22.5)
    print("Calibrating - everything in mid position, claw closed")
    time.sleep(2)

def grab_tube():
    claw.mid()
    r.ChangeDutyCycle(2.5)
    print("Moved towards tubes")
    time.sleep(2)
    print("Grabbing tube")
    time.sleep(2)
    claw.max()
    time.sleep(2)

def grab_swab():
    r.ChangeDutyCycle(3.5)
    claw.max()
    elbow.mid()
    print("Moved towards tubes")
    time.sleep(2)
    print("Grabbing tube")
    p.ChangeDutyCycle(22.5)
    claw.value = 0.65
    claw.mid()
    time.sleep(3)
    claw.max()
    time.sleep(1)
    print("Moving up")
    #p.ChangeDutyCycle(27.5)
    time.sleep(2)

def release():
    print("Moving to user")
    r.ChangeDutyCycle(12.5)
    time.sleep(2)
    print("Closing claw")
    time.sleep(2)

#calibrate()
#time.sleep(5)
#grab_tube()
#claw.max()
#claw.mid()
#time.sleep(3)
#claw.max()
#release()
#calibrate_updown()
#time.sleep(2)
#calibrate_rotate()
#time.sleep(2)
#p.stop()
#r.stop()
#GPIO.cleanup()
#claw.stop()
