import array
import math
import time
import sys

from fsk_common import *

import pyaudio

p = pyaudio.PyAudio()

# message = "This message sent using a homebrew\naudio interface and homebrew\nFSK digimode DE KF0CGO.\nOver just Baofengs!\n ~~ (:3) (:3) (:3) ~~"
# message = "ABCD" * 10

# message = message.split('\n')[0]

nsyms = len(symbols)
assert(nsyms-1 >= 4)

frames = [('[LEAD]', 0, 0)] * 40
for b in message.encode('utf-8'):
    for n in ([(b>>6) & 0b11, (b >> 4) & 0b11, (b >> 2) & 0b11, b & 0b11]):
        last = frames[-1][-1]
        frames.append((chr(b), n, (last + n + 1) % nsyms))

frames += [frames[-1]] * 10

output = bytes()

stream = p.open(format=pyaudio.paFloat32,
                output_device_index=get_tx_dev(phys_sr),
                channels=2,
                rate=phys_sr,
                output=True)

output = gen_samples([], 0.2)

for char, nybble, sym in frames:
    print('C:', char, 'NYB:', bin(nybble), 'TX SYM:', sym)
    ts = tones_for_byte(sym)
    output += gen_samples(ts, tx_bit_clk)

# for _ in range(10):
#     for sym in symbols:
#         output += gen_samples(sym, tx_bit_clk)

input("READY")

stream.write(output)

stream.stop_stream()
stream.close()

p.terminate()

