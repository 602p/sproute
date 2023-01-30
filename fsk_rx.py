import array
import math
import time
import os
import numpy as np
import string
from fsk_common import *

import pyaudio

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                input_device_index=rx_dev_index,
                channels=1,
                rate=sr,
                input=True)

start_t = time.time()

byte = None
msg = ''
last = {}

acceptnext = False

while 1:
    block = stream.read(blk_size)
    buf = np.frombuffer(block, dtype=np.float32)

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
    top = [x[0] for x in pairs[:simul_tones+1]]
    top.sort()

    clock_hi = clock_tone in top
    if clock_hi:
        top.remove(clock_tone)
    else:
        top.remove(pairs[simul_tones][0])

    break

    highest_power = pairs[0][1]

    if highest_power > 5:
        
        b = byte_for_tones(top)
        print(int(clock_hi), list(sorted(top)), byte, b)

        if byte is None and clock_hi:
            if not acceptnext:
                acceptnext = True
                continue
            acceptnext = False

            byte = b
        elif byte is not None and not clock_hi:
            if not acceptnext:
                acceptnext = True
                continue
            acceptnext = False

            byte = byte + (b << 4)

            print("RX:", byte)

            if chr(byte) in string.printable:
                msg += chr(byte)
                # print('rx byte:', byte)
                # os.system('clear')
                print(msg)

            byte = None



stream.stop_stream()
stream.close()

p.terminate()


# import matplotlib.pyplot as plt

# fig, ax = plt.subplots()

# plt.plot(freq, fft)

# print(pairs)

# freqstep = freq[1] - freq[0]
# binwidth = freqstep * bin_coalesce
# for t in tonebins:
#     ax.add_patch(plt.Rectangle((t-(binwidth/2), 0), binwidth, max(fft), color='b', fill=False))

# for f, v in pairs[:2]:
#     print("F", f, "V", v)
#     ax.add_patch(plt.Rectangle((f-10, 0), 20, max(fft), color='r'))

# plt.show()