import smbus
import time

# ch1: 0x70, ch2: 0x73
# check method : i2cdetect -y 1
bus = smbus.SMBus(1)
addr = 0x73

def write(value):
    bus.write_byte_data(addr, 0, value)
    return -1

def lightlevel():
    light = bus.read_byte_data(addr,1)
    return light
    
def range():
    range1 = bus.read_byte_data(addr, 2)
    range2 = bus.read_byte_data(addr, 3)
    range3 = (range1 << 8) + range2
    return range3
    
write(0x51)
time.sleep(0.7)
lightlvl = lightlevel()
rng = range()
print(lightlvl)
print(rng)
