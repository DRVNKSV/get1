import mcp3021_driver
import adc_plot
import time

mcp = mcp3021_driver.MCP3021(5.2, 1)
voltage_values = []
time_values = []
duration = 3.0
try:
    start_time = time.time()
    while (time.time() - start_time) < duration:
        current_voltage = mcp.get_voltage()
        current_time = time.time() - start_time
        voltage_values.append(current_voltage)
        time_values.append(current_time)
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, 3.3)
    adc_plot.plot_sampling_period_hist(time_values)
finally:
    mcp.deinit()