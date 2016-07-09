import threading
import time
import serial
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.OUT)

ser=serial.Serial('/dev/ttyAMA0',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=3)

# Function to read Serial data
# Function name :read
# Input : ser
# Output : read_value
# Example call: read(ser)
def read(ser):
    read_value=""
    while True:
        ch=ser.read()         # reads the data 
        read_value+=ch        # appends the string in read_value
        if ch=='\r' or ch=='': 
            return read_value

def Serial_Data(name,run_event):
    while run_event.is_set():
        re_va=read(ser)
        ser.write("\r"+repr(re_va)) # writes the data received
        print (re_va)
    ser.write("\r\n Connection terminated:") # writes the data to serial terminal
    return

def main_program(name,delay,run_event):
    while run_event.is_set():
        led_on()
        time.sleep(delay)
        led_off()
        time.sleep(delay)
    return

def led_on():
    GPIO.output(13,True)
    return

def led_off():
    GPIO.output(13,False)
    return


if __name__ == "__main__":
    run_event = threading.Event()
    run_event.set()
    d1=1
    t1 = threading.Thread(target = Serial_Data, args = ("Serial_data",run_event))

    d2 = 0.5
    t2 = threading.Thread(target = main_program, args = ("Main",d2,run_event))

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
