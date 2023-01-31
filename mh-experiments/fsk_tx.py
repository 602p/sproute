import array
import math
import time
import sys

from fsk_common import *

import pyaudio

p = pyaudio.PyAudio()

message = "\n\nMessage using a homebrew MFSK mode DE KF0CGO.\n\n"
message = '[ABCDEF]'
output = bytes()

# bit_clk *= 4

stream = p.open(format=pyaudio.paFloat32,
                #output_device_index=tx_dev_index,
                channels=2,
                rate=sr,
                output=True)

output = gen_samples([], 0.2)

for _ in range(100):
    for b in range(len(symbols)):
        print(b)
        ts = tones_for_byte(b)
        output = gen_samples(ts, bit_clk)
        stream.write(output)

stream.stop_stream()
stream.close()

p.terminate()

