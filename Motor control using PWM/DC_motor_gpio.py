import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD) #set the RPi mode as Board mode 
GPIO.setup(11,GPIO.OUT)  #set pin 11 as output
GPIO.setup(13,GPIO.OUT)  #set pin 13 as output
GPIO.setup(12,GPIO.OUT)  #set pin 12 as output
GPIO.setwarnings(False)
en=GPIO.PWM(12,50) #set pin 12 as PWM pin

en.start(0) # start PWM cycles

# Function name :forward
# Input : None
# Logic : give pin 11 logic 1 connected to IN1 of L293D
#         and give pin 13 logic 0 connected to IN2 of L293D
#         to rotate the motor in clockwise direction.   
# Output : Motor moves in clockwise direction i.e.,forward
# Example call: forward() 
def forward():
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
def backward():
    GPIO.outpur(11,False)
    GPIO.output(13,True)
    return

try:
    while True:
        forward()
        for i in range (100):
            en.ChangeDutyCycle(i) # speed of motor goes on increasing
                                 #in clockwise direction 
            time.sleep(0.02)
        for i in range(100):
            en.ChangeDutyCycle(100-i) # speed of motor goes on decreasing 
            time.sleep(0.02)

        en.ChangeDutyCycle(0)

        backward()        
        for i in range (100):
            en.ChangeDutyCycle(i) # speed of motor goes on increasing
                                 #in anticlockwise direction.
            time.sleep(0.02)
        for i in range(100):
            en.ChangeDutyCycle(100-i) # speed of motor goes on decreasing
            time.sleep(0.02)

        en.ChangeDutyCycle(0)

except KeyboardInterrupt:
    pass
GPIO.cleanup()
en.stop()
        
