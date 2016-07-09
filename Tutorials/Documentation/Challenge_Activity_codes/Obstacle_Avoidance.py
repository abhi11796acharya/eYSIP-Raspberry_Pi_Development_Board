import fipi as pi 
import time
import threading
thrld = 20
pi.serial_open()    # Open serial port

right_wl_sensor= (pi.adc_conversion(1))
center_wl_sensor= (pi.adc_conversion(2))
left_wl_sensor= (pi.adc_conversion(3))
def obstacle_detect(name,run_event):
    while run_event.is_set():
        if ((pi.adc_conversion(6)<140)):
            pi.lcd_line_1("object detected\n")
            pi.buzzer_on()
            time.sleep(1)
            pi.buzzer_off()
            time.sleep(0.1)
            pi.lcd_reset()
            time.sleep(0.1)
    return                   
            

def linefollow():
    while True:
        right_wl_sensor= (pi.adc_conversion(1))
        center_wl_sensor= (pi.adc_conversion(2))
        left_wl_sensor= (pi.adc_conversion(3))
        flag = 0

        if ((center_wl_sensor > thrld) and (right_wl_sensor < thrld)and(left_wl_sensor<thrld)):
            flag=1
            pi.velocity(230,230)
            time.sleep(0.1)
        if ((right_wl_sensor > thrld) and (flag==0) and (center_wl_sensor < thrld) and (left_wl_sensor<thrld) ):
                flag = 1
                pi.velocity(200,150)
        if ((center_wl_sensor < thrld) and (right_wl_sensor < thrld) and (flag==0) and (left_wl_sensor>thrld)):
            flag = 1
            pi.velocity(150,200)
        if ((center_wl_sensor > thrld) and (right_wl_sensor > thrld) and (flag==0) and (left_wl_sensor<thrld)):
            flag = 1
            pi.velocity(220,180)
        if ((center_wl_sensor > thrld) and (right_wl_sensor < thrld) and (flag==0) and (left_wl_sensor>thrld)):
            flag = 1
            pi.velocity(180,220)
        if (center_wl_sensor > thrld) and (left_wl_sensor > thrld) and (right_wl_sensor > thrld) :
            pi.lcd_line1("Node\n")
            time.sleep(1)
            pi.lcd_reset()
            break
    return

if __name__ == "__main__":
    
    run_event = threading.Event()
    run_event.set()
    d1=1
    t1 = threading.Thread(target = obstacle_detect, args = ("Obstacle",run_event))
    t1.start()
			
    try:
	while True:
		linefollow()
		if ((pi.adc_conversion(6)<140)):
			pi.stop()
			time.sleep(0.1)
			pi.right()
			while True:
                            right_wl_sensor= (pi.adc_conversion(1))
                            center_wl_sensor= (pi.adc_conversion(2))
			    if ((center_wl_sensor > thrld) & (right_wl_sensor < thrld)):
				    pi.stop()
				    time.sleep(0.1)
				    linefollow()
				    break
			i=0
			while(i<2):
			    pi.right()
			    time.sleep(0.1)
			    while True:
                                right_wl_sensor= (pi.adc_conversion(1))
                                center_wl_sensor= (pi.adc_conversion(2))
				    if ((center_wl_sensor > thrld) & (right_wl_sensor < thrld)):
					    pi.stop()
					    time.sleep(0.1)
					    break
                            linefollow()
                            i=i+1
			linefollow()
			pi.right()
			time.sleep(0.1)
			while True:
                            right_wl_sensor= (pi.adc_conversion(1))
                            center_wl_sensor= (pi.adc_conversion(2))
			    if ((center_wl_sensor > thrld) & (right_wl_sensor < thrld)):
				pi.stop()
				time.sleep(0.1)
				break
			linefollow()
			pi.left()
			time.sleep(0.1)
			while True:
                            right_wl_sensor= (pi.adc_conversion(1))
                            center_wl_sensor= (pi.adc_conversion(2))
			    if ((center_wl_sensor > thrld) & (right_wl_sensor < thrld)):
				pi.stop()
				time.sleep(0.1)
				break
			linefollow()
			break        
		
	pi.serial_close()   


    except KeyboardInterrupt:
	pi.serial_close()
	print "attempting to close threads. Max wait =",max(d1)
	run_event.clear()
	t1.join()

