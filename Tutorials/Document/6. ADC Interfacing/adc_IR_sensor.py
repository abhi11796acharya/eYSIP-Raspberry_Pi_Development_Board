import os
import spidev # module to control spi devices
import time

# Open SPI bus
spi = spidev.SpiDev()# to create spi object
spi.open(0,0)#Clock polarity,Clock Phase

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
# Function name :ReadChannel
# Input : channel
# Output : data
# Example call: ReadChannel(channel)
def ReadChannel(channel):
	#Performs SPI Transaction and CS will be held active
	adc = spi.xfer2([1,(8+channel)<<4,0])	
	data1 = ((adc[2]& 0xFC) >> 2)
	data = ((adc[1]&3) << 6) + data1
        
	return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
# Function name :ConvertVolts
# Input : data,places
# Output : volts
# Example call: ConvertVolts(data,places)
def ConvertVolts(data,places):
	volts = (data * 3.3) / float(1023)
	volts = round(volts,places)
	return volts

# This Function calculates the actual distance in millimeters(mm)
# from the input 
# Function name :Sharp_GP2D12_estimation
# Input : adc_reading
# Output : distanceInt
# Example call: Sharp_GP2D12_estimation(adc_reading)
def Shar_sensor_estimation(adc_reading):
       distance =(10.00*(2799.6*(1.00/(pow(adc_reading,1.1546)))))
       distanceInt = distance
       if distanceInt>800:
               distanceInt=800
       return distanceInt

# Define sensor channels
sharp_channel =0

# Define delay between readings
delay =0.5

try:
        while True:
                # Read the sharp sensor data
                sharp_level = ReadChannel(sharp_channel)
                sharp_volts = ConvertVolts(sharp_level,3)
                value = Sharp_GP2D12_estimation(sharp_level)
                # Print out results
                print "--------------------------------------------"
                print("sharp: Digital {} (Analog {}V)".format(sharp_level,
                                                sharp_volts))
                print("sharp: (Distance {} mm)".format(value))
                # Wait before repeating loop
                time.sleep(delay)
except KeyboardInterrupt:
        pass
