import array
import math
import time
import sys

import pyaudio

ptt_tone_volume = 1

phys_sr = 48000

def gen_samples(tones, duration, volume=0.8, ptt_tone=True):
    # volume = 0.5 # range [0.0, 1.0]
    # duration = 0.5  # in seconds, may be float
    # f = 1000.0  # sine frequency, Hz, may be float

    # volume *= (random.random() / 3) + 0.5

    # generate samples, note conversion to float32 array
    num_samples = int(phys_sr * duration)

    out_samples = []
    for i in range(0, num_samples):
        samp = 0
        for tone in tones:
            samp += abs(volume/len(tones) * math.sin(2 * math.pi * i * tone / phys_sr))

        out_samples.append(samp)

        if ptt_tone:
            out_samples.append(ptt_tone_volume * math.sin(2 * math.pi * i * 1000 / phys_sr))
        
    output_bytes = array.array('f', out_samples).tobytes()

    return output_bytes


p = pyaudio.PyAudio()

output = bytes()

stream = p.open(format=pyaudio.paFloat32,
                output_device_index=None, #get_tx_dev(phys_sr),
                channels=2,
                rate=phys_sr,
                output=True)

output = gen_samples([], 0.2)

output += gen_samples([1000], 5)

input("READY")

stream.write(output)

stream.stop_stream()
stream.close()

p.terminate()

