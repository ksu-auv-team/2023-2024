from brping import Ping1D

myPing = Ping1D()
myPing.connect_serial("/dev/ttyUSB0", 115200)

if myPing.initialize() is False:
    print("Failed to initialize Ping!")
    exit(1)

data = myPing.get_distance()
if data:
    print("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
else:
    print("Failed to get distance data")

