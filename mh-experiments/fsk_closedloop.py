import array
import math
import time
import os
import numpy as np
import string
from fsk_common import *
import random
from scipy import signal

import pyaudio


print('----------------')

output = gen_samples(symbols[-1], bit_clk, ptt_tone=False)

print('output:', len(output), 'S')

block = np.frombuffer(output, dtype=np.float32)
buf = list(block[:blk_size])

print(buf[0:5])

for i in range(len(buf)):
	buf[i] += (random.random()-0.5) * 0.1


def abs2(x):
    return x.real**2 + x.imag**2

tuckey_window=signal.tukey(len(buf),0.5,True)
buf=buf*tuckey_window
buf -= np.mean(buf)
fft = np.fft.rfft(buf, norm='ortho')
fft = abs2(fft[start:stop])

pairs_raw = list(zip(freq, fft))

pairs = []
while len(pairs_raw) >= bin_coalesce:
    ps = pairs_raw[:bin_coalesce]
    del pairs_raw[:bin_coalesce]
    pairs.append((ps[bin_coalesce//2][0], sum(x[1] for x in ps)))

# print(pairs)

pairs.sort(key=lambda x: x[1], reverse=True)
top = [x[0] for x in pairs[:simul_tones]]
top.sort()

# clock_hi = clock_tone in top
# if clock_hi:
#     top.remove(clock_tone)
# else:
#     top.remove(pairs[simul_tones][0])

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

plt.plot(freq, fft)

print(pairs)

freqstep = freq[1] - freq[0]
binwidth = freqstep * bin_coalesce
for t in tonebins:
    ax.add_patch(plt.Rectangle((t-(binwidth/2), 0), binwidth, max(fft), color='b', fill=False))

for f, v in pairs[:2]:
    print("F", f, "V", v)
    ax.add_patch(plt.Rectangle((f-binwidth/4, 0), binwidth/2, max(fft), color=(1, 0.8, 0.8)))

plt.show()