from brping import Ping360

def test_ping360():
    p = Ping360()
    p.connect_serial("/dev/ttyUSB0", 115200)

    print(p.initialize())
    print(p.set_transmit_frequency(800))
    print(p.set_sample_period(80))
    print(p.set_number_of_samples(200))

    # Get data
    while True:
        try:
            for x in range(360):
                print(p.transmitAngle(x))
                print(p.read())
                
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

# --------------------------------------------------
# b'-r\x9a\xc3\xd1\xe9\xf3\xf4\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfc\xf8\xf3\xf0\xea\xe9\xe9\xe7\xe6\xe3\xe1\xe0\xe0\xd9\xd7\xd2\xcc\xd4\xdd\xe4\xe9\xec\xee\xf0\xed\xe4\xdc\xd9\xdb\xdd\xdf\xe0\xdf\xde\xdf\xde\xd9\xcc\xba\xb5\xb6\xb4\xaf\xac\xac\xae\xae\xac\xa9\xa8\xa9\xa6\xa3\xa1\xa3\xa6\xa6\xa3\xa1\x9f\x9b\x95\x90\x8e\x8f\x8f\x8b\x8a\x88\x86trw\x7f\x86\x8e\x94\x98\x98\x97\x92\x8e\x8a\x87\x85\x84\x81~zxqhgikid_`cdcefc_ekli__acfg_elsvvuy~\x84\x8c\x95\x9d\xa2\xa7\xad\xb0\xb2\xb2\xb2\xb0\xae\xad\xaf\xb3\xb8\xbd\xc1\xc4\xc4\xc2\xbd\xb5\xa4\x9f\xa0\xa4\xa8\xab\xad\xac\xa9\xa7\xa3\x9b\x8e\x86\x86\x88\x8a\x8d\x90\x93\x95\x95\x93\x8c~z|\x7f\x80\x81}'