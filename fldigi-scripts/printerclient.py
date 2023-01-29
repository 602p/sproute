import pyfldigi, time, threading, sys
# app = pyfldigi.ApplicationMonitor()
# app.start()
# time.sleep(1)

printer = open('/dev/usb/lp0', 'w')

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

def send_task():
	while 1:
		fldigi.main.send(padding + framing + mycall + ': ' + input() + framing + padding)

threading.Thread(target=send_task).start()

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
			print(message)
			printer.write('\n\n-----------\n'+message+'\n-----------\n\n')
			printer.flush()
			text = ''
		# else:
		# 	print(repr(text), left, right)
