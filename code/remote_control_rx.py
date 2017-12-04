import time
import EZLink_receive as rfm

# Setting up the radio
rfm.setup()

try: 
    while True:
	data = rfm.receive_bytes()	
        print(data)
except KeyboardInterrupt:
    print("Shutting down radio")
    rfm.close()
