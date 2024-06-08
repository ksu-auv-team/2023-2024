from smbus2 import SMBus
import time
while True:
    try:
        # Open i2c bus 1 and read one byte from address 80, offset 0
        bus = SMBus(7)
        b = bus.read_byte_data(80, 0)
        print(b)
        bus.close()
    except Exception as e:
        print(e)
        time.sleep(1)
