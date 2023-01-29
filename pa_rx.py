import array
import math
import time

import pyaudio

p = pyaudio.PyAudio()

fs = 44100  # sampling rate, Hz, must be integer

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                input=True)

BLKSZ = 128
t = 0
i = 0

win = [0] * 48

clk_time = 0.1

frame_start = 0
in_frame = False
frame_bits = []

while 1:
    block = stream.read(BLKSZ)
    arr = array.array('f')
    arr.frombytes(block)

    mval = max([abs(x) for x in arr])
    bit = mval > 0.01

    win.insert(0, bit)
    del win[-1]

    debounced = all(win)

    if debounced and not in_frame:
        in_frame = True
        frame_start = t

    if in_frame and (t - frame_bits) > (len(frame_bits) * clk_time):
        frame_bits.append(not debounced)

    if len(frame_bits) == 8:
        in_frame = False
        print(frame_bits)

    # if (i % 10) == 0:
    #     print(f'{t: 2.2f} {debounced}')

    t += BLKSZ / fs
    i += 1

stream.stop_stream()
stream.close()

p.terminate()
