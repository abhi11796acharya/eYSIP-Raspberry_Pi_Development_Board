# LED connnected to GPA0
# Push button to GPA4
import smbus # module to access i2c based interfaces
import time

#define I2C connections
bus = smbus.SMBus(1)
DEVICE = 0x20 # 0x20 is address of slave MCP23017 IC on bus.
              #Using this address bus communicates with MCP23017 IC Device
              #This address in set by setting the A0,A1,A2 pins of IC to GND.
IODIRA = 0x00 
OLATA  = 0x14 
GPIOA  = 0x12 


# all bits of IODIRA register are set to 0 meaning GPA pins are outputs
bus.write_byte_data(DEVICE,IODIRA,0x00)

# Set all 7 output bits of port A to 0
rw = bus.read_byte_data(DEVICE,GPIOA) & 0x00;
bus.write_byte_data(DEVICE,OLATA,rw)

try:
 while True:
  input = bus.read_byte_data(DEVICE,GPIOA) #read status of GPIO register i.e. 
                                           #switch status
  if input & 0x80 == 0x80:                 # switch pressed i.e. input = True
      rw = bus.read_byte_data(DEVICE,GPIOA) & 0x01
      bus.write_byte_data(DEVICE,OLATA,rw) 
      time.sleep(1)
      # Set all bits to zero
      bus.write_byte_data(DEVICE,OLATA,0)

except KeyboardInterrupt:
       pass
       bus.write_byte_data(DEVICE,OLATA,0) # in case of keyboard 
                                           # interrupt set port A pins to zero
