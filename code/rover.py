import socket
import subprocess
import time
import EZLink_receive as rfm

print("Connecting to NVS module...")
# Set port to binr mode
subprocess.call("nvsctl -v init", shell=True)

# Run nvs init script
subprocess.call("binrcmd -v init.cmd", shell=True)


# Setting up the radio
rfm.setup()

print("Creating server for radio rtcm3 stream")
HOST = ''
PORT = 5800
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

try: 
    print("Waiting for listeners...")
    conn, addr = s.accept()  
    print("Connected by"+str(addr))
    while True:
	data = rfm.receive_bytes()	
        if len(data) > 0:
            conn.sendall(bytes(data))
except KeyboardInterrupt:
    print("Closing socket server")
    conn.close()
    s.close()
    print("Shutting down radio and gps")
    rfm.close()
