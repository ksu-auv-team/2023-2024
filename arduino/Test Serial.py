# Libraries 
import serial 
import time 
import random

# Arduino Serial Object
arduino = serial.Serial(port = 'COM4', baudrate = 115200, timeout = 0.1) 



KILL_SWITCH = 0b10000000
PWM_ENABLE = 0b00000001
SENSOR_ENABLE = 0b00000010
SENSOR_FETCH = 0b00100000

SENSOR_DATA_END = bytearray(0xFFFFFFFF)

#-
# BASIC SERIAL DATA TRANSFER:
# - Create bytearray() object
# - Populate with values:
#  > Convert numerical values to bytearray(num.to_bytes(size, "little")) and use .append(arr)
#  > Directly use .append(num) when integer value is less than 256
# - Send using .write(populated_byte_arr)
# -#

#-
# CONTROL FLAG FORMAT:
# BYTE  NAME            STATES
# 0     BYTE_COUNT      0x04 = FLAG ONLY | 0x14 = FLAG + 8 MOTORS
# 1     R_STATE         0x00 = FULL ACTIVE | 0x04 = CONTROL ONLY | 0xF = CONTROLLED SHUTDOWN | 0xFF = EMERGENCY SHUTDOWN
# 2     SENSOR_QUERY    0x00 = NO QUERY | 0x04 = QUERY CAMERA | 0xF = QUERY VITALS | 0xF8 = QUERY POSITION | 0xFF = QUERY HYDROPHONE
# 3     PWM_ENABLE      BITS ACT AS FLAGS FOR MOTORS 0-7 | 0x00 = ALL INACTIVE | 0xFF = ALL ACTIVE
# -#

def get_pwm():
    return bytearray(random.randint(1000,2000).to_bytes(2,"little"))

def send_pwm():
    byte_data = bytearray()
    
    byte_data.append(PWM_ENABLE | SENSOR_ENABLE | SENSOR_FETCH)
    
    for _ in range(8):
        for i in get_pwm():
            byte_data.append(i)


    arduino.write(byte_data)

    print(byte_data)

    time.sleep(0.5)

    sensor_data = arduino.read_all() # arduino.read_until(SENSOR_DATA_END)
    
    print(list(sensor_data))

    return

while True: 
    send_pwm()
    time.sleep(5)

