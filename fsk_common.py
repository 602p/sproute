import math
import numpy as np
import itertools

import sounddevice

rx_dev_index = None
tx_dev_index = None

# print(sounddevice.query_devices())

for i, dev in enumerate(sounddevice.query_devices()):
    if "USB Audio Device" in dev['name'] and dev['max_input_channels']:
        rx_dev_index = i
    if "USB Audio Device" in dev['name'] and dev['max_output_channels']:
        tx_dev_index = i

assert rx_dev_index is not None and tx_dev_index is not None

sr = 48000  # sampling rate, Hz, must be integer

sounddevice.check_input_settings(device=rx_dev_index, channels=1, samplerate=sr)
sounddevice.check_output_settings(device=tx_dev_index, channels=2, samplerate=sr)

print("dev", rx_dev_index, "/", tx_dev_index, "=", dev['name'], "; sr", sr, "OK")

bit_clk = 0.4
simul_tones = 1
bin_coalesce = 14

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

tonebins = []
from_freq = list(freq)
while len(from_freq)>=bin_coalesce:
    tonebins.append(from_freq[:bin_coalesce][bin_coalesce//2])
    del from_freq[:bin_coalesce]

print(tonebins,len(tonebins), 'bins')

# tones = list(freq)

print(simul_tones, 'simul tones')

symbols = [set(x) for x in itertools.combinations(tonebins[:-1], simul_tones)]
clock_tone = tonebins[-1]

print('clock tone:', clock_tone)

print(len(symbols), 'combinations;', math.log2(len(symbols)), 'bits')
# assert(len(symbols) >= 2**4)

def tones_for_byte(b):
    return symbols[b]

def byte_for_tones(ts):
    return symbols.index(set(ts))
