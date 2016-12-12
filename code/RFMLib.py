"""
RFM device library for C.H.I.P device
H Pienaar Dec 2016
"""

import CHIP_IO.GPIO as GPIO
import spiBitBang as spi
import time

#Pin definitions
PIN_RX_ANT = "XIO-P4"
PIN_TX_ANT = "XIO-P5"
PIN_SDN = "XIO-P6"
PIN_NSEL = "XIO-P3"

def setup():
    print("Setting up RFM22B GPIO connections..."),
    #Setup GPIO pins
    GPIO.setup(PIN_RX_ANT, GPIO.OUT)
    GPIO.setup(PIN_TX_ANT, GPIO.OUT)
    GPIO.setup(PIN_SDN, GPIO.OUT)
    GPIO.setup(PIN_NSEL, GPIO.OUT)

    #Initialize output pins
    GPIO.output(PIN_RX_ANT, GPIO.LOW)
    GPIO.output(PIN_TX_ANT, GPIO.LOW)
    GPIO.output(PIN_SDN, GPIO.HIGH)
    GPIO.output(PIN_NSEL, GPIO.HIGH)
    print("[DONE]")

    #Turn on RFM chip
    print("Turning on RFM22B..."),
    GPIO.output(PIN_SDN, GPIO.LOW)
    time.sleep(0.5)
    print("[DONE]")

    #Initialize bitbang spi library
    spi.setup()

def read_register(addr):
    GPIO.output(PIN_NSEL, GPIO.LOW)
    time.sleep(0.001)
    read = spi.xfer2([addr,0x00])[1]
    time.sleep(0.001)
    GPIO.output(PIN_NSEL, GPIO.HIGH)
    time.sleep(0.1)
    return read 

def write_register(addr, byte):
    GPIO.output(PIN_NSEL, GPIO.LOW)
    time.sleep(0.001)
    spi.xfer2([addr&0b10000000,byte])
    time.sleep(0.001)
    GPIO.output(PIN_NSEL, GPIO.HIGH)
    time.sleep(0.1)

def close():
    print("Turning off RFM22B..."),
    GPIO.output(PIN_SDN, GPIO.HIGH)
    print("[DONE]")

setup()
print(read_register(0x00))
print(read_register(0x01))
print(read_register(0x02))
close()
GPIO.cleanup()
