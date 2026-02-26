import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        self.dynamic_range = dynamic_range
        
    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        first_byte = self.wm | self.pds | (number >> 8)
        second_byte = number & 0xFF
        self.bus.write_byte_data(self.address, first_byte, second_byte)
    
        if self.verbose:
            write_address = (self.address << 1) & 0xFE

            
    def set_voltage(self, voltage):
        max_number = 4095  # 2^12 - 1
        number = int(round((voltage / self.dynamic_range) * max_number))
        self.set_number(number)
        
        if self.verbose:
            actual_voltage = (number / max_number) * self.dynamic_range
            error = actual_voltage - voltage
            error_percent = (abs(error) / self.dynamic_range) * 100
            

if __name__ == "__main__":
    try:
        dac = MCP4725(5.0, 0x61, True)
        while True:
            try:

                    voltage = float(input("Введите напряжение в Вольтах (0 - 5.0): "))
                    dac.set_voltage(voltage)
                    
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
