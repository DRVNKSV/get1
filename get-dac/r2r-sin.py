import r2r_dac as r2r
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 10 
sampling_frequency = 1000 
dac_range = 3.3 

dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.3)

try:
    start_time = time.time()
    while True:
        t = time.time() - start_time
        voltage = sg.get_sin_wave_amplitude(signal_frequency, t) * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()