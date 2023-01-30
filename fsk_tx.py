import array
import math
import time

from fsk_common import *

import pyaudio

p = pyaudio.PyAudio()

ptt_tone_volume = 1

def gen_samples(tones, duration, volume=0.8):
    # volume = 0.5 # range [0.0, 1.0]
    # duration = 0.5  # in seconds, may be float
    # f = 1000.0  # sine frequency, Hz, may be float

    # generate samples, note conversion to float32 array
    num_samples = int(sr * duration)

    out_samples = []
    for i in range(0, num_samples):
        samp = 0
        for tone in tones:
            samp += volume/len(tones) * math.sin(2 * math.pi * i * tone / sr)

        out_samples.append(samp)
        out_samples.append(ptt_tone_volume * math.sin(2 * math.pi * i * 1000 / sr))
        
    output_bytes = array.array('f', out_samples).tobytes()

    return output_bytes


message = "\n\nMessage using a homebrew MFSK mode DE KF0CGO.\n\n"
message = '[ABCDEF]'
output = bytes()

# bit_clk *= 3

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
                output_device_index=tx_dev_index,
                channels=2,
                rate=sr,
                output=True)

stream.write(output)

stream.stop_stream()
stream.close()

p.terminate()

