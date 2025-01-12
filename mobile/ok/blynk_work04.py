####################################
# 190730 mobile robot /w blynk
# remote control by blynk app

# 190814 auto shutdown
####################################
import blynklib
import blynktimer
import RPi.GPIO as GPIO
from subprocess import call

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

init = 0
ll = 1
rr = 2
ff = 3
bb = 4
lx = 5
rx = 6
fx = 7
bx = 8

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

####################################

#이메일로 받은 토큰을 여기에 추가
BLYNK_AUTH = 'l06y5RhVosdY8ZQi7gYiVcDFl6jaThIh'
# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = blynktimer.Timer()

WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"

# Register Virtual Pins
# blynk앱에서 버튼 누를경우 동작 - write (Virtual Pins 1)
@blynk.handle_event('write V5')
def write_virtual_pin_handler(pin, value):
	global dir_lr
	global v5_value
	
	# 'value' is string in array, not decimal value
	v5_value = int(value[0])
	
	if v5_value >= 0 and v5_value <= 10 :
		dir_lr = ll
	elif v5_value > 10 and v5_value <= 118:
		dir_lr = lx
	elif v5_value >= 245 and v5_value <= 255:
		dir_lr = rr
	elif v5_value >= 138 and v5_value < 245:
		dir_lr = rx
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
	
	v6_value = int(value[0])
	
	if v6_value >= 0 and v6_value <= 10 :
		dir_fb = bb
	elif v6_value > 10 and v6_value <= 118 :
		dir_fb = bx
	elif v6_value >= 245 and v6_value <= 255 :
		dir_fb = ff
	elif v6_value >= 138 and v6_value < 245 :
		dir_fb = fx
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
	msg = str(dir_result)
	blynk.virtual_write(3, msg)

        
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
	
# Start Blynk, Start timer
####################################
while True:
	blynk.run()
	timer.run()
	detect_lowvoltage_task()

	# ctrl_enable have to activate to enable motor
	if ctrl_enable == 1 :
		ctrl_weel()
	else :
		GPIO.output(GPIO_RIGHT, True)
		GPIO.output(GPIO_BACK, True)
		GPIO.output(GPIO_LEFT, True)
		GPIO.output(GPIO_FORW, True)

	#debug
	#aa = '140'
	#bb = int(aa)
	#cc = ['140']
	#dd = int(cc[0])
	#print("%s" %aa)
	#print("%d" %bb)
	#print("%d" %dd)
	
