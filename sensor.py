import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM (Broadcom SOC channel numbering)
GPIO.setmode(GPIO.BCM)

# Set the pin number connected to the touch sensor
TOUCH_PIN = 12

# Set the GPIO pin as an input
GPIO.setup(TOUCH_PIN, GPIO.IN)

# Variable to track the touch sensor state
prev_touch_state = GPIO.LOW  # Assuming the sensor is not touched initially

# Variable to track the start time of touch
touch_start_time = None

try:
    while True:
        touch_state = GPIO.input(TOUCH_PIN)

        if touch_state != prev_touch_state:
            if touch_state == GPIO.HIGH:
                # Sensor touched event
                print("Touch sensor is touched!")
                # Record the start time when the touch is detected
                touch_start_time = time.time()
            else:
                # Sensor released event
                print("Touch sensor is released!")
                # Reset the touch start time when sensor is released
                touch_start_time = None

        if touch_start_time is not None:
            # Check if the touch has been held for 3 seconds
            if time.time() - touch_start_time >= 3:
                print("Activated")
                # Reset touch start time after activation
                touch_start_time = None

        prev_touch_state = touch_state
        time.sleep(0.1)  # A small delay to debounce the input
        
except KeyboardInterrupt:
    # Clean up the GPIO settings on program exit
    GPIO.cleanup()

