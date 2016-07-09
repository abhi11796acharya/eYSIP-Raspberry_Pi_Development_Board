import threading
import time
import spidev


value = [0x08]
spi = spidev.SpiDev()
spi.open(0,0)
i = 0

# Function to read Serial data
# Function name :read
# Input : ser
# Output : read_value
# Example call: read(ser)

def Receive_data():
    while run_event.is_set():
        number = spi.readbytes(1)
        if (number !=):
            print (number)
            print "thread1"
        time.sleep(1)
    return

def Send_data():
    i=0;
    while run_event.is_set():
        #resp=spi.xfer2(value)
        #print resp
        print "thread2"
        time.sleep(1)
    return




if __name__ == "__main__":
    run_event = threading.Event()
    run_event.set()
    d1=1
    t1 = threading.Thread(target = Receive_data, args = ())

    d2 = 0.5
    t2 = threading.Thread(target = Send_data, args = ())

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
        
