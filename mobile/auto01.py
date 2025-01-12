import smbus
import time
import RPi.GPIO as GPIO
import random
import threading

GPIO.setmode(GPIO.BCM)
1
# controller gpio init
GPIO_RIGHT = 6
GPIO_BACK = 13
GPIO_LEFT = 19
GPIO_FORW = 26

GPIO.setup(GPIO_RIGHT, GPIO.OUT)
GPIO.setup(GPIO_BACK, GPIO.OUT)
GPIO.setup(GPIO_LEFT, GPIO.OUT)
GPIO.setup(GPIO_FORW, GPIO.OUT)

GPIO.output(GPIO_RIGHT, True)
GPIO.output(GPIO_BACK, True)
GPIO.output(GPIO_LEFT, True)
GPIO.output(GPIO_FORW, True)

# sensor gpio init
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
#==============================================
limit_dist_long = 40
limit_dist_short = 35
#==============================================
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

def start_timer():
    global dir
    timer=threading.Timer(10,start_timer)
    dir = random.randint(1,3)
    timer.start()
    return dir

def deinit_motor():
    GPIO.output(GPIO_RIGHT, True)
    GPIO.output(GPIO_BACK, True)
    GPIO.output(GPIO_LEFT, True)
    GPIO.output(GPIO_FORW, True)

#==============================================

start_timer()

time.sleep(3)

try:
    distance = 0
    distance_ch2 = 0
    while True:

        # 1. gathering distance
        stop = 0
        start = 0
        GPIO.output(GPIO_TRIGGER, False)
        time.sleep(0.01)
        
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        
        error_ch = 0
        timeout_f = 0
        #print ("ch1_before")
        while GPIO.input(GPIO_ECHO) == 0:
            start = time.time()
            
            if timeout_f == 0:
                timeout_f = 1
                time_init = start
                
            if time_init >= (start+0.5):
                error_ch = 1
                print ("ch1_error_detect")
                break

        #print ("ch1_after")
        if error_ch == 0 :
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
        
        error_ch = 0
        timeout_f = 0
        #print ("ch2_before")
        while GPIO.input(GPIO_ECHO_CH2) == 0:
            start = time.time()

            if timeout_f == 0:
                timeout_f = 1
                time_init = start
            if time_init >= (start+0.036):
                error_ch = 1
                print ("ch2_error_detect")
                break

        #print ("ch2_after")
        if error_ch == 0 :
            while GPIO.input(GPIO_ECHO_CH2) == 1:
                stop = time.time()
                    
            elapsed = stop - start
            
            if(stop and start):
                distance_ch2 = (elapsed*34000.0)/2    

        # i2c sensor data gather
        write(addr, 0x51)
        time.sleep(0.1)
        lightlvl = lightlevel(addr)
        rng = range(addr)

        write(addr2, 0x51)
        time.sleep(0.1)
        lightlvl2 = lightlevel(addr2)
        rng2 = range(addr2)

        #print ("d_ch1: %.lf cm" % distance, "d_ch2: %.lf cm" % distance_ch2, "d_ch3: %.lf cm" % rng, "d_ch4: %.lf cm" % rng2)
        #print ("lig_ch1: %.lf" % lightlvl, "lig_ch2: %.lf" % lightlvl2)

        # 2. gathering direction by random fun