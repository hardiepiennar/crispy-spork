import socket
import subprocess
import time
import EZLink_transmit as rfm

print("Connecting to NVS module...")
# Set port to binr mode
subprocess.call("nvsctl -v init", shell=True)

# Run nvs init script
subprocess.call("binrcmd -v init.cmd", shell=True)

# Start rtcm3 server
subprocess.call("rtkbase &", shell=True)

# Setting up the radio
rfm.setup()

print("Waiting for the server to start...")
time.sleep(5)


print("Sending RTCM data over radio...")
# Listen to rtcm3 socket and send data to radio
HOST = 'localhost'
PORT = 5800
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

try: 
    while True:
        data = s.recv(8)
	rfm.send_bytes(data)	
except KeyboardInterrupt:
    print("Closing connection to port")
    s.close()
    print("Shutting down radio and gps")
    rfm.close()
