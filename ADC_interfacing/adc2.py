import os
import spidev # module to control spi devices
import time
import RPi .GPIO as GPIO # module to control Pi GPIO channels

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
	data = ((adc[1]&3) << 8)
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
def Sharp_GP2D12_estimation(adc_reading):
       distance =(10.00*(2799.6*(1.00/(pow(adc_reading,1.1546)))))
       distanceInt = distance
       if distanceInt>800:
       distanceInt=800
       return distanceInt

# Define sensor channels
sharp_channel =0
white_channel =1

# Define delay between readings
delay =0.5

try:
while True:
      GPIO.setmode(GPIO.BOARD)# set up GPIO output channel
      GPIO.setup(24, GPIO.OUT)# set up CE0 Pin
      GPIO.setup(26, GPIO.OUT)# set up CE1 Pin

      GPIO.output(24,GPIO.LOW)# Enable CE0 Pin
      GPIO.output(26,GPIO.HIGH)# Disable CE1 Pin


      # Read the sharp sensor data
      sharp_level = ReadChannel(sharp_channel)	
      sharp_volts = ConvertVolts(sharp_level,3)
      value = Sharp_GP2D12_estimation(sharp_level)

      GPIO.output(26,GPIO.LOW)# Enable CE1 Pin
      GPIO.output(24,GPIO.HIGH)# Disable CE0 Pin

      # Read the white line sensor data
      white_level=ReadChannel(white_channel)
      white_volts = ConvertVolts(white_level,3)

      # Print out results
      print "--------------------------------------------"
      print("sharp: D{} (A{}V)".format(sharp_level,sharp_volts))
      print("sharp: (Distance {} cm)".format(value))

      print "--------------------------------------------"
      print("white: D{} (A{}V)".format(white_level,white_volts))

      # Wait before repeating loop
      time.sleep(delay)
      except KeyboardInterrupt:
pass