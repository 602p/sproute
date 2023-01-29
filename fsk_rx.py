import array
import math
import time
import os
import numpy as np
from fsk_common import *

import pyaudio

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sr,
                input=True)

t = 0
i = 0

time_per_sample = BLKSZ / sr

print('block_rate:', 1/time_per_sample, '(Hz)')

start_t = time.time()

msg = ''
last = {}

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
    top = [x[0] for x in pairs[:simul_tones+1]]
    top.sort()
    highest_power = pairs[0][1]

    if highest_power > 5:
        b = byte_for_tones(top - {clock_tone})

        if top != last:
            last = top

            print('raw rx:', top, ';', end='')

            msg += chr(b)
            print('rx byte:', b)
            print(msg)

    t += time_per_sample
    i += 1


stream.stop_stream()
stream.close()

p.terminate()


# import matplotlib.pyplot as plt
# plt.plot(freq, np.abs(fft))

# # plt.xlim(0, 5000)
# plt.show()