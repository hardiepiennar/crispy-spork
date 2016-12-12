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

def print_current_mode():
    """Reads register 0x07 and prints out the current mode"""
    mode_reg = read_register(0x07)
    print("\n======Operating and Function Control======")

    print("Crystal Oscillator (xton): "),
    if mode_reg&0b00000001 > 0:
        print("\t[ON]")
    else:
        print("\t[OFF]")

    print("Phase Locked Loop (pllon): "),
    if mode_reg&0b00000010 > 0:
        print("\t[ON]")
    else:
        print("\t[OFF]")

    print("Receive Mode (rxon): "),
    if mode_reg&0b00000100 > 0:
        print("\t\t[ON]")
    else:
        print("\t\t[OFF]")

    print("Transmit Mode (txon): "),
    if mode_reg&0b00001000 > 0:
        print("\t\t[ON]")
    else:
        print("\t\t[OFF]")

    print("32 kHz Clock Source (32ksel): "),
    if mode_reg&0b00010000 > 0:
        print("\t[ON]")
    else:
        print("\t[OFF]")

    print("Watchdog Timer (enwt): "),
    if mode_reg&0b00100000 > 0:
        print("\t[Enabled]")
    else:
        print("\t[Disabled]")

    print("Low Battery Detect (enlbd): "),
    if mode_reg&0b01000000 > 0:
        print("\t[Enabled]")
    else:
        print("\t[Disabled]")

    mode_reg = read_register(0x08)
    print("Auto Transmit (autotx): "),
    if mode_reg&0b00001000 > 0:
        print("\t[Enabled]")
    else:
        print("\t[Disabled]")

    print("Multi-packet Receive (rxmpk): "),
    if mode_reg&0b00010000 > 0:
        print("\t[Enabled]")
    else:
        print("\t[Disabled]")

    print("Ant diversity mode (antdiv): "),
    print("\t["+str(mode_reg&0b11100000/32)+"]")

    print("==========================================\n")

def soft_reset():
    #TODO: use register 0x07 to reset by setting swres
    print("ERROR: soft_reset function not yet implemented")

def clear_tx_fifo():
    #TODO: use register 0x08 to clear tx fifo by setting ffclrtx 
    print("ERROR: clear_tx_fifo function not yet implemented")

def clear_rx_fifo():
    #TODO: use register 0x08 to clear rx fifo by setting ffclrrx 
    print("ERROR: clear_rx_fifo function not yet implemented")

def set_auto_tx(state):
    #TODO: use register 0x08 to turn on or off autotx 
    print("ERROR: set_auto_tx function not yet implemented")
    
setup()
print_current_mode()
close()
GPIO.cleanup()
