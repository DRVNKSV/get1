import mcp4725_driver
import signal_generator as sg
import time
amplitude = 3
signal_frequency = 10
sampling_frequency = 1000

if __name__ == "__main__":
    try:
        mcp = mcp4725_driver.MCP4725(5)
        start = time.time()
        while True:
            finish = time.time() - start
            mcp.set_voltage(amplitude*sg.get_sin_wave_amplitude(signal_frequency, finish))
            sg.wait_for_sampling_period(sampling_frequency)
    finally:
        mcp.deinit()
