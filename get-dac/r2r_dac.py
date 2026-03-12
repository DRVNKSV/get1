import RPi.GPIO as gp
class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        gp.setmode(gp.BCM)
        gp.setup(self.gpio_bits, gp.OUT, initial = 0)
    def deinit(self):
        gp.output(self.gpio_bits, 0)
        gp.cleanup()
    def set_number(self, number):
        bin_n = [int(element) for element in bin(number)[2:].zfill(8)]
        gp.output(self.gpio_bits, bin_n)
        print(f"Number in input: {number}, {bin_n}")
    def voltage_to_number(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f'The voltage is out of range(0.00 - {self.dynamic_range:.2f} В)')
            print('install 0.0 В')
            return 0
        return int(voltage / self.dynamic_range * 255 + 1)
    def set_voltage(self, voltage):
        number = self.voltage_to_number(voltage)
        self.set_number(number)


if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.3, True)

        while True:
            try:
                voltage = float(input("Paste voltage in volts: "))
                dac.set_voltage(voltage)
            except ValueError:
                print('You paste noy a number. paste number\n')
    finally:
        dac.deinit()
    



