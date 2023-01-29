import math
import numpy as np

sr = 44100 * 4  # sampling rate, Hz, must be integer

BLKSZ = 1024 * 6

min_freq = 500
max_freq = 2500

freq = np.fft.fftfreq(BLKSZ, d=1/sr)
start = np.argmax(freq > min_freq)
stop = np.argmax(freq > max_freq)

print(start, stop)

freq = freq[start:stop]

print(stop-start, 'useful bins')

tone_step = 200
tones = list(range(min_freq+tone_step, max_freq, tone_step))
tones = tones[:8]
print(len(tones), 'tones')

simul_tones = 3
combinations = 1
for i in range(simul_tones):
    combinations *= len(tones) - i
print(simul_tones, 'simul tones;', combinations, 'combinations;', math.log2(combinations), 'bits')

tone_bin_size = tone_step / 2

symbols = []
for a in tones:
    for b in tones:
        for c in tones:
            if a != b and b != c and a != c:
                symbols.append((a, b, c))

symbols = symbols[:2**int(math.log2(combinations))]

def tones_for_byte(b):
    return symbols[b]

def byte_for_tones(ts):
    ts.sort()
    return symbols.index(ts)
