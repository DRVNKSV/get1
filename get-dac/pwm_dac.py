import RPi.GPIO as GPIO
class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)
        if self.verbose:
            print(f"PWM_DAC инициализирован на пине {gpio_pin}")
            print(f"Частота ШИМ: {pwm_frequency} Гц")
            print(f"Динамический диапазон: {dynamic_range} В")
    
    def deinit(self):
        self.pwm.stop()
        GPIO.output(self.gpio_pin, 0)
        GPIO.cleanup()

    def set_voltage(self, voltage):
        if voltage < 0:
            raise ValueError(f"Напряжение не может быть отрицательным: {voltage}")
        if voltage > self.dynamic_range:
            raise ValueError(f"Напряжение {voltage} В превышает максимальное {self.dynamic_range} В")
        duty_cycle = (voltage / self.dynamic_range) * 100.0
        self.pwm.ChangeDutyCycle(duty_cycle)
        
        if self.verbose:
            actual_voltage = (duty_cycle / 100.0) * self.dynamic_range
            print(f"Запрошено напряжение: {voltage:.3f} В")
            print(f"Установлен коэффициент заполнения: {duty_cycle:.2f}%")
            print(f"Фактическое напряжение: {actual_voltage:.3f} В")

if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.290, True)
        print("Программа управления ЦАП на основе ШИМ")
        print("Пин OUT: GPIO 12 (физический пин 32)")
        print("Для выхода нажмите Ctrl+C")
        print("-" * 50)
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах (0 - 3.290): "))
                dac.set_voltage(voltage)
                print("-" * 50)
            except ValueError:
                print("Ошибка: Вы ввели не число. Попробуйте ещё раз\n")
            except KeyboardInterrupt:
                print("\nПрограмма остановлена пользователем")
                break
            except Exception as e:
                print(f"Ошибка: {e}\n")
    finally:
        if 'dac' in locals():
            dac.deinit()
