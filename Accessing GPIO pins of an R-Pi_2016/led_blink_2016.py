import RPi.GPIO as GPIO # module to control Pi GPIO channels
import time 

# Function name :blink()
# Input : Pin number 
# Output : Alternating high and low logic levels on the pin
# Example call: blink(pin)
def blink(pin): 
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(1) # to see the blinking effect clearly
		      # we give a delay 
        GPIO.output(pin,GPIO.LOW)
        time.sleep(1)
        return 

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# set up GPIO output channel i.e. on pin 12 
GPIO.setup(35, GPIO.OUT)

# blink GPIO18 10 times
for i in range(0,10):
        blink(35) # call 

#to clean up all the ports used
GPIO.cleanup()
