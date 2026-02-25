import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        self.address = address
        # wm = 0x00 - запись без записи в EEPROM
        # pds = 0x00 - нормальный режим (без сброса)
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        self.dynamic_range = dynamic_range
        
        if self.verbose:
            print(f"MCP4725 инициализирован")
            print(f"  I2C адрес: 0x{address:02X}")
            print(f"  Динамический диапазон: {dynamic_range} В")
            print(f"  Разрешение: 12 бит (0-4095)")
    
    def deinit(self):
        self.bus.close()
        if self.verbose:
            print("I2C шина закрыта")
    
    def set_number(self, number):
        if not isinstance(number, int):
            raise TypeError(f"На вход ЦАП можно подавать только целые числа, получен {type(number)}")
        if not (0 <= number <= 4095):
            raise ValueError(f"Число {number} выходит за разрядность MCP4725 (12 бит, 0-4095)")
        first_byte = self.wm | self.pds | (number >> 8)
        second_byte = number & 0xFF
        self.bus.write_byte_data(self.address, first_byte, second_byte)
        
        if self.verbose:
            # Формирование адреса для вывода (с битом записи)
            write_address = (self.address << 1) & 0xFE
            print(f"Число: {number} (0x{number:03X})")
            print(f"  Двоичное представление: 0b{number:012b}")
            print(f"  Отправленные по I2C данные: [0x{write_address:02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]")
            print(f"    Первый байт (настройки + биты 11-8): 0x{first_byte:02X}")
            print(f"    Второй байт (биты 7-0): 0x{second_byte:02X}")
    
    def set_voltage(self, voltage):
        if not isinstance(voltage, (int, float)):
            raise TypeError(f"Напряжение должно быть числом, получен {type(voltage)}")
        if voltage < 0:
            raise ValueError(f"Напряжение не может быть отрицательным: {voltage}")
        if voltage > self.dynamic_range:
            raise ValueError(f"Напряжение {voltage} В превышает максимальное {self.dynamic_range} В")
        
        max_number = 4095  # 2^12 - 1
        number = int(round((voltage / self.dynamic_range) * max_number))
        self.set_number(number)
        
        if self.verbose:
            actual_voltage = (number / max_number) * self.dynamic_range
            error = actual_voltage - voltage
            error_percent = (abs(error) / self.dynamic_range) * 100
            
            print(f"Запрошено напряжение: {voltage:.3f} В")
            print(f"Установлено число: {number}")
            print(f"Фактическое напряжение: {actual_voltage:.3f} В")
            print(f"Абсолютная ошибка: {error:.3f} В")
            print(f"Относительная ошибка: {error_percent:.2f}%")
            print(f"Разрешение ЦАП: {self.dynamic_range / 4096:.3f} В/шаг")

if __name__ == "__main__":
    try:
        dac = MCP4725(5.0, 0x61, True)
        while True:
            try:
                choice = input("Ваш выбор (1/2/3): ").strip()
                if choice == '1':
                    voltage = float(input("Введите напряжение в Вольтах (0 - 5.0): "))
                    dac.set_voltage(voltage)
                    
                elif choice == '2':
                    number = int(input("Введите число (0 - 4095): "))
                    dac.set_number(number)
                    
                elif choice == '3':
                    print("Завершение программы...")
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
                    
            except ValueError as e:
                print(f"Ошибка ввода: {e}")
            except KeyboardInterrupt:
                print("\nПрограмма остановлена пользователем")
                break
            except Exception as e:
                print(f"Ошибка: {e}")

    finally:
        if 'dac' in locals():
            dac.deinit()
        print("Программа завершена")
