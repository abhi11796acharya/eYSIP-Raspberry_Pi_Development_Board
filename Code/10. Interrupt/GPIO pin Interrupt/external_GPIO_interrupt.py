# Switch - pin 11 and GND
# LED1 - pin 12
# LED2 - pin13
import time
import thread  # to create thread
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)  # set Rpi in board mode
GPIO.setup(11,GPIO.IN,GPIO.PUD_UP)  # set pin 11 as input and internal pull up
                                    # is set high
GPIO.setup(12,GPIO.OUT) # set pin 12 as output
GPIO.setup(13,GPIO.OUT) # set pin 13 as output

# Function name :switch_pressed
# Input : None
# Output : Turn on led for 5 second and then turn it off.
# Example call: switch_pressed()
def switch_pressed():
        print 'Switch pressed'
        GPIO.output(12,True)
        time.sleep(5)
        GPIO.output(12,False)
        return

GPIO.add_event_detect(11,GPIO.FALLING,callback=switch_pressed,bouncetime=300)
                                        # Continuously check status of pin 11
try:
    while 1:
        GPIO.output(13,True) # turn on led connected to pin 13
        time.sleep(0.5)      #0.5 second delay
        GPIO.output(13,False) # turn off led 
        time.sleep(0.5)
    
except KeyboardInterrupt:
    pass
GPIO.cleanup()           # cleanup GPIO values on GPIO pins


