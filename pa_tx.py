import array
import math
import time

import pyaudio

p = pyaudio.PyAudio()

fs = 44100  # sampling rate, Hz, must be integer

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

def gen_samples(f, duration, volume=0.8):
    # volume = 0.5 # range [0.0, 1.0]
    # duration = 0.5  # in seconds, may be float
    # f = 1000.0  # sine frequency, Hz, may be float

    # generate samples, note conversion to float32 array
    num_samples = int(fs * duration)
    samples = [volume * math.sin(2 * math.pi * k * f / fs) for k in range(0, num_samples)]

    output_bytes = array.array('f', samples).tobytes()

    return output_bytes


message = "Hello, World"
output = bytes()

for b in bytes(message, encoding='utf-8'):
    print(b)
    for i in range(8):
        bit = (b >> i) & 1

        output += gen_samples(1000 if bit else 500, 0.05)

stream.write(output)

stream.stop_stream()
stream.close()

p.terminate()
