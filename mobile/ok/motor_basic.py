import RPi.GPIO as GPIO 

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

GPIO.output(GPIO_RIGHT, True)
GPIO.output(GPIO_BACK, True)
GPIO.output(GPIO_LEFT, True)
GPIO.output(GPIO_FORW, False)

# left wheel more speed up, f+r dir
#GPIO.output(GPIO_RIGHT, False)
#GPIO.output(GPIO_BACK, True)
#GPIO.output(GPIO_LEFT, True)
#GPIO.output(GPIO_FORW, False)

# right wheel more speed up, f+l dir
#GPIO.output(GPIO_RIGHT, True)
#GPIO.output(GPIO_BACK, True)
#GPIO.output(GPIO_LEFT, False)
#GPIO.output(GPIO_FORW, False)

# right wheel more speed up, b+l dir
#GPIO.output(GPIO_RIGHT, True)
#GPIO.output(GPIO_BACK, False)
#GPIO.output(GPIO_LEFT, False)
#GPIO.output(GPIO_FORW, True)

# left wheel more speed up, b+r dir
#GPIO.output(GPIO_RIGHT, False)
#GPIO.output(GPIO_BACK, False)
#GPIO.output(GPIO_LEFT, True)
#GPIO.output(GPIO_FORW, True)
