import mcp4725_driver
import signal_tr as tr
import time


amplitude = 3
signal_frequency = 20
sampling_frequency = 1000

if __name__ == "__main__":
    try:
        dac = mcp4725_driver.MCP4725(5)
        start = time.time()
        while True:
            finish = time.time() - start
            dac.set_voltage(amplitude*tr.get_tr_value(signal_frequency, finish))
            tr.wait_for_sampling_period(sampling_frequency)
    finally:
        dac.deinit()
