import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
leds = [16, 12, 25, 17, 27, 23, 22, 24]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)
up = 9
down = 10
GPIO.setup(up, GPIO.IN)
GPIO.setup(down, GPIO.IN)
num = 0
def dec2bin(val):
    return [int(element) for element in bin(val)[2:].zfill(8)]

sleep_time = 0.2
while True:
    if not GPIO.input(up) and not GPIO.input(down):
        GPIO.output(leds, 11111111)
    elif GPIO.input(up) and num < 255:
        num = num + 1
        print(num, dec2bin(num))
        time.sleep(sleep_time)
        GPIO.output(leds, dec2bin(num))
    elif GPIO.input(down) and num >= 0:
        num -= 1
        print(num, dec2bin(num))
        time.sleep(sleep_time)
        GPIO.output(leds, dec2bin(num))
GPIO.cleanup()