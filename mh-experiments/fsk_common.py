import math
import numpy as np
import itertools
import array
import os
import random

import sounddevice
import textwrap

message = "" \
    "This longer message sent using a" \
    "\nhomebrew audio interface and" \
    "\nhomebrew digimode DE KF0CGO." \
    "\nNow over 520bit/s ..." \
    "\nMinor improvement via coherent" \
    "\nFSK tones. But hey, half a kbps!" \
    "\n ~~ (:3) (:3) (:3) ~~ \n"


def get_tx_dev(phys_sr):
    return None

    if os.name == 'nt': return None

    for i, dev in enumerate(sounddevice.query_devices()):
        if "USB Audio Device" in dev['name'] and dev['max_output_channels']:
            sounddevice.check_output_settings(device=i, channels=2, samplerate=phys_sr)
            return i

def get_rx_dev(phys_sr):
    return None

    if os.name == 'nt': return None

    for i, dev in enumerate(sounddevice.query_devices()):
        if "USB Audio Device" in dev['name'] and dev['max_input_channels']:
            sounddevice.check_input_settings(device=i, channels=1, samplerate=phys_sr)
            return i

phys_sr = 48000  # sampling rate, Hz, must be integer

bit_clk = 0.004
tx_bit_clk = bit_clk * 1.05 # * 20 #* 30

phys_blk_time = bit_clk
interpolate_factor = 1
window_blks = 16
agree_blocks_req = 0.4

bin_coalesce = 2
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

