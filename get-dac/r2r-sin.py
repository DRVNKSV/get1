import r2r_dac as r2r
import signal_generator as sg
import time
import signal
import sys
amplitude = 3.2
signal_frequency = 10  # Гц (10 периодов в секунду)
sampling_frequency = 1000  # Гц (1000 точек в секунду)
dac_range = 3.3  # Вольт
start_time = None
sample_count = 0
def signal_handler(sig, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def generate_sine_wave():
    global start_time, sample_count
    try:
        dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], dac_range, verbose=False)
        start_time = time.time()
        sample_count = 0
        while True:
            current_time = time.time() - start_time
            normalized_amplitude = sg.get_sin_wave_amplitude(signal_frequency, current_time)
            output_voltage = normalized_amplitude * amplitude
            dac.set_voltage(output_voltage)
            if sample_count % 100 == 0:
                print(f"t={current_time:.3f}с, напряжение={output_voltage:.3f}В, "
                      f"норм.амплитуда={normalized_amplitude:.3f}")
            sample_count += 1
            sg.wait_for_sampling_period(sampling_frequency)
    finally:
        if 'dac' in locals():
            dac.deinit()
            print(f"\nГенерация завершена.")
            print(f"Сгенерировано точек: {sample_count}")
            print(f"Длительность: {time.time() - start_time:.2f} с")
if __name__ == "__main__":
    try:
        generate_sine_wave()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nОшибка: {e}")
    finally:
        print("Программа завершена.")
