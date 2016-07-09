import threading
import smbus
import time

bus = smbus.SMBus(1)

address = 0x04

# Function to read Serial data
# Function name :read
# Input : ser
# Output : read_value
# Example call: read(ser)

def Serial_Data(name,run_event):
    while run_event.is_set():
        number = bus.read_byte(address)
        if (number != 0):
            print (number)
        time.sleep(2)
    bus.write_byte(address,0)
    return

def main_program(name,run_event):
    i=0;
    while run_event.is_set():
        
        bus.write_byte(address,i);
        print ("RPI: Hi Arduino, I sent you", i)
        i = i + 1
        time.sleep(1)
    return




if __name__ == "__main__":
    run_event = threading.Event()
    run_event.set()
    d1=1
    t1 = threading.Thread(target = Serial_Data, args = ("Serial_data,run_event))

    d2 = 0.5
    t2 = threading.Thread(target = main_program, args = ("Main",run_event))

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
        
