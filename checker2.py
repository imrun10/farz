import time
import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
import math
from time import sleep


CW = 1
CCW = 0
Dir = 20
Stp = 21

paper = 1
metal = 2
plastic = 3
other = 4
servoPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(Dir, GPIO.OUT)
GPIO.setup(Stp, GPIO.OUT)
GPIO.output(Dir, CCW)




def rotate(pins): # pass in pin to rotate

    factory = PiGPIOFactory()
    ope = 90
    clo = 270

    
    servo = Servo(pins, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
#open 70 - 100   closed  250 - 290




    for i in range(0, 25):             # open rotation 0-100 how much it rotates
        servo.value = math.sin(math.radians(i))
        sleep(0.01) #dont touch this

    servo.value = math.sin(math.radians(0)) #stops rotation when open
    sleep(3) #stays open for 3 sec

    for i in range(190, 208): #close rotaion start from 190 for reverse rotation 190-273 how much it closes
        servo.value = math.sin(math.radians(i))
        sleep(0.01) #dont touch this


    servo.value = math.sin(math.radians(0)) #stops rotation when closed
    sleep(1) #avoid bug
   
    return 1 #avoid bug






try:
    
    while True:
            GPIO.output(Stp, GPIO.HIGH)
            time.sleep(0.0005)
            GPIO.output(Stp, GPIO.LOW)
            time.sleep(0.0005)
       
       




except KeyboardInterrupt:
    # Clean up GPIO channels on program exit
    GPIO.cleanup()
