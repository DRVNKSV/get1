import numpy as np
import time
def get_sin_wave_amplitude(freq, t):
    raw_sin = np.sin(2 * np.pi * freq * t)
    normalized = (raw_sin + 1) / 2
    return normalized
def wait_for_sampling_period(sampling_frequency):
    sampling_period = 1.0 / sampling_frequency
    time.sleep(sampling_period)

def get_square_wave_amplitude(freq, t, duty_cycle=0.5):
    """
    Генерация меандра (прямоугольного сигнала)
    
    Параметры:
    freq (float): Частота сигнала
    t (float): Время
    duty_cycle (float): Коэффициент заполнения (0-1)
    """
    period = 1.0 / freq
    t_in_period = t % period
    
    if t_in_period < duty_cycle * period:
        return 1.0  # Высокий уровень
    else:
        return 0.0  # Низкий уровень

def get_triangle_wave_amplitude(freq, t):
    period = 1.0 / freq
    t_in_period = t % period
    if t_in_period < period / 2:
        return 2 * t_in_period / period
    else:
        return 2 - 2 * t_in_period / period

def get_sawtooth_wave_amplitude(freq, t):
    period = 1.0 / freq
    t_in_period = t % period
    return t_in_period / period
