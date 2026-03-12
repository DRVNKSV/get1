import r2r_adc
import adc_plot
import time
voltage_values = []
time_values = []
duration = 3.0
if __name__ == "__main__":
    try:  
        start_time = time.time()
        while (time.time() - start_time) < duration:
            current_voltage = r2r_adc.R2R_ADC(3.3).get_sar_voltage()
            current_time = time.time() - start_time
            voltage_values.append(current_voltage)
            time_values.append(current_time)
        adc_plot.plot_voltage_vs_time(time_values, voltage_values, 3.3)
        adc_plot.plot_sampling_period_hist(time_values)
    finally:
        r2r_adc.R2R_ADC(3.3).deinit()