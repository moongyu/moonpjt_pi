import time
import RPi.GPIO as GPIO
import threading

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 17
GPIO_ECHO = 27

print ("ultrasonic distance measurement")

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.output(GPIO_TRIGGER, False)

status = 0
stop = 0
start = 0
distance = 0

def ch1_trg():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

def ch1_rising(channel):
    global status
    global start
    status = 1
    start = time.time()
    
def ch1_falling(channel):
    global status
    global stop
    status = 0
    stop = time.time()
    
    elapsed = stop - start
        
    if(stop and start):
        distance = (elapsed*34000.0)/2
        print (channel)
        print ("distance : %.lf cm" % distance)
            
def ch1_both(channel):
    global status
    global start
    global distance
    
    if status == 0:
        status = 1
        start = time.time()
        
    elif status == 1:
        status = 0
        stop = time.time()
    
        elapsed = stop - start
            
        if(stop and start):
            distance = (elapsed*34000.0)/2
            print (channel)
            print ("distance : %.lf cm" % distance)
    

def timer_prid():
    global distance
    
    #distance = 1 # _test
    timer=threading.Timer(1,timer_prid)
    print ("distance : %.lf cm" % distance)
    
    if status == 0:
        ch1_trg()
    timer.start()
    

#GPIO.add_event_detect(GPIO_ECHO, GPIO.RISING, callback = ch1_rising)
#GPIO.add_event_detect(GPIO_ECHO, GPIO.FALLING, callback = ch1_falling)
GPIO.add_event_detect(GPIO_ECHO, GPIO.BOTH, callback = ch1_both)
timer_prid()

try:
    while True:
        #if status == 0:
        #    ch1_trg()
        pass

except KeyboardInterrupt:
    print ("ultrasonic distance measurement end")
    GPIO.cleanup()
    #.cancel()
    GPIO.remove_event_detect(GPIO_ECHO)
