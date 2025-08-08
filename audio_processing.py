import numpy as np
from scipy.signal import butter, lfilter

from conversion import convertToFloat


def process_audio_channels(input_audio, sample_rate, damping_3dB):
    input_audio = convertToFloat(input_audio)

    # Split to left and right channel
    if input_audio.ndim == 2 and input_audio.shape[1] == 2:
        left_channel = input_audio[:, 0]
        right_channel = input_audio[:, 1]
    else:
        raise ValueError("Audio is not stereo!")

    # Auxiliary variables
    damping_6dB = (np.sqrt(2) / 2) * (np.sqrt(2) / 2)
    surround_delayed = np.zeros((len(input_audio), 1))

    # Creation of low-pass and band-pass filters
    [num_d_low, den_d_low] = butter(3, 80, fs=sample_rate, btype="lowpass")
    [num_d_pass, den_d_pass] = butter(2, [100, 7000], fs=sample_rate, btype="bandpass")

    # Delay variables
    delay_time = 5 * 10 ** (-3)
    delay_n = int(np.floor(delay_time / (1 / sample_rate)))

    # Surround Channel Creation
    surround_before_filtering = (left_channel - right_channel) * damping_3dB
    surround_delayed[delay_n:, 0] = surround_before_filtering[:-delay_n]
    surround_after_filter = lfilter(num_d_pass, den_d_pass, surround_delayed[:, 0])
    surround_left = surround_after_filter
    surround_right = surround_after_filter * (-1)

    # Central and Subwoofer Channel Creation
    central_channel = (left_channel + right_channel) * damping_6dB
    subwoofer_channel = lfilter(num_d_low, den_d_low, central_channel)

    # Return a dictionary of the processed audio channels
    channels = {
        "left_front": left_channel,
        "right_front": right_channel,
        "center": central_channel,
        "lfe": subwoofer_channel,
        "left_surround": surround_left,
        "right_surround": surround_right,
    }

    return channels
