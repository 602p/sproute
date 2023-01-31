import math
import numpy as np
import itertools
import array

import sounddevice

rx_dev_index = None
tx_dev_index = None

# print(sounddevice.query_devices())

for i, dev in enumerate(sounddevice.query_devices()):
    if "USB Audio Device" in dev['name'] and dev['max_input_channels']:
        rx_dev_index = i
    if "USB Audio Device" in dev['name'] and dev['max_output_channels']:
        tx_dev_index = i

# assert rx_dev_index is not None and tx_dev_index is not None

sr = 48000  # sampling rate, Hz, must be integer

sounddevice.check_input_settings(device=rx_dev_index, channels=1, samplerate=sr)
sounddevice.check_output_settings(device=tx_dev_index, channels=2, samplerate=sr)

print("dev", rx_dev_index, "/", tx_dev_index, "=", dev['name'], "; sr", sr, "OK")

bit_clk = 0.01
simul_tones = 2
bin_coalesce = 1

blk_time = bit_clk / 4

blk_size = int(blk_time * sr)
blk_time = blk_size / sr # exact number

print('bit:', bit_clk, 's; blk:', blk_time, 's (',blk_size,' S)')

min_freq = 300
max_freq = 2800

freq = np.fft.rfftfreq(blk_size, d=1/sr)
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

ptt_tone_volume = 0

def gen_samples(tones, duration, volume=0.8, ptt_tone=True):
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

        if ptt_tone:
            out_samples.append(ptt_tone_volume * math.sin(2 * math.pi * i * 1000 / sr))
        
    output_bytes = array.array('f', out_samples).tobytes()

    return output_bytes
