import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 17
GPIO_ECHO = 27
GPIO_TRIGGER_CH2 = 23
GPIO_ECHO_CH2 = 24

print ("ultrasonic distance measurement")

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_CH2, GPIO.OUT)
GPIO.setup(GPIO_ECHO_CH2, GPIO.IN)

try:
    while True:
        stop = 0
        start = 0
        GPIO.output(GPIO_TRIGGER, False)
        #time.sleep(1)
        time.sleep(0.5)
        
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        
        while GPIO.input(GPIO_ECHO) == 0:
            start = time.time()
            
        while GPIO.input(GPIO_ECHO) == 1:
            stop = time.time()
                
        elapsed = stop - start
        
        if(stop and start):
            distance = (elapsed*34000.0)/2
            
        stop = 0
        start = 0
        GPIO.output(GPIO_TRIGGER_CH2, False)
        time.sleep(0.5)
        
        GPIO.output(GPIO_TRIGGER_CH2, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER_CH2, False)
        
        while GPIO.input(GPIO_ECHO_CH2) == 0:
            start = time.time()
            
        while GPIO.input(GPIO_ECHO_CH2) == 1:
            stop = time.time()
                
        elapsed = stop - start
        
        if(stop and start):
            distance_ch2 = (elapsed*34000.0)/2    
            
            #print ("distance : %.lf cm" % distance)
            #print ("distance : %.lf cm" % distance_ch2)
            print ("d_ch1 : %.lf cm" % distance, "d_ch2 : %.lf cm" % distance_ch2)
            
except KeyboardInterrupt:
    print ("ultrasonic distance measurement end")
    GPIO.cleanup()
    
#GPIO.cleanup()
