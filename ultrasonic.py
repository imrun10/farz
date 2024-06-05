import RPi.GPIO as GPIO
import time

def ultrasonic():
    # Set GPIO pin numbers
    GPIO_TRIG = 19
    GPIO_ECHO = 4

    def setup():
        # Use BCM GPIO references
        GPIO.setmode(GPIO.BCM)

        # Set pins as output and input
        GPIO.setup(GPIO_TRIG, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)

        # Set trigger pin to low
        GPIO.output(GPIO_TRIG, False)
        time.sleep(0.5)

    def object_detected(distance):
        if distance < 15:
            return True
        else:
            return False

    def get_distance():
        # Send 10us pulse to trigger
        GPIO.output(GPIO_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIG, False)

        # Measure time between start and end of pulse
        start_time = time.time()
        end_time = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            start_time = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            end_time = time.time()

        # Calculate distance based on time
        duration = end_time - start_time
        distance = duration * 17150  # Speed of sound is 34300 cm/s, halved for return trip
        distance = round(distance, 2)

        return distance

    def cleanup():
        GPIO.cleanup()

    setup()
    distance = get_distance()
    if object_detected(distance):
        print(distance)
    return False
    time.sleep(1)

while True:
   ultrasonic()
