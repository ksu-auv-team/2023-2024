from smbus2 import SMBus
import time
while True:
    try:
        data = [127, 127, 127, 127, 127, 127, 127, 127]
        # Open i2c bus 1 and read one byte from address 80, offset 0
        bus = SMBus(7)
        # b = bus.read_byte_data(8, 0)
        b = bus.write_i2c_block_data(8,  0, data)
        print(b)
        bus.close()
    except Exception as e:
        print(e)
        time.sleep(1)
