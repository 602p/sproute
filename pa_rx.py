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

while 1:
    block = stream.read(1024)
    arr = array.array('f')
    arr.frombytes(block)
    # print(max(arr))
    if max(arr) > 0.05:
        print('ON')

stream.stop_stream()
stream.close()

p.terminate()
