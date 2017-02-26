"""
SPI bit bang for C.H.I.P device
H Pienaar Dec 2016
"""

import CHIP_IO.GPIO as GPIO
import numpy as np
import time

#Pin defenitions
PIN_SDI = "XIO-P0"
PIN_SDO = "XIO-P1"
PIN_SCK = "XIO-P2"

def setup():
    """Setup GPIO ports"""
    print("Setting up SPI GPIO connections..."),
    #Setup GPIO pins
    GPIO.setup(PIN_SDI, GPIO.OUT)
    GPIO.setup(PIN_SDO, GPIO.IN)
    GPIO.setup(PIN_SCK, GPIO.OUT)

    #Initialize output pins
    GPIO.output(PIN_SDI, GPIO.LOW)
    GPIO.output(PIN_SCK, GPIO.LOW)
    print("[DONE]")

def close():
    GPIO.cleanup()

def xfer2(byte_list):
    """Transfer a list of bytes and store the returned values"""
    stored_bytes = []
    for byte in byte_list:
        temp_byte = byte
        store_byte = 0x00
        for i in np.arange(8):
            store_byte *= 2

            if temp_byte & 0b10000000 > 0:
                GPIO.output(PIN_SDI, GPIO.HIGH)
            else:
                GPIO.output(PIN_SDI, GPIO.LOW)
            temp_byte*=2
                
            #time.sleep(0.001)
            GPIO.output(PIN_SCK, GPIO.HIGH)
            #time.sleep(0.001)
            if GPIO.input(PIN_SDO):
                store_byte += 1
            GPIO.output(PIN_SCK, GPIO.LOW)

        GPIO.output(PIN_SDI, GPIO.LOW)
        stored_bytes.append(store_byte)

    return stored_bytes
