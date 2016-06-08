import smbus # module to access i2c based interfaces
import time

bus = smbus.SMBus(1) # Rev 2 Pi uses 1

DEVICE = 0x20 # Device address (A0-A2)
IODIRA = 0x00 # Pin direction register
OLATA  = 0x14 # Register for outputs
GPIOA  = 0x12 # Register for inputs


# all bits of IODIRA register are set to 0 meaning GPA pins are outputs
bus.write_byte_data(DEVICE,IODIRA,0x00)

# Set all 7 output bits of port A to 0
bus.write_byte_data(DEVICE,OLATA,0)

try:
 while True:
  input = bus.read_byte_data(DEVICE,GPIOA) #read status of GPIO register i.e. 
                                           #switch status
  if input & 0x80 == 0x80: # switch pressed i.e. input = True
    bus.write_byte_data(DEVICE,OLATA,1) # led glows 
    time.sleep(1)
 
  # Set all bits to zero
  bus.write_byte_data(DEVICE,OLATA,0)

except KeyboardInterrupt:
       pass
       bus.write_byte_data(DEVICE,OLATA,0) # in case of keyboard 
	                   # interrupt set port A pins to zero