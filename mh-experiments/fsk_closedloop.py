import array
import math
import time
import os
import numpy as np
import string
from fsk_common import *
import random

import pyaudio


print('----------------')

output = gen_samples([tonebins[0], tonebins[2]], bit_clk, ptt_tone=False)

print('output:', len(output), 'S')

block = np.frombuffer(output, dtype=np.float32)
buf = list(block[:blk_size])

print(buf[0:5])

for i in range(len(buf)):
	buf[i] += (random.random()-0.5) * 0.1


fft = np.fft.rfft(buf)
fft = np.abs(fft[start:stop])**2

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
    ax.add_patch(plt.Rectangle((f-10, 0), 20, max(fft), color='r'))

plt.show()
