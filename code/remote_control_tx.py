"""
Main python script for ski course base station remote control testing

Hardie Pienaar
Makespace Cambridge
June 2017
"""


import os
import subprocess 
import time
import numpy as np

import EZLink_transmit as rfm
	
print("Sending user commands over radio")
try:
	while True:
            key=raw_input("Direction?")
	    rfm.send_bytes(key)	
except KeyboardInterrupt:
	print("Shutting down radio")
	rfm.close()

