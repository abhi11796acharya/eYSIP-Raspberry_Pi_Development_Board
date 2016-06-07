import spidev
# module to control spi devices
import time
import math
import sys
# Open SPI bus
spi = spidev.SpiDev () # to create spi object
spi.open(0 ,0) #Clock polarity , Clock Phase
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0−7
# Function name : ReadChannel
# Input : channel
# Output : data
# Example call : Readadc( channel )
def readadc(adcnum):
# read SPI data from MCP3008 chip , 8 possible adc ’s (0 thru 7)
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi . xfer2 ([1 , 8 + adcnum << 4 , 0])
    adcout = (( r [1] & 3) << 8) + r [2]
    return adcout
# Function to calculate temperature from
# LM35 data , rounded to specified
# number of decimal places .
def ConvertTemp(data,places):
    temp = data*100
    temp = round(temp,places)
    return temp
try:
    while True:
        value = readadc(0)
        volts = ( value * 3.3) / 1024
        temperature = ConvertTemp( volts ,2)
        #Print out results
        print("Temp : {} volts: {} deg C: {}".format( value,volts,temperature ))
        time . sleep (0.5)
except KeyboardInterrupt:
    pass
spi.close()
sys.exit(0)
    
