"""
NVS device library for C.H.I.P device
H Pienaar Dec 2016
"""

import CHIP_IO.GPIO as GPIO
import time

#Pin defenitions
PIN_GPIO3 = "XIO-P4"
PIN_GPIO4 = "XIO-P5"
PIN_GPIO5 = "XIO-P7"
PIN_RST = "CSID1"
PIN_SLP = "CSID0"

print("Setting up NVS GPIO connections..."),
#Setup GPIO pins
GPIO.setup(PIN_GPIO3, GPIO.OUT)
GPIO.setup(PIN_GPIO4, GPIO.OUT)
GPIO.setup(PIN_GPIO5, GPIO.OUT)
GPIO.setup(PIN_RST, GPIO.OUT)
GPIO.setup(PIN_SLP, GPIO.IN)

#Initialize output pins
GPIO.output(PIN_GPIO3, GPIO.LOW)
GPIO.output(PIN_GPIO4, GPIO.HIGH)
GPIO.output(PIN_GPIO5, GPIO.HIGH)
GPIO.output(PIN_RST, GPIO.LOW)
print("[DONE]")

time.sleep(0.1)

print("Releasing NVS from reset..."),
GPIO.output(PIN_RST, GPIO.HIGH)
time.sleep(0.5)
print("[DONE]")

while True:
    time.sleep(1)
