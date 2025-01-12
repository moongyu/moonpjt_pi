import smbus
import math
import time

bms_addr = 0x70

def read_byte(addr, adr):
	return bus.read_byte_data(addr, adr)
	
def read_word(addr, adr):
	high = bus.read_byte_data(addr, adr)
	low = bus.read_byte_data(addr, adr+1)
	val = (high<<8) + low
	return val
	
def read_signed_16_2c(addr, adr):
		val = read_word(addr, adr)
		if(val >= 0x8000):
			return -((65535-val)+1)
		else:
			return val
	
bus = smbus.SMBus(1)

#get_data_00 = bus.read_word_data(bms_addr, 0x00)
#time.sleep(0.2)
#get_data_01 = bus.read_word_data(bms_addr, 0x01)
#time.sleep(0.2)
#get_data_00 = bus.read_byte_data(bms_addr, 0x52)
#get_data_00 = bus.write_byte_data(bms_addr, 0x00, 0x51)
get_data_00 = bus.write_byte(bms_addr, 0x00)
time.sleep(1)
get_data_01 = bus.read_byte_data(bms_addr, 0x51)

#print "get_data_00 = ", get_data_00
#print "get_data_01 = ", get_data_01
print("get_data_00 = ", get_data_00)
print("get_data_01 = ", get_data_01)


