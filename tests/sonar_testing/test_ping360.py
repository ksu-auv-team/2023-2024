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
            data = []
            temp_data = []
            for x in range(360):
                temp_data.append(p.transmitAngle(x))
                print(temp_data[x][data])
        except KeyboardInterrupt:
            break    
    print(data)

if __name__ == "__main__":
    test_ping360()