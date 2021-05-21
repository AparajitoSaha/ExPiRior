"""

Gets the object distance measurement from the ultrasonic sensor

From the PiHut tutorial: https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

"""

def sensor():

  import RPi.GPIO as GPIO

  import time

  GPIO.setmode(GPIO.BCM)
  
  TRIG = 23

  ECHO = 24

  print "Distance Measurement In Progress"

  GPIO.setup(TRIG,GPIO.OUT)

  GPIO.setup(ECHO,GPIO.IN)

  GPIO.output(TRIG, False)

  #Waiting For Sensor To Settle

  time.sleep(2)

  GPIO.output(TRIG, True)

  time.sleep(0.00001)

  GPIO.output(TRIG, False)

  while GPIO.input(ECHO)==0:

    pulse_start = time.time()

  while GPIO.input(ECHO)==1:

    pulse_end = time.time()      

  pulse_duration = pulse_end - pulse_start

  distance = pulse_duration x 17150

  distance = round(distance, 2)

  GPIO.cleanup()
  
  return (distance)





