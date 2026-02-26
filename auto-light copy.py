import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
trans = 6
GPIO.setup(trans, GPIO.IN)
while True:
    GPIO.output(led, not GPIO.input(trans))
GPIO.cleanup()