import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 17
GPIO_ECHO = 27

print ("ultrasonic distance measurement")

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.output(GPIO_TRIGGER, False)

status = 0
cnt = 0

def ch1_trg():
    global status
    
    status = 1
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(1)
    
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

def ch1_both(channel):
    global status
    global start
    global stop
    
    if status == 1:
        status = 2
        start = time.time()
        
    elif status == 2:
        status = 0
        stop = time.time()
    
        elapsed = stop - start
            
        if(stop and start):
            distance = (elapsed*34000.0)/2
            #print (channel)
            print ("distance : %.lf cm" % distance)
        else:
            print ("error")
            


#GPIO.add_event_detect(GPIO_ECHO, GPIO.RISING, callback = ch1_rising)
#GPIO.add_event_detect(GPIO_ECHO, GPIO.FALLING, callback = ch1_falling)
GPIO.add_event_detect(GPIO_ECHO, GPIO.BOTH, callback = ch1_both)


try:
    while True:
        if status == 0:
            ch1_trg()

        #else:
            #GPIO.output(GPIO_TRIGGER, False)
        
        #print (status)
        #pass

except KeyboardInterrupt:
    print ("ultrasonic distance measurement end")
    GPIO.cleanup()



