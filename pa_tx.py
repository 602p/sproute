import array
import math
import time

import pyaudio

p = pyaudio.PyAudio()

fs = 44100  # sampling rate, Hz, must be integer

def gen_samples(f, duration, volume=0.8):
    # volume = 0.5 # range [0.0, 1.0]
    # duration = 0.5  # in seconds, may be float
    # f = 1000.0  # sine frequency, Hz, may be float

    # generate samples, note conversion to float32 array
    num_samples = int(fs * duration)
    samples = [volume * math.sin(2 * math.pi * k * f / fs) for k in range(0, num_samples)]

    out_samples = []
    for i in range(0, num_samples):
        out_samples.append(samples[i])
        out_samples.append(1 * math.sin(2 * math.pi * i * 1000 / fs))
        
    output_bytes = array.array('f', out_samples).tobytes()

    return output_bytes


message = "\n\nHello from linux -> windows DE KF0CGO\nLonger message :3\n"
output = bytes()

bit_clk = 0.05


output += gen_samples(750, bit_clk * 12, 0)

for b in bytes(message, encoding='utf-8'):
    print(b)

    output += gen_samples(750, bit_clk, 0.5)

    for i in range(8):
        bit = (b >> i) & 1

        output += gen_samples(750, bit_clk, 0.5 if bit else 0.0)

    output += gen_samples(750, bit_clk*2, 0)

stream = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=fs,
                output=True)

stream.write(output)

stream.stop_stream()
stream.close()

p.terminate()
