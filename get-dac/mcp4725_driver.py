import smbus
class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose = True):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        self.dynamic_range = dynamic_range
    def deinit(self):
        self.bus.close()
    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return
        if not(0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")
            return
        first_byte = self.wm | self.pds | (number >> 8)
        second_byte = number & 0xFF
        try:
            self.bus.write_i2c_block_data(self.address, 0x40, [first_byte, second_byte])
        except Exception as e:
            print(f"Ошибка I2C: {e}")
            return
        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address << 1):02X}, 0x{first_byte:02x}, 0x{second_byte:02x}]\n")
    def voltage_to_number(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f'Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)')
            print('Устанавливаем 0.0 В')
            return 0
        return int(voltage / self.dynamic_range * 4095)
    def set_voltage(self, voltage):
        number = self.voltage_to_number(voltage)
        self.set_number(number)
    

if __name__ == "__main__":
    try:
        mcp = MCP4725(dynamic_range=5.0)
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                mcp.set_voltage(voltage)
            except ValueError:
                print('Вы ввели не число. Попробуйте еще раз\n')
    finally:
        mcp.deinit()
