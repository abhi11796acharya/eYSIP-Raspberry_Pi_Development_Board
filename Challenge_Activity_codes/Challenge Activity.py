import fipi as pi 
import time
import threading
pi.serial_open()  #Open serial port

# Function name :object_detect
# Input : Name,run_event
# Logic : This is a thread which is in a loop. When the value of proximity sensor
#         goes below the threshold value stop both the motors.
# Output : stops the motors.
# Example call: object_detected(name,run_event)
def object_detected(name,run_event):
    while run_event.is_set():
        Proximity_Sensor=ord(pi.adc_conversion(6))
        print Proximity_Sensor
        if (Proximity_Sensor<150):
            pi.stop()
    return

#MAIN FUNCTION:
if __name__ == "__main__":
    run_event = threading.Event()  
    run_event.set()       #set the threading event
    d1=1                        
    t1 = threading.Thread(target = object_detected, args = ("object_detected",run_event)) #descirbe the thread and then call it
    t1.start()   #start the thread

    try:
        while True:
            pi.forward()       # for forward motion of both the motors
            Proximity_Sensor=ord(pi.adc_conversion(6))    #read the value of IR proximity sensor
            if (Proximity_Sensor<150):   # if the proximity sensor value is less than threshold value
                pi.lcd_line1("object "+str(Proximity_Sensor)+"\n")  #sends string to LCD when object is detected 
                time.sleep(0.1)
                pi.buzzer_on()      # Turn the buzzer on
                time.sleep(3)       #wait for 3 seconds  
                pi.buzzer_off()     # turn the buzzer off 
                time.sleep(0.1)     
                pi.lcd_reset()      #reset the LCD
                time.sleep(0.1)
                break
        pi.serial_close()           #closse the serial port

    except KeyboardInterrupt:
        print "attempting to close threads. Max wait =",max(d1)
        pi.serial_close()
        run_event.clear()         # kill the thread
        t1.join()                 # waits for the thread to end
        

    
    



