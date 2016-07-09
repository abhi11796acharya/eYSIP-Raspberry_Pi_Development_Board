import threading        
import RPi.GPIO as GPIO   
import time

GPIO.setmode(GPIO.BOARD)            #Set RPi in Board Mode
GPIO.setup(11,GPIO.IN,GPIO.PUD_UP)  #Set a Pull up resistor for pin 11
GPIO.setup(12,GPIO.OUT)             #Set pin 12 as output
GPIO.setup(13,GPIO.OUT)             #Set pin 13 as output

# Function to 
# Channel must be an integer 0-7
# Function name :ReadChannel
# Input : channel
# Output : data
# Example call: ReadChannel(channel)
def main_prog(name, delay, run_event):
    while run_event.is_set():
        led2_on()
        time.sleep(delay)
        led2_off()
        time.sleep(delay)
    
def switch_interrupt(name, delay, run_event):
    while run_event.is_set():
        input_state = GPIO.input(11)
        if input_state == False:
            print(name)
            led1_on()
            time.sleep(delay)
            led1_off()
        else:
            led1_off()

def led1_on():
    GPIO.output(12,True)
    return
def led1_off():
    GPIO.output(12,False)
    return
def led2_on():
    GPIO.output(13,True)
    return
def led2_off():
    GPIO.output(13,False)
    return


if __name__ == "__main__":
    run_event = threading.Event()
    run_event.set()
    d1 = 1
    t1 = threading.Thread(target = switch_interrupt, args = ("Switch Pressed",d1,run_event))

    d2 = 5
    t2 = threading.Thread(target = main_prog, args = ("Main Program Execution",d2,run_event))

    t1.start()
    time.sleep(.5)
    t2.start()

    try:
        while 1:
            time.sleep(.1)
    except KeyboardInterrupt:
        print "attempting to close threads. Max wait =",max(d1,d2)
        run_event.clear()
        t1.join()
        t2.join()
        print "threads successfully closed"
        GPIO.cleanup()
