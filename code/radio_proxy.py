"""
This program creates a virtual serial port and forwards the data from the RFM22B radio to the 
created serial port.

Hardie Pienaar
Makespace Cambridge
June 2017
"""

import os
import subprocess
import serial
import serial.tools.list_ports
import EZLink_receive as rfm

# Setting up the virtual serial port 
print("Checking if virtual serial port has been setup")
ports = os.listdir("/dev/pts/")

if len(ports) < 5:
	print("Setting up proxy serial port..."),
	subprocess.call("socat -d -d pty,raw,echo=0, pty,raw,echo=0 &", shell=True)
	print("Virtual port created")
else:
	print("Virtual ports already up and running")

# Open virtual port
print("Opening virtual port")
ser = serial.Serial("/dev/pts/2",115200,parity=serial.PARITY_ODD,timeout=None)

# Create RFM22B receive link object
print("Setting up RFM22B")
rfm.setup()

# Start forwarding loop
print("Creating endless posting loop")
#while True:
#	rfm.receive_bytes()
ser.close()
rfm.close()
