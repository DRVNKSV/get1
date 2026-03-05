import numpy as np
import time
def get_tr_value(freq, time):
    period = 1.0 / freq
    phase = (time % period) / period
    if phase < 0.5:
        return 2 * phase
    else:
        return 2 - 2 * phase

def wait_for_sampling_period(sampling_frequency):
    time.sleep(1 / sampling_frequency)
