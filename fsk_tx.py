import array
import math
import time


from fsk_common import *

import pyaudio

p = pyaudio.PyAudio()

fs = 44100 * 4  # sampling rate, Hz, must be integer

def gen_samples(tones, duration, volume=0.8):
    # volume = 0.5 # range [0.0, 1.0]
    # duration = 0.5  # in seconds, may be float
    # f = 1000.0  # sine frequency, Hz, may be float

    # generate samples, note conversion to float32 array
    num_samples = int(fs * duration)

    out_samples = []
    for i in range(0, num_samples):
        samp = 0
        for tone in tones:
            samp += volume/len(tones) * math.sin(2 * math.pi * i * tone / fs)

        out_samples.append(samp)
        out_samples.append(1 * math.sin(2 * math.pi * i * 1000 / fs))
        
    output_bytes = array.array('f', out_samples).tobytes()

    return output_bytes


message = "\n\nHello from linux -> windows DE KF0CGO\nLonger message :3\n"
output = bytes()

bit_clk = 0.1

output += gen_samples([], bit_clk * 12, 0)

for b in bytes(message, encoding='utf-8'):
    print(b)
    ts = tones_for_byte(b)
    print(ts)
    output += gen_samples(ts, bit_clk)

stream = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=fs,
                output=True)

stream.write(output)

stream.stop_stream()
stream.close()

p.terminate()