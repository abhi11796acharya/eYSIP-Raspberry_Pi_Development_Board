import fipi as pi 
import time
import threading
pi.serial_open()  

def object_detected(name,run_event):
    while run_event.is_set():
        Proximity_Sensor=ord(pi.adc_conversion(6))
        print Proximity_Sensor
        if (Proximity_Sensor<150):
            pi.stop()
    return

if __name__ == "__main__":
    run_event = threading.Event()
    run_event.set()
    d1=1
    t1 = threading.Thread(target = object_detected, args = ("object_detected",run_event))
    t1.start()

    try:
        while True:
            pi.forward()
            Proximity_Sensor=ord(pi.adc_conversion(6))
            #time.sleep(0.5)
            if (Proximity_Sensor<150):
                pi.lcd_line1("object "+str(Proximity_Sensor)+"\n")
                time.sleep(0.1)
                pi.buzzer_on()
                time.sleep(3)
                pi.buzzer_off()
                time.sleep(0.1)
                pi.lcd_reset()
                time.sleep(0.1)
                break
        pi.serial_close()

    except KeyboardInterrupt:
        print "attempting to close threads. Max wait =",max(d1)
        pi.serial_close()
        run_event.clear()
        t1.join()
        

    
    



