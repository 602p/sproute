import array
import math
import time
import sys

from fsk_common import *

import pyaudio

p = pyaudio.PyAudio()

ptt_tone_volume =  0.8

def gen_samples(tones, duration, volume=0.8, ptt_tone=True):
    tone, = tones

    if volume:
        volume += 0.5 * ((tone-3000)/3000)

    if tone == 625.0:
        volume -= 0.1

    samp_per_wave = phys_sr / tone

    # num_samples = int(phys_sr * duration)
    num_samples = int(samp_per_wave * (math.floor((phys_sr * duration) / samp_per_wave)))
    # num_samples = math.ceil(samp_per_wave) * 9

    out_samples = []
    for i in range(0, num_samples):
        samp = volume * math.sin(2 * math.pi * i * tone / phys_sr)

        out_samples.append(samp)

        if ptt_tone:
            out_samples.append(ptt_tone_volume * math.sin(2 * math.pi * i * 1000 / phys_sr))
        
    output_bytes = array.array('f', out_samples).tobytes()

    return output_bytes


# message = "This message sent using a homebrew\naudio interface and homebrew\nFSK digimode DE KF0CGO.\nOver just Baofengs!\n ~~ (:3) (:3) (:3) ~~"
# message = "ABCD" * 10

# message = message.split('\n')[0]

nsyms = len(symbols)
assert(nsyms-1 >= 4)

frames = [('[LEAD]', 0, 0)] * 40
for b in message.encode('utf-8'):
    for n in ([(b>>6) & 0b11, (b >> 4) & 0b11, (b >> 2) & 0b11, b & 0b11]):
        last = frames[-1][-1]
        frames.append((chr(b), n, (last + n + 1) % nsyms))

frames += [frames[-1]] * 10

output = bytes()

stream = p.open(format=pyaudio.paFloat32,
                output_device_index=get_tx_dev(phys_sr),
                channels=2,
                rate=phys_sr,
                output=True)

output = gen_samples([1000], 0.2, 0)

headerlen = None

for char, nybble, sym in frames:
    print('C:', char, 'NYB:', bin(nybble), 'TX SYM:', sym)
    if char != '[LEAD]' and headerlen is None:
        headerlen = len(output)

    ts = tones_for_byte(sym)
    output += gen_samples(ts, tx_bit_clk)

# for _ in range(10):
#     for sym in symbols:
#         output += gen_samples(sym, tx_bit_clk)


totallen = (len(output) - headerlen) / 4 / 2
lensec = totallen / phys_sr
print(totallen, "samples;", lensec, "sec;", (len(message)*8)/lensec, "bit/sec")

input("READY")

stream.write(output)

stream.stop_stream()
stream.close()

p.terminate()

