import RPi.GPIO as GPIO
import time

PIR_PIN_ONE = 23
PIR_PIN_TWO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_ONE_PIN,  GPIO.IN)
GPIO.setup(PIR2_TWO_PIN, GPIO.IN)

def camera(channel):
    # Take your photo here
    print('Movement!')

try:
    GPIO.add_event_detect(PIR_ONE_PIN, GPIO.RISING, callback=camera)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print('KeyboardInterrupt detected.')

GPIO.cleanup()
