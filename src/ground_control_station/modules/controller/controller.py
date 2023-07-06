import struct
from dataclasses import dataclass
from inputs import get_gamepad
import numpy as np
import socket
import serial

@dataclass
class Gamepad_State:
    A: int = 0
    B: int = 0
    X: int = 0
    Y: int = 0
    D_Pad_Up_Down: int = 0
    D_Pad_Left_Right: int = 0 
    LB: int = 0
    RB: int = 0
    LT: int = 0
    RT: int = 0
    Left_Stick_Up_Down: int = 0
    Left_Stick_Left_Right: int = 0
    Right_Stick_Left_Right: int = 0
    Right_Stick_Up_Down: int = 0
    Back: int = 0
    Start: int = 0

    def to_byte_array(self):
        return struct.pack('16i', self.A, self.B, self.X, self.Y, self.D_Pad_Up_Down, self.D_Pad_Left_Right, self.LB, self.RB, self.LT, self.RT, self.Left_Stick_Up_Down, self.Left_Stick_Left_Right, self.Right_Stick_Left_Right, self.Right_Stick_Up_Down, self.Back, self.Start)


class Controller:
    def __init__(self, host, port, gamepad_type='xboxone', connect=False):
        self.host = host
        self.port = port
        self.gamepad_type = gamepad_type

        if connect:
            self.socket = socket.socket()
            self.socket.connect((self.host, self.port))
        else:
            self.socket = None

        if gamepad_type == 'xboxone':
            self.events = get_gamepad()
            self.controller_data = Gamepad_State()
            self.code_to_attribute = {
                'BTN_SOUTH': 'A',
                'BTN_EAST': 'B',
                'BTN_NORTH': 'X',
                'BTN_WEST': 'Y',
                'ABS_HAT0Y': 'D_Pad_Up_Down',
                'ABS_HAT0X': 'D_Pad_Left_Right',
                'BTN_TL': 'LB',
                'BTN_TR': 'RB',
                'ABS_Z': 'LT',
                'ABS_RZ': 'RT',
                'ABS_Y': 'Left_Stick_Up_Down',
                'ABS_X': 'Left_Stick_Left_Right',
                'ABS_RX': 'Right_Stick_Left_Right',
                'ABS_RY': 'Right_Stick_Up_Down',
                'BTN_SELECT': 'Back',
                'BTN_START': 'Start'
            }
        elif gamepad_type == 'custom':
            comport = 'COM3'
            baud = 115200
            self.ser = serial.Serial(comport, baudrate=baud, timeout=1)

            self.ser.write(b'1')

            hold = False
            while not hold:
                if self.ser.readline() == b'1':
                    print('Arduino connected')
                    hold = True
                else:
                    print('Arduino not connected')
                    self.ser.write(b'1')

    def xboxone_get_data(self):
        self.events = get_gamepad()

        for event in self.events:
            attribute = self.code_to_attribute.get(event.code)
            if attribute:
                setattr(self.controller_data, attribute, event.state)

        return self.controller_data

    def send_data(self, data):
        if self.socket is not None:
            self.socket.send(data)

    def run(self):
        while True:
            if self.gamepad_type == 'xboxone':
                controller_data = self.xboxone_get_data()
                print(controller_data)
                byte_data = controller_data.to_byte_array()
            elif self.gamepad_type == 'custom':
                byte_data = b'0'
            else:
                byte_data = b'0'

            self.send_data(byte_data)


if __name__ == "__main__":
    controller = Controller('localhost', 9999)
    controller.run()
