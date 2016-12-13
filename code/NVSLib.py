"""
NVS device library for C.H.I.P device
H Pienaar Dec 2016
"""

import CHIP_IO.GPIO as GPIO
import time
import serial
import numpy as np

#Pin defenitions
PIN_GPIO3 = "XIO-P4"
PIN_GPIO4 = "XIO-P5"
PIN_GPIO5 = "XIO-P7"
PIN_RST = "CSID1"
PIN_SLP = "CSID0"
SERIAL_PORT = "/dev/ttyS0"

def soft_reset():
    ser.write(bytearray([0x10,0x01,0x00,0x01,0x21,0x01,0x00,0x00,0x10,0x03]))

print("Setting up NVS GPIO connections..."),
#Setup GPIO pins
GPIO.setup(PIN_GPIO3, GPIO.OUT)
GPIO.setup(PIN_GPIO4, GPIO.OUT)
GPIO.setup(PIN_GPIO5, GPIO.OUT)
GPIO.setup(PIN_RST, GPIO.OUT)
GPIO.setup(PIN_SLP, GPIO.IN)

#Initialize output pins
GPIO.output(PIN_GPIO3, GPIO.LOW)
GPIO.output(PIN_GPIO4, GPIO.LOW)
GPIO.output(PIN_GPIO5, GPIO.LOW)
GPIO.output(PIN_RST, GPIO.LOW)

#Initialize uart port
ser = serial.Serial(SERIAL_PORT, 115200, parity=serial.PARITY_ODD,timeout=None)
print("[DONE]")

time.sleep(0.1)

print("Releasing NVS from reset..."),
GPIO.output(PIN_RST, GPIO.HIGH)
time.sleep(0.5)
print("[DONE]")

print("Sending NVS port commands..."),
#ser.write(bytearray([0x10,0x0B,0x00,0x00,0xC2,0x01,0x00,0x04,0x10,0x03])) #Turn on BINR
#ser.write(bytearray([0x10,0x0B,0x00,0x00,0xC2,0x01,0x00,0x01,0x10,0x03])) #Turn off protocol 
#ser.write(bytearray([0x10,0x0B,0x01,0xC0,0x12,0x00,0x00,0x03,0x10,0x03])) #Turn on RTCM 4800 Port A 
#ser.write(bytearray([0x10,0x0B,0x01,0xC0,0x12,0x00,0x00,0x02,0x10,0x03])) #Turn on NMEA 4800 Port A 
#time.sleep(5)
#ser.write(bytearray([0x10,0x0B,0x01,0x00,0xC2,0x01,0x00,0x02,0x10,0x03])) #Turn on NMEA 115200 Port A 
#ser.write(bytearray([0x10,0x26,0x10,0x03])) #Check communication 
#ser.write("$PORST,F*20\r\n")
print("[DONE]")
#soft_reset()

while True:
    print(str(ser.read())),

GPIO.cleanup()
ser.close()
print("Exiting")
