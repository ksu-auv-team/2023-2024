# Libraries 
import serial 
import time 
import random

# Arduino Serial Object
arduino = serial.Serial(port = 'COM4', baudrate = 115200, timeout = 0.1) 

arduino.flush()

FULL_ACTIVE = 0xFF
CONTROL_ONLY = 0x04
CONTROLLED_SHUTDOWN = 0x0F
EMERGENCY_SHUTDOWN = 0xFF

KILL_SWITCH = 0b10000000
PWM_ENABLE = 0b00000001
SENSOR_ENABLE = 0b00000010
SENSOR_FETCH = 0b00100000

SENSOR_DATA_END = bytearray(0xFFFFFFFF)

# BASIC SERIAL DATA TRANSFER:
# - Create bytearray() object
# - Populate with values:
#  > Convert numerical values to bytearray(num.to_bytes(size, "little")) and use .append(arr)
#  > Directly use .append(num) when integer value is less than 256
# - Send using .write(populated_byte_arr)

# CONTROL FLAG FORMAT:
# BYTE  NAME            STATES
# 0     BYTE_COUNT      0x04 = FLAG ONLY | 0x0C = FLAG + 8 MOTORS
# 1     R_STATE         0x00 = FULL ACTIVE | 0x04 = CONTROL ONLY | 0xF = CONTROLLED SHUTDOWN | 0xFF = EMERGENCY SHUTDOWN
# 2     SENSOR_QUERY    0x00 = NO QUERY | 0x04 = QUERY CAMERA | 0xF = QUERY VITALS | 0xF8 = QUERY POSITION | 0xFF = QUERY HYDROPHONE
# 3     PWM_ENABLE      BITS ACT AS FLAGS FOR MOTORS 0-7 | 0x00 = ALL INACTIVE | 0xFF = ALL ACTIVE

# Resolution of PWM for Arduino is only 256, cap to 250 for easy conversion (0 = 1000, 250 = 2000), reduces data transfer by ~40%
def get_pwm():
    return bytearray(random.randint(0,250).to_bytes(1,"little"))

def send_pwm():
    byte_data = bytearray()
    
    byte_data.append(0x0C) # Standard transfer - 4 byte control flag - 8 byte PWM data
    byte_data.append(0x00) # Normal robot state
    byte_data.append(0x00) # No sensor query
    byte_data.append(0xFF) # All motor enable
    
    for _ in range(8):
        for i in get_pwm():
            byte_data.append(i)


    arduino.write(byte_data) # Send over serial

    print(list(byte_data)) # Debug

    time.sleep(0.1)

    sensor_data = arduino.read_all() # TODO: End codes & start codes
    
    print(list(sensor_data)) # Debug

    return

while True: 
    send_pwm()
    time.sleep(5)

