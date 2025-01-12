# Autor:	Ingmar Stapel
# Date:		20160207
# Version:	1.0
# Homepage:	www.custom-build-robots.com

import smbus
import time
import subprocess
import os

# set the SMBus device.
dev = smbus.SMBus(1)

os.system('clear')
 
print("---------------------------------------------------------")
print("Checking for connected i2c devices")
time.sleep(1)
print("The following devices are conntected:")
print("---------------------------------------------------------")
output = subprocess.check_output("i2cdetect -y 1", shell=True)
print(output)


# Address of the SRF08 ultrasonic sensor on the I2C bus (default 0X70)
print("---------------------------------------------------------")
print("Now change the address of the SRF08 ultrasonic sensor.")
print("---------------------------------------------------------")

try:
	addressOld = input("Please enter the old address (default 0x70):")
	addressNew = input("Please enter the new address (0x70 to 0x77):") 
except ValueError: 
	sys.exit()

print("---------------------------------------------------------")
print("Checking if the new address is in the range 0x70 to 0x77")
time.sleep(0.5)
print("Changing address...")
print("---------------------------------------------------------")

# The address needs to be changed into an integer value
addressOld = int(addressOld, 16)
addressNew = int(addressNew, 16)

# checking if the new address value is a valid address to protect the ultrasonic sensor.
# To de-activate the check delete the if clause.

if addressNew in range(111, 120):

	# the new address is changed by a left bitshift (e.g. 0x73 << 1 = 0xE6)
	# ID 0x70 defulat address is 'E0'
	addressNew = addressNew << 1

	# write_byte_data(addr,cmd,val) 	Write Byte Data transaction. 	int addr,char cmd,char val 
	dev.write_byte_data(addressOld, 0, 0xA0)
	time.sleep(0.065)
	dev.write_byte_data(addressOld, 0, 0xAA)
	time.sleep(0.065)
	dev.write_byte_data(addressOld, 0, 0xA5)
	time.sleep(0.065)
	dev.write_byte_data(addressOld, 0, addressNew)

	time.sleep(2)
	os.system('clear')
	print("---------------------------------------------------------")
	print("Checking for connected i2c devices")
	time.sleep(1)
	print("The following devices are conntected:")
	print("---------------------------------------------------------")
	output = subprocess.check_output("i2cdetect -y 1", shell=True)
	print(output)