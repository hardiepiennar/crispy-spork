"""
RFM device library for C.H.I.P device
H Pienaar Dec 2016
"""

import CHIP_IO.GPIO as GPIO
import spiBitBang as spi

#Pin defenitions
PIN_RX_ANT = "XIO-P4"
PIN_TX_ANT = "XIO-P5"
PIN_SDN = "XIO-P6"

print("Setting up RFM22B GPIO connections..."),
#Setup GPIO pins
GPIO.setup(PIN_RX_ANT, GPIO.OUT)
GPIO.setup(PIN_TX_ANT, GPIO.OUT)
GPIO.setup(PIN_SDN, GPIO.OUT)

#Initialize output pins
GPIO.output(PIN_RX_ANT, GPIO.LOW)
GPIO.output(PIN_TX_ANT, GPIO.LOW)
GPIO.output(PIN_SDN, GPIO.LOW)
print("[DONE]")

spi.setup()
print(spi.xfer2([10,20]))
spi.close()
