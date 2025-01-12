import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 17
GPIO_ECHO = 27

print ("ultrasonic distance measurement")

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

try:
    while True:
        stop = 0
        start = 0
        GPIO.output(GPIO_TRIGGER, False)
        time.sleep(1)
        
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
            print (elapsed)
            print ("distance : %.lf cm" % distance)
            
except KeyboardInterrupt:
    print ("ultrasonic distance measurement end")
    GPIO.cleanup()
    
#GPIO.cleanup()