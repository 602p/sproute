

import pyaudio

p = pyaudio.PyAudio()

srs = [32000, 44100, 48000, 96000, 128000]

for sr in srs:
	if p.is_format_supported(44100.0,  # Sample rate
                         input_device=devinfo['index'],
                         input_channels=2,
                         input_format=pyaudio.paFloat32):
  	print 'Yay!'
