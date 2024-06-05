import time
import RPi.GPIO as GPIO

CW =1
CCW =0
Dir = 20
Stp = 21
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(Dir, GPIO.OUT)
GPIO.setup(Stp, GPIO.OUT)

GPIO.output(Dir, CW)


while True:
    GPIO.output(Stp, GPIO.HIGH)
    time.sleep(.001)
    GPIO.output(Stp, GPIO.LOW)
    time.sleep(.001)


