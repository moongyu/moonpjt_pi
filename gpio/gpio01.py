import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO_06_RIGHT = 6
GPIO_13_BACK = 13
GPIO_19_LEFT = 19
GPIO_26_FORW = 26

GPIO.setup(GPIO_06_RIGHT, GPIO.OUT)
GPIO.setup(GPIO_13_BACK, GPIO.OUT)
GPIO.setup(GPIO_19_LEFT, GPIO.OUT)
GPIO.setup(GPIO_26_FORW, GPIO.OUT)

GPIO.output(GPIO_06_RIGHT, True)
#GPIO.output(GPIO_06_RIGHT, False)
GPIO.output(GPIO_13_BACK, True)
#GPIO.output(GPIO_13_BACK, False)
GPIO.output(GPIO_19_LEFT, True)
#GPIO.output(GPIO_19_LEFT, False)
GPIO.output(GPIO_26_FORW, True)
#GPIO.output(GPIO_26_FORW, False)

#except KeyboardInterrupt:
#    GPIO.cleanup()