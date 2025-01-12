####################################
# 190730 mobile robot /w blynk
# remote control by blynk app

# 190814 auto shutdown

# 190818 /w distance measure by ultrasonic sensor
#        /change forward, backward, left, right range fix
####################################
import blynklib
import blynktimer
import RPi.GPIO as GPIO
from subprocess import call
import smbus
import time
import threading

#import time
#import threading

GPIO.setmode(GPIO.BCM)

# controller gpio init
GPIO_RIGHT = 6
GPIO_BACK = 13
GPIO_LEFT = 19
GPIO_FORW = 26

GPIO_BATLOW = 12
GPIO_LED = 16

GPIO.setup(GPIO_RIGHT, GPIO.OUT)
GPIO.output(GPIO_RIGHT, True)
GPIO.setup(GPIO_BACK, GPIO.OUT)
GPIO.output(GPIO_BACK, True)
GPIO.setup(GPIO_LEFT, GPIO.OUT)
GPIO.output(GPIO_LEFT, True)
GPIO.setup(GPIO_FORW, GPIO.OUT)
GPIO.output(GPIO_FORW, True)

GPIO.setup(GPIO_BATLOW, GPIO.IN)

GPIO.setup(GPIO_LED, GPIO.OUT)
GPIO.output(GPIO_LED, False)

#GPIO.output(GPIO_RIGHT, True)
#GPIO.output(GPIO_BACK, True)
#GPIO.output(GPIO_LEFT, True)
#GPIO.output(GPIO_FORW, True)

# sensor gpio init
GPIO_TRIGGER = 17
GPIO_ECHO = 27
GPIO_TRIGGER_CH2 = 23
GPIO_ECHO_CH2 = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_CH2, GPIO.OUT)
GPIO.setup(GPIO_ECHO_CH2, GPIO.IN)

###########################
# i2c sensor init
bus = smbus.SMBus(1)
addr = 0x70
addr2 = 0x73
###########################

init = 0
ll = 1
rr = 2
ff = 3
bb = 4
lx = 5
rx = 6
fx = 7
bx = 8
dir_result = init

dir_lr = 0
dir_fb = 0
	
v5_value = 0
v6_value = 0

ctrl_enable = 0

forward = 12
forward_right = 1
right = 3
backward_right = 4
backward = 6
backward_left = 7
left = 9
forward_left = 10

distance = 0
distance_ch2 = 0
rng = 0
rng2 = 0

block_cnt = 0
detect_block = 0 

get_cmd_cnt = 0
motor_lock = 0
cmd_cnt_temp1 = 0
cnt_motor_dis = 0

exit_th = 1
####################################

#이메일로 받은 토큰을 여기에 추가
BLYNK_AUTH = 'l06y5RhVosdY8ZQi7gYiVcDFl6jaThIh'
# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = blynktimer.Timer()

WRITE_EVENT_PRINT_MSG = "[EVENT] Pin: V{} Val: '{}'"
READ_PRINT_MSG = "[EVENT] Pin: V{}"

# Register Virtual Pins
# blynk앱에서 버튼 누를경우 동작 - write (Virtual Pins 1)
@blynk.handle_event('write V5')
def write_virtual_pin_handler(pin, value):
	global dir_lr
	global v5_value
	global get_cmd_cnt
	
	# 'value' is string in array, not decimal value
	v5_value = int(value[0])
	
	if v5_value == 0 :
		dir_lr = ll
		get_cmd_cnt = get_cmd_cnt + 1
	elif v5_value > 0 and v5_value <= 118:
		dir_lr = lx
		get_cmd_cnt = get_cmd_cnt + 1
	elif v5_value == 255:
		dir_lr = rr
		get_cmd_cnt = get_cmd_cnt + 1
	elif v5_value >= 138 and v5_value < 255:
		dir_lr = rx
		get_cmd_cnt = get_cmd_cnt + 1
	else :
		dir_lr = init
		
	#print(dir_lr)
	#print("%s" %value)
	#print("%d" %v5_value)
	print(WRITE_EVENT_PRINT_MSG.format(pin,value))

@blynk.handle_event('write V6')
def write_virtual_pin_handler(pin, value):
	global dir_fb
	global v6_value
	global get_cmd_cnt
	
	v6_value = int(value[0])
	
	if v6_value == 0 :
		dir_fb = bb
		get_cmd_cnt = get_cmd_cnt + 1
	elif v6_value > 0 and v6_value <= 118 :
		dir_fb = bx
		get_cmd_cnt = get_cmd_cnt + 1
	elif v6_value == 255 :
		dir_fb = ff
		get_cmd_cnt = get_cmd_cnt + 1
	elif v6_value >= 138 and v6_value < 255 :
		dir_fb = fx
		get_cmd_cnt = get_cmd_cnt + 1
	else :
		dir_fb = init

	print(WRITE_EVENT_PRINT_MSG.format(pin,value))

@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
	global ctrl_enable
	
	print(WRITE_EVENT_PRINT_MSG.format(pin,value))

	if(value == ['1']) :
		ctrl_enable = 1
	else :
		ctrl_enable = 0

@blynk.handle_event('read V3')
def read_virtual_pin_handler(pin):
    global distance
    global distance_ch2
    global rng
    global rng2
    
    msg = str(dir_result)
    blynk.virtual_write(3, msg)
    blynk.virtual_write(7,distance)
    blynk.virtual_write(8,rng)
    blynk.virtual_write(9,rng2)

#@blynk.handle_event('read V7')
#def read_virtual_pin_handler(pin):
#    msg = str(msg)
#    blynk.virtual_write(7,msg)

##########################################################
def ctrl_weel(): 
	global dir_result
	# if dir_lr is used reference, do not need declear global
	# global need only when writing in function
	 
	if dir_fb == ff :
		dir_result = forward
		GPIO.output(GPIO_RIGHT, True)
		GPIO.output(GPIO_BACK, True)
		GPIO.output(GPIO_LEFT, True)
		GPIO.output(GPIO_FORW, False)

	elif dir_fb  == bb :
		dir_result = backward
		GPIO.output(GPIO_RIGHT, True)
		GPIO.output(GPIO_BACK, False)
		GPIO.output(GPIO_LEFT, True)
		GPIO.output(GPIO_FORW, True)

	elif dir_lr == rr :
		dir_result = right
		GPIO.output(GPIO_RIGHT, False)
		GPIO.output(GPIO_BACK, True)
		GPIO.output(GPIO_LEFT, True)
		GPIO.output(GPIO_FORW, True)

	elif dir_lr == ll :
		dir_result = left
		GPIO.output(GPIO_RIGHT, True)
		GPIO.output(GPIO_BACK, True)
		GPIO.output(GPIO_LEFT, False)
		GPIO.output(GPIO_FORW, True)
		
	elif dir_fb == fx :
		if dir_lr == rx:
			# caution. direction
			# this is control of switch, simply
			dir_result = forward_right
			GPIO.output(GPIO_RIGHT, False)
			GPIO.output(GPIO_BACK, True)
			GPIO.output(GPIO_LEFT, True)
			GPIO.output(GPIO_FORW, False)
		elif dir_lr == lx :
			dir_result = forward_left
			GPIO.output(GPIO_RIGHT, True)
			GPIO.output(GPIO_BACK, True)
			GPIO.output(GPIO_LEFT, False)
			GPIO.output(GPIO_FORW, False)
		else :
			dir_result = init
			GPIO.output(GPIO_RIGHT, True)
			GPIO.output(GPIO_BACK, True)
			GPIO.output(GPIO_LEFT, True)
			GPIO.output(GPIO_FORW, True)

	elif dir_fb == bx :
		if dir_lr == rx:
			dir_result = backward_right
			GPIO.output(GPIO_RIGHT, False)
			GPIO.output(GPIO_BACK, False)
			GPIO.output(GPIO_LEFT, True)
			GPIO.output(GPIO_FORW, True)
		elif dir_lr == lx :
			dir_result = backward_left
			GPIO.output(GPIO_RIGHT, True)
			GPIO.output(GPIO_BACK, False)
			GPIO.output(GPIO_LEFT, False)
			GPIO.output(GPIO_FORW, True)
		else :
			dir_result = init
			GPIO.output(GPIO_RIGHT, True)
			GPIO.output(GPIO_BACK, True)
			GPIO.output(GPIO_LEFT, True)
			GPIO.output(GPIO_FORW, True)
	else :
		dir_result = init
		GPIO.output(GPIO_RIGHT, True)
		GPIO.output(GPIO_BACK, True)
		GPIO.output(GPIO_LEFT, True)
		GPIO.output(GPIO_FORW, True)
				
# Add Timers
# timer : 설정해 둔 시간마다 실행됨
@timer.register(interval=1, run_once=True) # 최초 1회, 1초후 실행
def hello_world():
  print("Ready System")


@timer.register(interval=1, run_once=False) # 1초마다 반복실행
def my_user_task():
	global dir_fb
	global dir_lr
	
	try:
		if(my_user_task.LED_flag):
			blynk.virtual_write(4, 255)   # Vpin =  V4, value = 255
			my_user_task.LED_flag = False
			
			GPIO.output(GPIO_LED, True)

			#debug
			#print("dir_fb", dir_fb)
			#print("dir_lr", dir_lr)
      
		else:
			blynk.virtual_write(4, 0)     # Vpin =  V4, value = 0
			my_user_task.LED_flag = True
			
			GPIO.output(GPIO_LED, False)

	# 최초 1회 변수 선언
	except AttributeError:
		my_user_task.LED_flag = True
		blynk.virtual_write(4, 255)

batlowcnt = 0
def detect_lowvoltage_task() :
	global batlowcnt
	batlow_f = GPIO.input(GPIO_BATLOW)
	
	if batlow_f == 1 :
		batlowcnt = batlowcnt + 1
		if batlowcnt >= 3 :
			call(['shutdown', '-h', 'now'], shell=False)
	else :
		batlowcnt = 0

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

def run_ultra_sensor_trigger() :
    global distance
    global distance_ch2
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
            
        if start >= (time_init+0.036):
            error_ch = 1
            print ("ch1_errB")
            break

    #print ("ch1_after")
    if error_ch == 0 :
        while GPIO.input(GPIO_ECHO) == 1:
            stop = time.time()
                
        elapsed = stop - start
        
        if(stop and start):
            distance = (elapsed*34000.0)/2
            #print ("1: %d" % distance) #_debug
        
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
        if start >= (time_init+0.036):
            error_ch = 1
            print ("ch2_errB")
            break

    #print ("ch2_after")
    if error_ch == 0 :
        while GPIO.input(GPIO_ECHO_CH2) == 1:
            stop = time.time()
                
        elapsed = stop - start
        
        if(stop and start):
            distance_ch2 = (elapsed*34000.0)/2
                
                
def run_ultra_sensor() :
	global rng
	global rng2
# i2c sensor data gather
	write(addr, 0x51)
	time.sleep(0.1)
	#lightlvl = lightlevel(addr)
	rng = range(addr)

	write(addr2, 0x51)
	time.sleep(0.1)
	#lightlvl2 = lightlevel(addr2)
	rng2 = range(addr2)

def deinit_motor():
    GPIO.output(GPIO_RIGHT, True)
    GPIO.output(GPIO_BACK, True)
    GPIO.output(GPIO_LEFT, True)
    GPIO.output(GPIO_FORW, True)

# need to reset motor button in blynk
def start_timer():
    global get_cmd_cnt
    global motor_lock
    global cmd_cnt_temp1
    global cnt_motor_dis
    global exit_th
    
    #cmd_cnt_temp1 = 0
    #cnt_motor_dis = 0
    if exit_th == 1 :
        timer=threading.Timer(1,start_timer)
        timer.start()

        cmd_cnt_temp2 = cmd_cnt_temp1
        cmd_cnt_temp1 = get_cmd_cnt
        
        if get_cmd_cnt == cmd_cnt_temp2 :
            
            cnt_motor_dis = cnt_motor_dis + 1
            if cnt_motor_dis >= 3 :
                motor_lock = 1
                get_cmd_cnt = 0
                cmd_cnt_temp1 = 0
                print("m_lock") # _debug
        else :
            cnt_motor_dis = 0
            motor_lock = 0
        
def start_timer_sensor():
    # threading for reduing delay time 
    global exit_th
    
    if exit_th == 1 :
        timer_run_sensor = threading.Timer(1,start_timer_sensor)
        timer_run_sensor.start()

        run_ultra_sensor_trigger()
        run_ultra_sensor()
        
# Main Function
##########################################################
#timer.deamon = True
start_timer()

#timer_run_sensor.deamon = True
start_timer_sensor()

# Start Blynk, Start timer
##########################################################
try:
    
    while True:
            blynk.run()
            timer.run()

            # _debug
            #print ("1: %d" % distance, "2: %d" % distance_ch2)
            #print ("3: %d" % rng, "4: %d" % rng2)
            
            detect_lowvoltage_task()
            
            if ctrl_enable == 0 :
                deinit_motor()
            elif motor_lock == 1 :
                deinit_motor()
            else :
                ctrl_weel()
               
            #debug
            #aa = '140'
            #bb = int(aa)
            #cc = ['140']
            #dd = int(cc[0])
            #print("%s" %aa)
            #print("%d" %bb)
            #print("%d" %dd)

except KeyboardInterrupt:
    global exit_th
    
    deinit_motor()
    GPIO.cleanup()
    
    exit_th = 0



