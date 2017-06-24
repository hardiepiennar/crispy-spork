import os, pty
import serial.tools.list_ports
import subprocess

print("Checking if virtual serial port has been setup")
ports = os.listdir("/dev/pts/")

if len(ports) < 5:
	print("Setting up proxy serial port..."),
	subprocess.call("socat -d -d pty,raw,echo=0, pty,raw,echo=0 &", shell=True)
	print("Virtual port created")
else:
	print("Virtual ports already up and running")

