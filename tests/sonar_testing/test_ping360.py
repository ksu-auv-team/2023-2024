from brping import Ping360

def test_ping360():
    p = Ping360()
    p.connect_serial("/dev/ttyUSB0", 115200)

    # Get data
    while True:
        try:
            data = []
            temp_data = []
            for x in range(360):
                temp_data.append(p.transmit_angle(x))
            data.append(temp_data)
        except KeyboardInterrupt:
            break    
    print(data)