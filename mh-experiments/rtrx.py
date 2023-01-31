import pygame

pygame.init()

screen = pygame.display.set_mode((1920, 1080))

import array
import math
import time
import os
import numpy as np
import string
from fsk_common import *
import random

from scipy import signal

import pyaudio

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                input_device_index=rx_dev_index,
                channels=1,
                rate=sr,
                input=True)

start_t = time.time()

byte = None
msg = ''
last = {}

acceptnext = False

def abs2(x):
    return x.real**2 + x.imag**2

vnorm = 0

font = pygame.font.SysFont("monospace", 80, True)
def draw(text, pos, color=(255,255,255)):
    screen.blit(font.render(text, True, color), pos)

# last = [0]*len(freq)

while 1:
    block = stream.read(blk_size, exception_on_overflow=False)
    buf = np.frombuffer(block, dtype=np.float32)

    tuckey_window=signal.tukey(len(buf),0.5,True)
    buf=buf*tuckey_window
    buf -= np.mean(buf)
    fft = np.fft.rfft(buf, norm='ortho')
    fft = abs2(fft[start:stop])

    # tmp = last.copy()
    # last = fft.copy()
    # fft += tmp

    pairs_raw = list(zip(freq, fft))

    pairs = []
    del pairs_raw[:(len(pairs_raw)%bin_coalesce)//2]
    while len(pairs_raw) >= bin_coalesce:
        ps = pairs_raw[:bin_coalesce]
        del pairs_raw[:bin_coalesce]
        pairs.append((ps[bin_coalesce//2][0], sum(x[1] for x in ps)))

    # print(pairs)

    pairs.sort(key=lambda x: x[1], reverse=True)
    top = [x[0] for x in pairs[:simul_tones]]
    top.sort()

    # clock_hi = clock_tone in top
    # if clock_hi:
    #     top.remove(clock_tone)
    # else:
    #     top.remove(pairs[simul_tones][0])

    screen.fill((0,0,0))


    freqstep = freq[1] - freq[0]

    vnorm = pairs[0][1]*1.1 #max(vnorm, pairs[0][1]*1.1)
    
    height = 1000

    last_x = freq[0]-freqstep
    last_y = 0

    hnorm = freq[-1] / 1800

    for f, v in zip(freq, fft):
        pygame.draw.line(screen, (0,255,0), (last_x/hnorm,height - last_y*height/vnorm), (f/hnorm, height - v*height/vnorm))
        last_x = f
        last_y = v

    pygame.draw.line(screen, (0,255,0), (last_x/hnorm,height - last_y*height/vnorm), ((freq[-1]+freqstep)/hnorm, height))

    binwidth = freqstep * bin_coalesce
    for t in tonebins:
        pygame.draw.rect(screen, (0,0,255), ((t-(binwidth/2))/hnorm, 0, binwidth/hnorm, height), width=2)

    binwidth = freqstep * bin_coalesce
    for t in top:
        pygame.draw.rect(screen, (255,0,0), ((t-(binwidth/2))/hnorm + 5, 5, binwidth/hnorm - 5, height - 5), width=5)

    if math.log(pairs[0][1]) > -14:
        try:
            b = byte_for_tones(top)
        except ValueError:
            b = -1
        print(b)
        draw("D:"+str(b), (0, 0), color=(200,255,200) if b!=-1 else (255,100,100))
    else:
        print('NO', pairs[0][1])
        draw("SQL", (0, 0), color=(255,200,200))

    draw(f"T1:e{math.log(pairs[0][1]):5.1f}", (0, 80))
    draw(f"T2:e{math.log(pairs[1][1]):5.1f}", (0, 160))

    pygame.display.flip()

# import matplotlib.pyplot as plt

# fig, ax = plt.subplots()

# plt.plot(freq, fft)

# print(pairs)

# freqstep = freq[1] - freq[0]
# binwidth = freqstep * bin_coalesce
# for t in tonebins:
#     ax.add_patch(plt.Rectangle((t-(binwidth/2), 0), binwidth, max(fft), color='b', fill=False))

# for f, v in pairs[:2]:
#     print("F", f, "V", v)
#     ax.add_patch(plt.Rectangle((f-binwidth/4, 0), binwidth/2, max(fft), color=(1, 0.8, 0.8)))

# plt.show()

    # break

    # highest_power = pairs[0][1]

    # if highest_power > 5:
        
    #     b = byte_for_tones(top)
    #     print(int(clock_hi), list(sorted(top)), byte, b)

    #     if byte is None and clock_hi:
    #         if not acceptnext:
    #             acceptnext = True
    #             continue
    #         acceptnext = False

    #         byte = b
    #     elif byte is not None and not clock_hi:
    #         if not acceptnext:
    #             acceptnext = True
    #             continue
    #         acceptnext = False

    #         byte = byte + (b << 4)

    #         print("RX:", byte)

    #         if chr(byte) in string.printable:
    #             msg += chr(byte)
    #             # print('rx byte:', byte)
    #             # os.system('clear')
    #             print(msg)

    #         byte = None



stream.stop_stream()
stream.close()

p.terminate()


