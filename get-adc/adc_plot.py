import matplotlib.pyplot as plt
def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize = (10,6))
    plt.plot(time, voltage)
    plt.title("Voltage(time)")
    plt.xlabel("time, s")
    plt.ylabel("voltage, V")
    plt.xlim(0, max(time))
    plt.ylim(0, max_voltage)
    plt.grid(True)
    plt.show()
def plot_sampling_period_hist(time):
    sampling_periods = []
    for i in range (1, len(time)):
        period = time[i] - time[i - 1]
        sampling_periods.append(period)
    plt.figure(figsize = (10,6))
    plt.hist(samling_periods)
    plt.title("распределение периодов")
    plt.xlim(0, 0.06)
    plt.show()