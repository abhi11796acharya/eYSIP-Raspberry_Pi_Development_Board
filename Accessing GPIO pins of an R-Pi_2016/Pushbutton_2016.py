import RPi.GPIO as GPIO # module to control Pi GPIO channels
import time

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # the input pin(12) is 
# normally pulled up to 3.3V therefore when we press the button a logic 
# low or false value is returned at this pin

while True:
    input_state = GPIO.input(23) # a variable to measure the 
				# logic state of the input pin
    if input_state == False:
        print('Button Pressed')
        time.sleep(0.2) # this is the min debouncing delay that 
			# we give in order to ensure that the 
			# switch is definitely pressed
