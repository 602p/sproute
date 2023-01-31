import array
import math
import time
import os
import numpy as np

import pyaudio

p = pyaudio.PyAudio()

sr = 44100 * 4  # sampling rate, Hz, must be integer

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sr,
                input=True)

BLKSZ = 1024 * 6
t = 0
i = 0

time_per_sample = BLKSZ / sr

print('block_rate:', 1/time_per_sample, '(Hz)')

freq = np.fft.fftfreq(BLKSZ, d=1/sr)
start = np.argmax(freq > 500)
stop = np.argmax(freq > 2500)

print(start, stop)

freq = freq[start:stop]

print(stop-start, 'bins')

tones = [
    1209,
    1336,
    1477,
    1633,

    697,
    770,
    852,
    941
]

dtmf = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

def get_dtmf(t1, t2):
    coltone = max(t1, t2)
    rowtone = min(t1, t2)
    col = tones.index(coltone)
    row = tones.index(rowtone) - 4
    if col >= 0 and col < 4 and row >= 0 and row < 4:
        return dtmf[row][col]
    return None

tone_bin_size = 100 / 2

start_t = time.time()

while 1:
    block = stream.read(BLKSZ)
    buf = np.frombuffer(block, dtype=np.float32)

    fft = np.fft.fft(buf)
    fft = fft[start:stop]

    tone_power = {k:0 for k in tones}

    for f, v in zip(freq, fft):
        for t in tones:
            if abs(f - t) < tone_bin_size:
                tone_power[t] += abs(v)

    pairs = list(tone_power.items())
    pairs.sort(key=lambda x: x[1], reverse=True)
    toptwo = [x[0] for x in pairs[:2]]
    highest_power = pairs[0][1]

    if highest_power > 5:
        code = get_dtmf(*toptwo)
        if code:
            print(code)

    t += time_per_sample
    i += 1


stream.stop_stream()
stream.close()

p.terminate()


# import matplotlib.pyplot as plt
# plt.plot(freq, np.abs(fft))

# # plt.xlim(0, 5000)
# plt.show()