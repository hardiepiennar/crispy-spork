"""
NVS device library for C.H.I.P device
H Pienaar Dec 2016
"""

import RPi.GPIO as GPIO
import time
import serial
import numpy as np

#Pin defenitions
#PIN_RST = "CSID1"
#PIN_SLP = "CSID0"
#PIN_ANT = "CSID2"
PIN_RST = 18
PIN_SLP = 23 
PIN_ANT = 17 
SERIAL_PORT = "/dev/ttyS0"

ser = None

def soft_reset_no_erase():
    ser.write(bytearray([0x10,0x01,0x00,0x01,0x21,0x01,0x00,0x01,0x10,0x03]))

def check_ant():
    if GPIO.input(PIN_ANT):
        return True
    else:
        return False

def set_porta_nmea():
	#Turn on NMEA on Port A at 4800 baud
	ser.write(bytearray([0x10,0x0B,0x01,0xC0,0x12,0x00,0x00,0x02,0x10,0x03])) 
def set_porta_rtcm():
	#Turn on RTCM on Port A at 4800 baud
	ser.write(bytearray([0x10,0x0B,0x01,0xC0,0x12,0x00,0x00,0x03,0x10,0x03])) 
def set_porta_binr():
	#Turn on BINR on Port A at 115200 baud
	ser.write(bytearray([0x10,0x0B,0x01,0x00,0xC2,0x01,0x00,0x04,0x10,0x03])) 
def req_raw():
	#Request raw data at 5Hz
	ser.write(bytearray([0x10,0xF4,0x32,0x10,0x03])) 
def set_nav_rate():
	#Set the navigation rate
	ser.write(bytearray([0x10,0xD7,0x02,0x02,0x10,0x03])) 
def req_pvt():
	#request pvt vector
	ser.write(bytearray([0x10,0x27,0x01,0x10,0x03])) 
def set_smooth_range():
	#Set smooth range
	ser.write(bytearray([0x10,0xD7,0x03,0x78,0x10,0x03])) 
def init():
	print("Initialising GPS...")

	print("Warm start reboot")
	soft_reset_no_erase()
	time.sleep(0.2)

	print("Setting navgation rate to 2 Hz")
	ser.write(bytearray([0x10,0xD7,0x02,0x02,0x10,0x03])) 
	time.sleep(0.2)

	print("Differential correction SBAS w RTCA troposphere model")
	ser.write(bytearray([0x10,0xD7,0x08,0x02,0x02,0x10,0x03]))
	time.sleep(1)

	print("Setting raw data output to 2 Hz")
	ser.write(bytearray([0x10,0xF4,0x14,0x10,0x03])) 
	time.sleep(0.2)

	print("Setting bit information transmitted by satellites")
	ser.write(bytearray([0x10,0xD5,0x01,0x10,0x03])) 
	time.sleep(0.2)

	#print("Rebooting")
	#soft_reset_no_erase()
	#time.sleep(0.2)

def check_communication():
	#Sends check communication package and reads reply
	print("Sending Check Communication Packet")
	ser.write(bytearray([0x10,0x26,0x10,0x03])) 
	msg = ser.read(4) 
	print(len(msg))

def setup():
	global ser

	print("Setting up NVS GPIO connections..."),
	#Setup GPIO pins
	#GPIO.setup(PIN_GPIO3, GPIO.OUT)
	#GPIO.setup(PIN_GPIO4, GPIO.OUT)
	#GPIO.setup(PIN_GPIO5, GPIO.OUT)
	GPIO.setup(PIN_RST, GPIO.OUT)
	GPIO.setup(PIN_SLP, GPIO.IN)
	GPIO.setup(PIN_ANT, GPIO.IN)

	#Initialize output pins
	#GPIO.output(PIN_GPIO3, GPIO.LOW)
	#GPIO.output(PIN_GPIO4, GPIO.LOW)
	#GPIO.output(PIN_GPIO5, GPIO.LOW)
	GPIO.output(PIN_RST, GPIO.LOW)

	#Initialize uart port
	ser = serial.Serial(SERIAL_PORT, 115200, parity=serial.PARITY_ODD,timeout=None)
	#ser = serial.Serial(SERIAL_PORT, 115200, parity=serial.PARITY_NONE,timeout=None)
	print("[DONE]")

	time.sleep(0.1)

	print("Releasing NVS from reset..."),
	GPIO.output(PIN_RST, GPIO.HIGH)
	time.sleep(0.5)
	print("[DONE]")

	soft_reset_no_erase()
	time.sleep(0.5)

	print("Sending NVS port init commands...")
	init()
	print("[DONE]")

def close_serial():
	ser.close()

def close():
	global ser
	GPIO.cleanup()

#last_byte = 0
#while True:
#	packet = ser.read()
#    	print(packet.encode('hex')),
#	if packet.encode('hex') == "03" and last_byte.encode('hex') == "10":
#		print("")	
#	last_byte = packet

#print("Exiting")
