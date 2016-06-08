import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD) #set the RPi mode as Board mode 
GPIO.setup(11,GPIO.OUT)  #set pin 11 as output
GPIO.setup(13,GPIO.OUT)  #set pin 13 as output
GPIO.setwarnings(False)
p= GPIO.PWM(11,50) #set pin 11 as software PWM
q= GPIO.PWM(13,50) #set pin 13 as software PWM

p.start(0) 
q.start(0)

try:
    while True:
        for i in range (100):
            p.ChangeDutyCycle(i) # speed of motor goes on increasing
                                 #in clockwise direction 
            time.sleep(0.02)
        for i in range(100):
            p.ChangeDutyCycle(100-i) # speed of motor goes on decreasing 
            time.sleep(0.02)

        p.ChangeDutyCycle(0)

        for i in range (100):
            q.ChangeDutyCycle(i) # speed of motor goes on increasing
                                 #in anticlockwise direction.
            time.sleep(0.02)
        for i in range(100):
            q.ChangeDutyCycle(100-i) # speed of motor goes on decreasing
            time.sleep(0.02)

        q.ChangeDutyCycle(0)

except KeyboardInterrupt:
    pass
GPIO.cleanup()
p.stop()
q.stop()
        
