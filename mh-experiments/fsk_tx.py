import array
import math
import time
import sys

from fsk_common import *

import pyaudio

p = pyaudio.PyAudio()

message = "This message sent using a homebrew\naudio interface and homebrew\nFSK digimode DE KF0CGO.\nOver just Baofengs!\n ~~ (:3) (:3) (:3) ~~"
# message = "ABCD" * 10

nsyms = len(symbols)
assert(nsyms-1 == 4)

frames = [('[LEAD]', 0, 0)] * 10
for b in message.encode('utf-8'):
    for n in ([(b>>6) & 0b11, (b >> 4) & 0b11, (b >> 2) & 0b11, b & 0b11]):
        last = frames[-1][-1]
        frames.append((chr(b), n, (last + n + 1) % nsyms))

frames += [frames[-1]] * 10

output = bytes()

bit_clk *= 1.8

stream = p.open(format=pyaudio.paFloat32,
                #output_device_index=tx_dev_index,
                channels=2,
                rate=sr,
                output=True)

output = bytes() #gen_samples([], 0.2)

for char, nybble, sym in frames:
    print('C:', char, 'NYB:', bin(nybble), 'TX SYM:', sym)
    ts = tones_for_byte(sym)
    output = gen_samples(ts, bit_clk)
    stream.write(output)

stream.stop_stream()
stream.close()

p.terminate()

