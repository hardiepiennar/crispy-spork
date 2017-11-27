"""
EZLink application note for transmitting data

Hardie Pienaar 
Feb 2017
"""

import RFMLib as rfm
import time
import numpy as np

def setup():
	"""Setup the library and turn on ism chip"""
	rfm.setup()
	"""Read the interrupt status1 register"""
	ItStatus1 = rfm.read_register(0x03)
	ItStatus2 = rfm.read_register(0x04)

	"""Set RF Parameters"""
	# Set the center frequency to 915MHz
	rfm.write_register(0x75, 0x75) # Write 0x75 to the Frequency Band Select register
	rfm.write_register(0x76, 0xBB) # Write 0xBB to the Nominal Carrier Frequency1 register
	rfm.write_register(0x77, 0x80) # Write 0x80 to the Nominal Carrier Frequency0 register
	# Set the desired TX data rate (9.6kbps)
	rfm.write_register(0x6E, 0x4E) # Write 0x4E to the TXDataRate 1 register
	rfm.write_register(0x6F, 0xA5) # Write 0xA5 to the TXDataRate 0 register
	rfm.write_register(0x70, 0x2C) # Write 0x2C to the Modulation Mode Control 1 register
	# Set the desired TX deviation (+=45kHz)
	rfm.write_register(0x72, 0x48) # Write 0x48 to the Frequency Deviation Register

	"""Set Packet Configuration"""
	# Set packet structure and modulation type
	rfm.write_register(0x34, 0x09) # Write 0x09 to the Preamble length register
	# Disable header bytes; set variable packet length (the length of the packet is defined by the
	# received packet length field of the packet); set the synch word to two bytes long
	rfm.write_register(0x33, 0x02) # Write 0x02 to the Header Control 2 register
	# Set the sync word pattern to 0x2DD4
	rfm.write_register(0x36, 0x2D) # Write 0x2D to the Sync Word 3 register
	rfm.write_register(0x37, 0xD4) # Write 0xD4 to the Sync Word 2 register
	# Enable the TX packet handler and CRC-16 (IBM) check
	rfm.write_register(0x30, 0x0D) # Write 0x0D to the Data Access Control register
	# Enable FIFO mode and GFSK modulation
	rfm.write_register(0x71, 0x63) # Write 0x63 to the Modulation Mode Control 2 Register 

	"""Select modulation"""
	# Set VCO and PLL
	rfm.write_register(0x54, 0x7F) # Write 0x7F to the VCO Current Trimming register
	rfm.write_register(0x59, 0x40) # Write 0x40 to the Divider Current Trimming register

def send_bytes(msg):
	"""Set the contents of the packet"""
	# Set the length of the payload to 8 bytes 
	rfm.write_register(0x3E, len(msg))
	# Fill the payload into the transmit FIFO
	for i in np.arange(len(msg)):
		rfm.write_register(0x7F, ord(msg[i]))

	"""Disable all interrupts and enable the packet sent interrupt only"""
	# This will be used for indicating the successful packet transmission for the CHIP
	rfm.write_register(0x05, 0x04) # Write 0x04 to the interrupt enable 1 register
	rfm.write_register(0x06, 0x00) # Write 0x03 to the Interrute enable 2 register
	# Read interrupt status registers to clear pending interrupts making nIRQ pin go back to high
	ItStatus1 = rfm.read_register(0x03) # Read the Interrupt Status 1 register
	ItStatus2 = rfm.read_register(0x04) # Read the Interrupt Status 2 register

	"""Enable Transmitter"""
	# The radio forms the packet and sends it automatically
	rfm.write_register(0x07, 0x09) # Write 0x09 to the Operating Function Control 1 register

	"""Wait for the packet sent interrupt"""
	# CHIP only needs to monitor the ipksent interrupt
	while rfm.check_irq():
		time.sleep(0.001)
	# Read interrupt status registers to release the interrupt flags
	ItStatus1 = rfm.read_register(0x03) # Read the Interrupt Status 1 register
	ItStatus2 = rfm.read_register(0x04) # Read the Interrupt Status 2 register

def close():
	"""Cleanup GPIO and turn off the chip"""
	rfm.close()

