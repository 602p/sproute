import math
import numpy as np
import itertools
import array
import os
import random

import sounddevice

message = "This message sent using a homebrew\naudio interface and homebrew\nFSK digimode DE KF0CGO.\nOver just Baofengs!\n ~~ (:3) (:3) (:3) ~~"


def get_tx_dev(phys_sr):
    if os.name == 'nt': return None

    for i, dev in enumerate(sounddevice.query_devices()):
        if "USB Audio Device" in dev['name'] and dev['max_output_channels']:
            sounddevice.check_output_settings(device=i, channels=2, samplerate=phys_sr)
            return i

def get_rx_dev(phys_sr):
    if os.name == 'nt': return None

    for i, dev in enumerate(sounddevice.query_devices()):
        if "USB Audio Device" in dev['name'] and dev['max_input_channels']:
            sounddevice.check_input_settings(device=i, channels=1, samplerate=phys_sr)
            return i

phys_sr = 48000  # sampling rate, Hz, must be integer

downscale = 1

bit_clk = 0.006

phys_blk_time = bit_clk
interpolate_factor = 1
window_blks = 20

bin_coalesce = 3 * downscale
simul_tones = 1

phys_blk_size = int(phys_blk_time * phys_sr)
phys_blk_time = phys_blk_size / phys_sr # exact number

chunk_size = phys_blk_size // window_blks
chunk_time = chunk_size / phys_sr

interp_blk_size = phys_blk_size * interpolate_factor
interp_sr = phys_sr * interpolate_factor

print('bit:', bit_clk, 's; blk:', phys_blk_time, 's (',phys_blk_size,' S, ',chunk_size,'S chunks)')

min_freq = 300
max_freq = 2800

freq = np.fft.rfftfreq(interp_blk_size, d=1/interp_sr)

print(freq, '--', len(freq), 'bins raw')

start = np.argmax(freq > min_freq)
stop = np.argmax(freq > max_freq)

freq = freq[start:stop]

print(freq, '--', len(freq), 'tones')

tonebins = []
from_freq = list(freq)
del from_freq[:(len(from_freq)%bin_coalesce)//2]
while len(from_freq)>=bin_coalesce:
    tonebins.append(sum(from_freq[:bin_coalesce])/bin_coalesce)
    del from_freq[:bin_coalesce]

print(tonebins,len(tonebins), 'bins')

# tones = list(freq)

print(simul_tones, 'simul tones')

symbols = [set(x) for x in itertools.combinations(tonebins, simul_tones)]
# clock_tone = tonebins[-1]

# print('clock tone:', clock_tone)

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

    volume *= (random.random() / 3) + 0.5

    # generate samples, note conversion to float32 array
    num_samples = int(phys_sr * duration)

    out_samples = []
    for i in range(0, num_samples):
        samp = 0
        for tone in tones:
            samp += volume/len(tones) * math.sin(2 * math.pi * i * tone / phys_sr)

        out_samples.append(samp)

        if ptt_tone:
            out_samples.append(ptt_tone_volume * math.sin(2 * math.pi * i * 1000 / phys_sr))
        
    output_bytes = array.array('f', out_samples).tobytes()

    return output_bytes
