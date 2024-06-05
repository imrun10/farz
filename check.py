import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
p = GPIO.PWM(17, 100)
p.start(5)


p.ChangeDutyCycle(7)  # open
time.sleep(1)
p.ChangeDutyCycle(2.5)  # stop
time.sleep(1)


p.stop()  # Stop PWM
GPIO.cleanup()