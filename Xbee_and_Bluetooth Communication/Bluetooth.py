import serial
import time

#serial Driver Initialization
ser=serial.Serial('/dev/ttyUSB0',baudrate=9600,
                  parity=serial.PARITY_NONE,
                  stopbits=serial.STOPBITS_ONE,
                  bytesize=serial.EIGHTBITS,timeout=3)

# Function to read Serial data
# Function name :read
# Input : ser
# Output : read_value
# Example call: read(ser)
def read(ser):
    read_value=""
    while True:
        ch=ser.read()         # reads the data 
        read_value+=ch        # appends the string in read_value
        if ch=='\r' or ch=='': 
            return read_value
try:
    while True:
        ser.write("\r\nHi I am Raspbian Jessie:")
                               # writes the data to serial terminal
        re_va=read(ser)
        print("Received String :")
        ser.write("\r\n"+repr(re_va)) # writes the data received
        print (re_va)
except KeyboardInterrupt:
    pass
