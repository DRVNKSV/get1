import RPi.GPIO as gp
class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        gp.setmode(gp.BCM)
        gp.setup(self.gpio_pin, gp.OUT, initial = 0)
        self.pwm = gp.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)
    def deinit(self):
        self.pwm.stop()
        gp.cleanup()
    def set_duty(self, duty):
        self.pwm.ChangeDutyCycle(duty)
        fill_factor = 1 / duty * 100
        print(f"Коэффициент заполнения: {fill_factor:.2f}")
    def voltage_to_duty(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f'Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)')
            print('Устанавливаем 0.0 В')
            return 0
        return int(voltage / self.dynamic_range * 100)
    def set_voltage(self, voltage):
        duty = self.voltage_to_duty(voltage)
        if duty:
            self.set_duty(duty)

if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.3, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print('Вы ввели не число. Попробуйте еще раз\n')
    finally:
        dac.deinit()
