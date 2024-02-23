from brping import Ping360
from brping import definitions
import logging
import time

# Configure logging
logging.basicConfig(filename='ping360_data.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def test_ping360():
    p = Ping360()
    p.connect_serial("/dev/ttyUSB1", 115200)

    print(p.initialize())
    print(p.set_transmit_frequency(800))
    print(p.set_sample_period(80))
    print(p.set_number_of_samples(200))

    # Get data
    while True:
        try:
            data = []
            # for x in range(360):
            #     d = p.transmitAngle(x)
            #     data.append(d)
            #     # Log the data to a file after each for loop run
            #     logging.info(f"Angle: {x}, Data: {d}")

            # turn on auto-scan with 1 grad steps
            p.control_auto_transmit(0,399,1,0)

            # wait for 400 device_data messages to arrive
            for x in range(400):
                data.append(p.wait_message([definitions.PING360_DEVICE_DATA]))
            logging.debug(f"Data: {data}")

        except KeyboardInterrupt:
            break    

if __name__ == "__main__":
    test_ping360()


# --------------------------------------------------
# ID: 2300 - device_data
# Header: start_1: 66 start_2: 82 payload_length: 214 message_id: 2300 src_device_id: 2 dst_device_id: 0
# Payload:
#   - mode: 0
#   - gain_setting: 0
#   - angle: 70
#   - transmit_duration: 32
#   - sample_period: 80
#   - transmit_frequency: 800
#   - number_of_samples: 200
#   - data_length: 200
#   - data: ['0x2e', '0x74', '0x9c', '0xc5', '0xd3', '0xec', '0xf7', '0xf6', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xfb', '0xf6', '0xf3', '0xed', '0xed', '0xec', '0xe9', '0xe7', '0xe6', '0xe5', '0xe4', '0xe4', '0xe3', '0xe6', '0xe7', '0xe7', '0xe7', '0xe9', '0xeb', '0xec', '0xeb', '0xe9', '0xe6', '0xdc', '0xd2', '0xd1', '0xd3', '0xd5', '0xd5', '0xd4', '0xd3', '0xd4', '0xd5', '0xd7', '0xd7', '0xd4', '0xcf', '0xcc', '0xc5', '0xbc', '0xb1', '0xab', '0xaa', '0xa7', '0xa3', '0xa5', '0xa9', '0xac', '0xac', '0xa9', '0xa4', '0x9e', '0x87', '0x83', '0x89', '0x8c', '0x8d', '0x8f', '0x8f', '0x8d', '0x8a', '0x85', '0x83', '0x84', '0x85', '0x84', '0x80', '0x7f', '0x7e', '0x7d', '0x7d', '0x80', '0x82', '0x85', '0x89', '0x8e', '0x91', '0x90', '0x8b', '0x83', '0x7c', '0x77', '0x75', '0x78', '0x79', '0x76', '0x73', '0x6c', '0x6a', '0x70', '0x76', '0x7a', '0x7d', '0x7e', '0x7c', '0x78', '0x71', '0x6b', '0x5f', '0x5d', '0x61', '0x63', '0x66', '0x64', '0x61', '0x63', '0x67', '0x69', '0x68', '0x67', '0x66', '0x5d', '0x5a', '0x5b', '0x5a', '0x58', '0x4c', '0x45', '0x42', '0x3f', '0x3e', '0x44', '0x47', '0x50', '0x54', '0x59', '0x5c', '0x5b', '0x5c', '0x5a', '0x59', '0x58', '0x5b', '0x5f', '0x61', '0x64', '0x6a', '0x6e', '0x70', '0x6f', '0x6d', '0x66', '0x64', '0x62', '0x66', '0x6b', '0x72', '0x77', '0x7e', '0x85', '0x8d', '0x93', '0x98', '0x99', '0x99', '0x98', '0x92', '0x94', '0x98', '0xa0', '0xa9', '0xb2', '0xb9', '0xbe', '0xc1', '0xc1', '0xc2', '0xc4', '0xc6', '0xc6', '0xc5', '0xc5', '0xc7', '0xca', '0xce', '0xd3', '0xd8', '0xdb', '0xdd']
# Checksum: 33075 check: 33075 pass: True
