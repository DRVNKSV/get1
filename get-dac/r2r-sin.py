import r2r_dac as r2r
import signal_generator as sg
import time
amplitude = 3
signal_frequency = 30
sampling_frequency = 1000

if __name__ == "__main__":
    try:
        dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.3, True)
        start = time.time()
        while True:
            finish = time.time() - start
            dac.set_voltage(amplitude*sg.get_sin_wave_amplitude(signal_frequency, finish))
            sg.wait_for_sampling_period(sampling_frequency)
    finally:
        dac.deinit()
