import array
import math
import time
import os

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


clk_time = 0.05

time_per_sample = BLKSZ / fs

win = [0] * int(clk_time / time_per_sample / 2)

print('winlen:', len(win))

frame_start = 0
in_frame = False
frame_bits = []


assert(len(win) * time_per_sample < clk_time * 0.5)

msg = ""


while 1:
    block = stream.read(BLKSZ)
    arr = array.array('f')
    arr.frombytes(block)

    mval = max([abs(x) for x in arr])
    bit = mval > 0.01

    win.insert(0, bit)
    del win[-1]

    debounced = all(win) #sum(win) > len(win) * 0.75

    if debounced and not in_frame:
        # print("Start Frame")
        in_frame = True
        frame_start = t + (clk_time + time_per_sample)

    if in_frame and ((t - frame_start) > ((len(frame_bits) * clk_time) + (clk_time / 2))):
        # print("Bit:", debounced)
        # print(win)
        frame_bits.append(debounced)

    if len(frame_bits) == 8:
        in_frame = False
        num = sum(x<<n for x, n in zip(frame_bits, range(0, len(frame_bits))))
        # print("End Frame:", frame_bits, num, chr(num))
        if num:
            msg += chr(num)
            # os.system("clear")
            print(msg)
        frame_bits = []

    # if (i % 10) == 0:
    #     print(f'{t: 2.2f} {debounced}')

    t += time_per_sample
    i += 1

stream.stop_stream()
stream.close()

p.terminate()
