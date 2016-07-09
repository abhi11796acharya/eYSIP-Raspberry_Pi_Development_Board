import Adafruit_PCA9685
import smbus
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD) # to use Raspberry Pi board pin numbers
GPIO.setup(11,GPIO.OUT)  # to set board pin 11 as output
GPIO.setup(13,GPIO.OUT)  # to set board pin 13 as output
GPIO.setwarnings(False)
pwm = Adafruit_PCA9685.PCA9685()  

pwm.set_pwm_freq(60)   # set the frequency of pwm to 60Hz

# Function name :forward
# Input : None
# Logic : give pin 11 logic 1 connected to IN1 of L293D
#         and give pin 13 logic 0 connected to IN2 of L293D
#         to rotate the motor in clockwise direction.   
# Output : Motor moves in clockwise direction i.e.,forward
# Example call: forward() 
def forward():   # for clockwise motion of motor 
    GPIO.output(11,True) 
    GPIO.output(13,False)
    return

# Function name :backward
# Input : None
# Logic : give pin 11 logic 0 connected to IN1 of L293D
#         and give pin 13 logic 1 connected to IN2 of L293D
#         to rotate the motor in anticlockwise direction.   
# Output : Motor moves in anticlockwise direction i.e.,backward
# Example call: backward()
def backward():  #for anticlockwise motion of motor
    GPIO.output(11,False)
    GPIO.output(13,True)
    return

try:
    while True:
        forward()
        for value in range (0,4095,409):
            pwm.set_pwm(0, 0, value) #motor rotates in forward direction 
            time.sleep(2)            #with increasing speed
        for value in range (0,4095,409):
            pwm.set_pwm(0, 0 ,4095-value)#motor rotates in backward direction
            time.sleep(2)              # with decreasing speed   

        backward()
        for value in range (0,4095,409):
            pwm.set_pwm(0,0,value)   #motor rotates in backward direction 
            time.sleep(2)           #with increasing speed
        for value in range (0,4095,409):
            pwm.set_pwm(0,0,4095-value)   #motor rotates in backward direction 
            time.sleep(2)            # with decreasing speed 
except KeyboardInterrupt:
    pass
GPIO.cleanup()    # clears GPIO pins which stalls the motor
        
        
    

