import RPi.GPIO as GPIO # module to control Pi GPIO channels
import time
# to use Raspberry Pi board pin numbers
#GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # the input pin(12) is 
# normally pulled up to 3.3V therefore when we press the button a logic 
# low or false value is returned at this pin
GPIO.setup(35,GPIO.OUT)
i=0  # flag is set to zero
while True:      #  COntinuous loop
    if GPIO.input(12)==False:
        if i==0:
            GPIO.output(35,GPIO.HIGH)
            if GPIO.input(12)==False:
                i=1
                time.sleep(0.5)
    if GPIO.input(12)==False:
        if i==1:
            GPIO.output(35,GPIO.LOW)
            if GPIO.input(12)==False:
                i=0
                time.sleep(0.5)
        
        

            
