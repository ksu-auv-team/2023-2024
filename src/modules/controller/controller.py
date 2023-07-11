# Import the custom networking module
from src.modules.networking.networking import Networking

# Import other libraries that will be needed
from dataclasses import dataclass
from inputs import get_gamepad
import numpy as np
import struct


# Data class that will handle the controller
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


# Create the controller class that will handle the controller inputs
class Controller:
    def __init__(self, host, port):
        # Initialize the networking module
        self.socket = Networking()
        self.socket.connect(host, port)

        # Initialize the controller
        self.events = get_gamepad()
        self.controller_data = Gamepad_State()

        # Initialize the dictionary that will map the controller inputs to the dataclass
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

    def get_data(self):
        self.events = get_gamepad()

        for event in self.events:
            attribute = self.code_to_attribute.get(event.code)
            if attribute:
                setattr(self.controller_data, attribute, event.state)

        return self.controller_data

    def return_data(self):
        return self.controller_data

    def run(self):
        while True:
            controller_data = self.get_data()
            print(controller_data)


if __name__ == "__main__":
    controller = Controller('localhost', 9999)
    controller.run()
