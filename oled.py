#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import signal
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = ssd1306(serial)

t = ""
stopNow = False
r = True

"""
def refreshTime():
	global t
	t = time.strftime("%Y-%m-%d %I:%M:%S")
"""

def updateOled():
	"""
	global t
	with canvas(device) as draw:
		draw.rectangle(device.bounding_box, outline="white", fill="black")
		draw.text((8, 24), t, fill="white")
	"""
	global r
	with canvas(device) as draw:
		draw.rectangle(device.bounding_box, outline="black", fill="black")
		for i in range(0, 14):
			if r == True:
				f = "black"
			else:
				f = "white"
			draw.rectangle([(1, i*4+1), (126, i*4+1+4)], fill=f)
			r = not r
		draw.rectangle([(0, 0), (65, 28)], outline="black", fill="black")
		for x in range(0, 6):
			for y in range(0, 5):
				draw.text((x*11+3, y*5+1), "*", fill="white")
		for x in range(0, 5):
			for y in range(0, 4):
				draw.text((x*11+9, y*5+3), "*", fill="white")

def stop():
	global stopNow
	stopNow = True
	sys.exit(0)

try:
	signal.signal(signal.SIGINT, stop)
	signal.signal(signal.SIGTERM, stop)
	signal.signal(signal.SIGABRT, stop);
	signal.signal(signal.SIGQUIT, stop);
	updateOled()
	#refreshTime()
	while True:
		if stopNow == True:
			break
		#refreshTime()
		#updateOled()
		time.sleep(1)
except:
	print("exception in main try block")
	pass



