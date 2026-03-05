import RPi.GPIO as GPIO
import time
class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        new_numb = [int(element) for element in bin(number)[2: ].zfill(8)]
        GPIO.output(self.bits_gpio, new_numb)

    def sequential_counting_adc(self):
        for i in range(0, 255):
            self.number_to_dac(i)
            time.sleep(self.compare_time)
            comparator = GPIO.input(self.comp_gpio)
            if comparator == 1:
                return(max(0, i - 1))
        return 255

    def get_sc_voltage(self):
        value = self.sequential_counting_adc()
        return (value/255)*self.dynamic_range
