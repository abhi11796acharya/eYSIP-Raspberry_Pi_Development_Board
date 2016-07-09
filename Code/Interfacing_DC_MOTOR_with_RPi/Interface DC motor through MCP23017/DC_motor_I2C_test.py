import smbus  # module to access i2c based interfaces
import time

bus = smbus.SMBus(1) # Rev 2 Pi uses 1

DEVICE = 0x20 # Device address (A0-A2)
IODIRB = 0x01 # Pin direction register
OLATB  = 0x15 # Register for outputs

# all bits of IODIRB register are set to 0 meaning GPA pins are outputs
bus.write_byte_data(DEVICE,IODIRB,0x00)

# Set all the pins of Port B of MCP23017 to 0 except pin 3
# pin 3 is set to logic 1 which is given to enable pin of L293D
bus.write_byte_data(DEVICE,OLATB,0x04)

# Function name :forward
# Input : None
# Output : Motor moves in clockwise direction i.e. forward
# Example call: forward() 
def forward():
     bus.write_byte_data(DEVICE,OLATB,0b00000101) # one input
                          #to the motor is set to logic high and the 
      # other input is set to logic low resulting in clockwise motion	 
     time.sleep(1)


# Function name :backward
# Input : None
# Output : Motor moves in anticlockwise direction i.e. backward
# Example call: backward() 	 
def backward():
     bus.write_byte_data(DEVICE,OLATB,0b00000110)# one input to the 
                               #motor is set to logic low and the 
     # other input is set to logic high resulting in anticlockwise motion
     time.sleep(1)
   

try:
    while 1:
         forward()    # motor moves in clockwise direction 
         time.sleep(2)
         bus.write_byte_data(DEVICE,OLATB,0b00000100)
                              # halt the motor for 1 second
         time.sleep(1)
         
         backward()    # motor moves in anticlockwise direction
         time.sleep(2)
         bus.write_byte_data(DEVICE,OLATB,0b00000100)
                                  # halt the motor for 1 second
         time.sleep(1)

except KeyboardInterrupt:
     pass
     bus.write_byte_data(DEVICE,OLATB,0b00000000)
     # Stop the motor by setting all pins to logic 0
     
