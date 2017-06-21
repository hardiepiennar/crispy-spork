"""
Main python script for ski course base station

Hardie Pienaar
Makespace Cambridge
June 2017
"""

import subprocess 
import time

import NVSLib as nvs
import EZLink_transmit as rfm
import serial


print("Removing getty service from ttyS0")
subprocess.call("systemctl mask serial-getty@ttyS0.service", shell=True)

print("Initialising gps")
nvs.setup()
print("Releasing serial from setup operation")
nvs.close_serial()

print("Opening serial port for receiving GPS data")
ser = serial.Serial("/dev/ttyS0", 115200, parity=serial.PARITY_ODD,timeout=None)
	
print("Initialising radio")
rfm.setup()

print("Sending UART data over radio")
try:
	while True:
		data = ser.read(8)
		rfm.send_bytes(data)	
except KeyboardInterrupt:
	print("Shutting down radio and gps")
	rfm.close()

