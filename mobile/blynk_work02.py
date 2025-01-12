import blynklib
import blynktimer
import RPi.GPIO as GPIO 

#import time
#import threading

GPIO.setmode(GPIO.BCM)

# controller gpio init
GPIO_RIGHT = 6
GPIO_BACK = 13
GPIO_LEFT = 19
GPIO_FORW = 26

GPIO.setup(GPIO_RIGHT, GPIO.OUT)
GPIO.setup(GPIO_BACK, GPIO.OUT)
GPIO.setup(GPIO_LEFT, GPIO.OUT)
GPIO.setup(GPIO_FORW, GPIO.OUT)
		
#GPIO.output(GPIO_RIGHT, True)
#GPIO.output(GPIO_BACK, True)
#GPIO.output(GPIO_LEFT, True)
#GPIO.output(GPIO_FORW, True)

#GPIO.output(GPIO_RIGHT, True)
#GPIO.output(GPIO_BACK, True)
#GPIO.output(GPIO_LEFT, True)
#GPIO.output(GPIO_FORW, False)
	
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

def ctrl_weel(): 
	# if dir_lr is used reference, do not need declear global
	 
	if dir_fb == ff :
		GPIO.output(GPIO_RIGHT, True)
		GPIO.output(GPIO_BACK, True)
		GPIO.output(GPIO_LEFT, True)
		GPIO.output(GPIO_FORW, False)

	elif dir_fb  == bb :
		GPIO.output(GPIO_RIGHT, True)
		GPIO.output(GPIO_BACK, False)
		GPIO.output(GPIO_LEFT, True)
		GPIO.output(GPIO_FORW, True)

	elif dir_lr == rr :
		GPIO.output(GPIO_RIGHT, False)
		GPIO.output(GPIO_BACK, True)
		GPIO.output(GPIO_LEFT, True)
		GPIO.output(GPIO_FORW, True)

	elif dir_lr == ll :
		GPIO.output(GPIO_RIGHT, True)
		GPIO.output(GPIO_BACK, True)
		GPIO.output(GPIO_LEFT, False)
		GPIO.output(GPIO_FORW, True)
		
	elif dir_fb == fx :
		if dir_lr == rx:
			GPIO.output(GPIO_RIGHT, False)
			GPIO.output(GPIO_BACK, True)
			GPIO.output(GPIO_LEFT, True)
			GPIO.output(GPIO_FORW, False)
		elif dir_lr == lx :
			GPIO.output(GPIO_RIGHT, True)
			GPIO.output(GPIO_BACK, True)
			GPIO.output(GPIO_LEFT, False)
			GPIO.output(GPIO_FORW, False)
		else :
			GPIO.output(GPIO_RIGHT, True)
			GPIO.output(GPIO_BACK, True)
			GPIO.output(GPIO_LEFT, True)
			GPIO.output(GPIO_FORW, True)

	elif dir_fb == bx :
		if dir_lr == rx:
			GPIO.output(GPIO_RIGHT, False)
			GPIO.output(GPIO_BACK, False)
			GPIO.output(GPIO_LEFT, True)
			GPIO.output(GPIO_FORW, True)
		elif dir_lr == lx :
			GPIO.output(GPIO_RIGHT, True)
			GPIO.output(GPIO_BACK, False)
			GPIO.output(GPIO_LEFT, False)
			GPIO.output(GPIO_FORW, True)
		else :
			GPIO.output(GPIO_RIGHT, True)
			GPIO.output(GPIO_BACK, True)
			GPIO.output(GPIO_LEFT, True)
			GPIO.output(GPIO_FORW, True)
	else :
				GPIO.output(GPIO_RIGHT, True)
				GPIO.output(GPIO_BACK, True)
				GPIO.output(GPIO_LEFT, True)
				GPIO.output(GPIO_FORW, True)
				
# Add Timers
# timer : 설정해 둔 시간마다 실행됨
@timer.register(interval=1, run_once=True) # 최초 1회, 1초후 실행
def hello_world():
  print("Hello World!")


@timer.register(interval=1, run_once=False) # 1초마다 반복실행
def my_user_task():
	global dir_fb
	global dir_lr
	
	try:
		if(my_user_task.LED_flag):
			blynk.virtual_write(4, 255)   # Vpin =  V4, value = 255
			my_user_task.LED_flag = False
			#print("V4 LED ON")

			print("dir_fb", dir_fb)
			print("dir_lr", dir_lr)
      
		else:
			blynk.virtual_write(4, 0)     # Vpin =  V4, value = 0
			my_user_task.LED_flag = True
			#print("V4 LED OFF")

	# 최초 1회 변수 선언
	except AttributeError:
		my_user_task.LED_flag = True
		blynk.virtual_write(4, 255)
		#print("V4 LED ON")


# Start Blynk, Start timer
while True:
	blynk.run()
	timer.run()
	ctrl_weel()

	#aa = '140'
	#bb = int(aa)
	#cc = ['140']
	#dd = int(cc[0])
	#print("%s" %aa)
	#print("%d" %bb)
	#print("%d" %dd)
	
