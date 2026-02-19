import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
dac_bits = [16, 20, 21, 25, 26, 17, 27, 22]
GPIO.setup(dac_bits, GPIO.OUT)
dynamic_range = 3.31.2\
def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Out of {dynamic_range:.2f} B")
        print("select 0.0 B")
        return 0
    return int(voltage / dynamic_range *255)

def number_to_dac(number):
    decimal_mass = [int(element) for element in bin(number)[2:].zfill(8)]
    GPIO.output(dac_bits, decimal_mass)
    print(decimal_mass)

try:
    while True:
        try:
            voltage = float(input("Paste voltage in volts: "))
            number = voltage_to_number(voltage)
            print(number)
            number_to_dac(number)

        except ValueError:
            print("you printed not a number. Do it again\n")
finally:
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()