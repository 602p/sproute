import pyfldigi, time, threading, sys
import math
# app = pyfldigi.ApplicationMonitor()
# app.start()
# time.sleep(1)

if len(sys.argv) == 2:
	mycall = sys.argv[1]
else:
	print("Run with YOUR callsign as argument")
	sys.exit(1)

fldigi = pyfldigi.Client()
fldigi.modem.name = '8PSK500F'
fldigi.modem.carrier = 900

fldigi.main.squelch_level = 30
fldigi.text.get_rx_data()

# fldigi.main.send('TEST TEST DE KF0CGO '*10)

framing = '\n\n\n\n'
padding = 'PAD' * 10

text = ''

while 1:
	time.sleep(0.5)
	new = fldigi.text.get_rx_data().decode('ascii', errors='ignore').replace('\r','')
	if new:
		text += new
		left = text.find(framing)
		right = text.rfind(framing)
		if left != right:
			message = text[left+len(framing):right]
			c = message.split(':',1)[1].strip()
			r = eval(c)
			print(repr(message), repr(r))
			time.sleep(3)
			fldigi.main.send(padding + framing + mycall + ': ' + c + " -> " + repr(r) + framing + padding)
			text = ''
		# else:
		# 	print(repr(text), left, right)
