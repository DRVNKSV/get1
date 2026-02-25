import RPi.GPIO as GPIO
class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)
    
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    
    def set_number(self, number):
        if number < 0 or number > 255:
            raise ValueError("Число должно быть в диапазоне от 0 до 255")
        for i, pin in enumerate(self.gpio_bits):
            bit_value = (number >> i) & 1
            GPIO.output(pin, bit_value)
        if self.verbose:
            print(f"Установлено число: {number} (0b{number:08b})")
            
    def set_voltage(self, voltage):
        if voltage < 0 or voltage > self.dynamic_range:
            raise ValueError(f"Напряжение должно быть в диапазоне от 0 до {self.dynamic_range} В")
        max_number = 255
        number = int(round((voltage / self.dynamic_range) * max_number))
        self.set_number(number)
        if self.verbose:
            actual_voltage = (number / max_number) * self.dynamic_range
            print(f"Запрошено напряжение: {voltage:.3f} В")
            print(f"Установлено число: {number}, фактическое напряжение: {actual_voltage:.3f} В")

if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
                print("-" * 40)

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

    



