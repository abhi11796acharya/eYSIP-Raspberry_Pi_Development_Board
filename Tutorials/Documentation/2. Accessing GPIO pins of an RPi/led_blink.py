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

# to use Raspberry Pi BCM pin 
GPIO.setmode(GPIO.BCM)

# setting the GPIO 19 as output(i.e IC pin 35) since we are using board in 'BOARD MODE'
# so refering the IC pin
GPIO.setup(19, GPIO.OUT)

# blink GPIO 19(i.e IC pin 35) 10 times
for i in range(0,10):
        blink(19) # call 

#to clean up all the ports used
GPIO.cleanup()
