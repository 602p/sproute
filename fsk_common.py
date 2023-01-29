import math
import numpy as np
import itertools

sr = 44100 * 4  # sampling rate, Hz, must be integer

BLKSZ = 1024 * 16

bit_clk = (BLKSZ / sr) * 2

min_freq = 500
max_freq = 2500

freq = np.fft.fftfreq(BLKSZ, d=1/sr)
start = np.argmax(freq > min_freq)
stop = np.argmax(freq > max_freq)

print(start, stop)

freq = freq[start:stop]

print(stop-start, 'useful bins')

tone_step = 160
tones = list(range(min_freq+tone_step, max_freq, tone_step))
# tones = tones[:8]
print(len(tones), 'tones')

simul_tones = 3
print(simul_tones, 'simul tones')

tone_bin_size = tone_step / 2

symbols = [set(x) for x in itertools.combinations(tones[:-1], simul_tones)]
clock_tone = tones[-1]

print('clock tone:', clock_tone)

print(len(symbols), 'combinations;', math.log2(len(symbols)), 'bits')
# symbols = symbols[:256]
assert(len(symbols) >= 128)

print(len(symbols))

def tones_for_byte(b):
    return symbols[b]

def byte_for_tones(ts):
    return symbols.index(set(ts))
