import smbus
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

# i2c sensor init
bus = smbus.SMBus(1)
addr = 0x70
addr2 = 0x73

def write(addr_val, value):
    bus.write_byte_data(addr_val, 0, value)
    return -1

def lightlevel(addr_val):
    light = bus.read_byte_data(addr_val,1)
    return light
    
def range(addr_val):
    range1 = bus.read_byte_data(addr_val, 2)
    range2 = bus.read_byte_data(addr_val, 3)
    range3 = (range1 << 8) + range2
    return range3


try:
    while True:
        stop = 0
        start = 0
        GPIO.output(GPIO_TRIGGER, False)
        #time.sleep(1)
        time.sleep(0.01)
        
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
        time.sleep(0.01)
        
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
            #print ("d_ch1 : %.lf cm" % distance, "d_ch2 : %.lf cm" % distance_ch2)
            

        # i2c sensor data gather
        write(addr, 0x51)
        time.sleep(0.2)
        lightlvl = lightlevel(addr)
        rng = range(addr)
        #print(lightlvl)
        #print(rng)

        write(addr2, 0x51)
        time.sleep(0.2)
        lightlvl2 = lightlevel(addr2)
        rng2 = range(addr2)

        print ("d_ch1: %.lf cm" % distance, "d_ch2: %.lf cm" % distance_ch2, "d_ch3: %.lf cm" % rng, "d_ch4: %.lf cm" % rng2)
        print ("lig_ch1: %.lf" % lightlvl, "lig_ch2: %.lf" % lightlvl2)
        #time.sleep(0.2)

except KeyboardInterrupt:
    print ("ultrasonic distance measurement end")
    GPIO.cleanup()
    
#GPIO.cleanup()
