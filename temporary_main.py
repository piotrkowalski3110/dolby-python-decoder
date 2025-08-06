import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from scipy.io import wavfile
from scipy.signal import butter, lfilter
from conversion import convertToFloat

# Read audio file
sampleRate, inputAudio = wavfile.read('source/Test2.wav')
inputAudio = convertToFloat(inputAudio)

# Split to left and right channel
if inputAudio.ndim == 2 and inputAudio.shape[1] == 2:
    leftChannel = inputAudio[:, 0]
    rightChannel = inputAudio[:, 1]
else:
    raise ValueError('Audio is not stereo!')

# Auxiliary variables
damping3dB = np.sqrt(2) / 2
damping6dB = (np.sqrt(2) / 2) * (np.sqrt(2) / 2)
surroundDelayed = np.zeros((len(inputAudio), 1))

# Creation of low-pass and band-pass filters
[numdLow, dendLow] = butter(3, 80, fs=sampleRate, btype='lowpass')
[numdPass, dendPass] = butter(2, [100, 7000], fs=sampleRate, btype='bandpass')

# Delay variables
delayTime = 5 * 10 ** (-3)
delayN = int(np.floor(delayTime / (1 / sampleRate)))

# Surrond Channel Creation
surroundBeforeFiltering = (leftChannel - rightChannel) * damping3dB
surroundDelayed[delayN:, 0] = surroundBeforeFiltering[:-delayN]
surroundAfterFilter = lfilter(numdPass, dendPass, surroundDelayed[:, 0])
surroundLeft = surroundAfterFilter
surroundRight = surroundAfterFilter * (-1)

# Central and Subwoofer Channel Creation
centralChannel = ((leftChannel + rightChannel) * damping6dB)
subwooferChannel = lfilter(numdLow, dendLow, centralChannel)

# Read amplitudes on result signals
LF = max(abs(np.max(leftChannel[14999:30000])), abs(np.min(leftChannel[14999:30000])))
C = max(abs(np.max(centralChannel[14999:30000])), abs(np.min(centralChannel[14999:30000])))
RF = max(abs(np.max(rightChannel[14999:30000])), abs(np.min(rightChannel[14999:30000])))
LFE = max(abs(np.max(subwooferChannel[14999:30000])), abs(np.min(subwooferChannel[14999:30000])))
SL = max(abs(np.max(surroundLeft[14999:30000])), abs(np.min(surroundLeft[14999:30000])))
SR = max(abs(np.max(surroundRight[14999:30000])), abs(np.min(surroundRight[14999:30000])))

# Print results
print(f'Lewy front (LF): {LF:.6f}')
print(f'Centralny (C): {C:.6f}')
print(f'Prawy front (RF): {RF:.6f}')
print(f'Subwoofer (LFE): {LFE:.6f}')
print(f'Lewy surround: {SL:.6f}')
print(f'Prawy surround: {SR:.6f}')
