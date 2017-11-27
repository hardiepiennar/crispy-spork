"""
Main python script for ski course base station

Hardie Pienaar
Makespace Cambridge
June 2017
"""


import os
import subprocess 
import time
import numpy as np

import NVSLib as nvs
import EZLink_transmit as rfm
import serial
import serial.tools.list_ports


#print("Removing getty service from ttyS0")
#subprocess.call("systemctl mask serial-getty@ttyS0.service", shell=True)

#print("Initialising gps")
#nvs.setup()
#print("Releasing serial from setup operation")
#nvs.close_serial()

print("Creating virtual port for rtcm3 data")
print("Killing any other socat process")
ports = os.listdir("/dev/pts/")
if len(ports) > 3:
        subprocess.call("pkill socat &", shell=True)
time.sleep(1)
old_ports = os.listdir("/dev/pts/")
subprocess.call("socat -d -d pty,raw,echo=0, pty,raw,echo=0 &", shell=True)
time.sleep(1)
print("Virtual port created")
new_ports = os.listdir("/dev/pts/")
for i in np.arange(len(old_ports)):
        new_ports.remove(old_ports[i])

#print("Starting up str2str server for rtcm3 generation")
#subprocess.call("./str2str -in \"serial://ttyS0:115200:8:O:1#nvs\" -out \"serial://pts/1:9600:8:N:1#rtcm3\" -msg \"1002,1004,1006,1013,1019\"&", shell=True)

print("Opening serial port for receiving rtcm3 data")
ser = serial.Serial("/dev/pts/2", 9600, parity=serial.PARITY_NONE,timeout=None)
	
#print("Initialising radio")
rfm.setup()


print("Sending UART data over radio")
try:
	while True:
		data = ser.read(8)
		rfm.send_bytes(data)	
except KeyboardInterrupt:
	print("Shutting down radio and gps")
	rfm.close()

