from smbus import SMBus

#creating slave addresses and i2c bus
a1_addr = 0x06
a2_addr = 0x07
a3_addr = 0x08
I2Cbus = smbus.SMBus(1)

numSelect = input("Which Arduino (1-3): ")

modeSelect = input("On or Off (on/off): ")

if numSelect == 1:
    SlaveAddress = a1_addr
elif numSelect == 2:
    SlaveAddress = a2_addr
elif numSelect == 3:
    SlaveAddress = a3_addr


if modeSelect == "1":
    bus.write_byte(SlaveAddress, 0x1)
elif modeSelect == "0":
    bus.write_byte(SlaveAddress, 0x0)
#possible statement allowing to break if incorrect mode is entered
else:
    quit()

