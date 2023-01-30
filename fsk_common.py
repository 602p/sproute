import math
import numpy as np
import itertools

import sounddevice

dev_index = None

# print(sounddevice.query_devices())

for i, dev in enumerate(sounddevice.query_devices()):
    if dev['name'].startswith("USB Audio Device"):
        dev_index = i
        break

assert dev_index is not None

sr = 48000  # sampling rate, Hz, must be integer

sounddevice.check_input_settings(device=dev_index, channels=1, samplerate=sr)
sounddevice.check_output_settings(device=dev_index, channels=2, samplerate=sr)

print("dev", dev_index, "/", dev['name'], "; sr", sr, "OK")

bit_clk = 0.1
simul_tones = 1

blk_time = bit_clk / 4

blk_size = int(blk_time * sr)
blk_time = blk_size / sr # exact number

print('bit:', bit_clk, 's; blk:', blk_time, 's (',blk_size,' S)')

min_freq = 300
max_freq = 2800

freq = np.fft.fftfreq(blk_size, d=1/sr)
start = np.argmax(freq > min_freq)
stop = np.argmax(freq > max_freq)

freq = freq[start:stop]

print(freq, '--', len(freq), 'tones')

tones = list(freq)

print(simul_tones, 'simul tones')

symbols = [set(x) for x in itertools.combinations(tones[:-1], simul_tones)]
clock_tone = tones[-1]

print('clock tone:', clock_tone)

print(len(symbols), 'combinations;', math.log2(len(symbols)), 'bits')
# assert(len(symbols) >= 2**4)

def tones_for_byte(b):
    return symbols[b]

def byte_for_tones(ts):
    return symbols.index(set(ts))
