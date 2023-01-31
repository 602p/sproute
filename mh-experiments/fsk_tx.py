import array
import math
import time

from fsk_common import *

import pyaudio

p = pyaudio.PyAudio()

message = "\n\nMessage using a homebrew MFSK mode DE KF0CGO.\n\n"
message = '[ABCDEF]'
output = bytes()

bit_clk *= 3

# output = gen_samples([500], 3)

output += gen_samples([], bit_clk * 4, 0)

i = 0
for b in bytes(message, encoding='utf-8'):
    print(b, end=' ')
    ts = tones_for_byte(b & 0b1111) | {clock_tone}
    print(list(sorted(ts)), end=' ')
    output += gen_samples(ts, bit_clk)

    output += gen_samples([], bit_clk, 0)

    ts = tones_for_byte(b >> 4)
    print(list(sorted(ts)))
    output += gen_samples(ts, bit_clk)

    output += gen_samples([], bit_clk, 0)
    i += 1

input("READY")

stream = p.open(format=pyaudio.paFloat32,
                #output_device_index=tx_dev_index,
                channels=2,
                rate=sr,
                output=True)

stream.write(output)

stream.stop_stream()
stream.close()

p.terminate()

