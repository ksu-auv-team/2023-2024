from modules.MovementPackageSupport.PID import PID
from modules.SupportAll.DebugHandler import DebugHandler

import requests
import numpy as np
import argparse

class MovementPackage:
    @staticmethod
    def mapping(self, x):
        return (x - self.in_min) * (self.out_max - self.out_min) / (self.in_max - self.in_min) + self.out_min
    
    def __init__(self, ip, port, debug):
        self.ip = ip
        self.port = port
        self.debug = debug
        
        self.horizontalMotors = [
            127, # M1
            127, # M2
            127, # M3
            127  # M4
        ]
        
        self.verticalMotors = [
            127, # M5
            127, # M6
            127, # M7
            127  # M8
        ]
        
        self.horizontalInputs = [
            0, # X
            0, # Y
            0 # Roll
        ]
        
        self.verticalInputs = [
            0, # Z
            0, # Pitch
            0 # Yaw
        ]
        
        self.input_data = {
            "X": 0,
            "Y": 0,
            "Z": 0,
            "Roll": 0,
            "Pitch": 0,
            "Yaw": 0,
            "Claw": 0,
            "Torp1": 0,
            "Torp2": 0
        }
        
        self.horizontalMapping = np.array([
            [1, 1, 1, 1],       # X
            [-1, -1, 1, 1],     # Y
            [-1, 1, -1, 1]      # Yaw
        ])
        
        self.verticalMapping = np.array([
            [1, 1, 1, 1],       # Z
            [-1, -1, 1, 1],     # Pitch
            [-1, 1, -1, 1]      # Roll
        ])
                
        self.output_data = {
            "M1": 0,
            "M2": 0,
            "M3": 0,
            "M4": 0,
            "M5": 0,
            "M6": 0,
            "M7": 0,
            "M8": 0,
            "Claw": 0,
            "Torp1": 0,
            "Torp2": 0
        }
        
        self.deadzone = 0.2
        
        self.debugger = DebugHandler(Package="MovementPackage", ip=self.ip, port=self.port)
        
    def get_data(self):
        request = requests.get(f'http://{self.ip}:{self.port}/inputs')
        self.input_data = request.json()
        
    def split_data(self):
        self.horizontalInputs = [
            self.input_data["X"],
            self.input_data["Y"],
            self.input_data["Roll"]
        ]
        
        self.verticalInputs = [
            self.input_data["Z"],
            self.input_data["Pitch"],
            self.input_data["Yaw"]
        ]
        
        self.output_data["Claw"] = self.input_data["Claw"]
        self.output_data["Torp1"] = self.input_data["Torp1"]
        self.output_data["Torp2"] = self.input_data["Torp2"]
    
    def calculate_motor_speeds(self):
        if abs(self.horizontalInputs[0]) < self.deadzone:
            self.horizontalInputs[0] = 0
        elif abs(self.horizontalInputs[0]) > self.deadzone:
            self.horizontalInputs[0] = self.mapping(self.horizontalInputs[0], -1, 1, 0, 255)
        elif abs(self.horizontalInputs[1]) < self.deadzone:
            self.horizontalInputs[1] = 0
        elif abs(self.horizontalInputs[1]) > self.deadzone:
            self.horizontalInputs[1] = self.mapping(self.horizontalInputs[1], -1, 1, 0, 255)
        elif abs(self.horizontalInputs[2]) < self.deadzone:
            self.horizontalInputs[2] = 0
        elif abs(self.horizontalInputs[2]) > self.deadzone:
            self.horizontalInputs[2] = self.mapping(self.horizontalInputs[2], -1, 1, 0, 255)
        
        if abs(self.verticalInputs[0]) < self.deadzone:
            self.verticalInputs[0] = 0
        elif abs(self.verticalInputs[0]) > self.deadzone:
            self.verticalInputs[0] = self.mapping(self.verticalInputs[0], -1, 1, 0, 255)
        elif abs(self.verticalInputs[1]) < self.deadzone:
            self.verticalInputs[1] = 0
        elif abs(self.verticalInputs[1]) > self.deadzone:
            self.verticalInputs[1] = self.mapping(self.verticalInputs[1], -1, 1, 0, 255)
        elif abs(self.verticalInputs[2]) < self.deadzone:
            self.verticalInputs[2] = 0
        elif abs(self.verticalInputs[2]) > self.deadzone:
            self.verticalInputs[2] = self.mapping(self.verticalInputs[2], -1, 1, 0, 255)
    
    def send_data(self):
        self.output_data = {
            "M1": self.horizontalInputs[0],
            "M2": self.horizontalInputs[1],
            "M3": self.horizontalInputs[2],
            "M4": self.horizontalInputs[3],
            "M5": self.verticalInputs[0],
            "M6": self.verticalInputs[1],
            "M7": self.verticalInputs[2],
            "M8": self.verticalInputs[3],
            "Claw": self.output_data["Claw"],
            "Torp1": self.output_data["Torp1"],
            "Torp2": self.output_data["Torp2"]
        }
        response = requests.post(f"{self.base_url}/outputs", json=self.output_data)
        if response.status_code != 201:
            self.handle_error(response.text)
    
    def print_data(self):
        message = f'{self.input_data}, {self.horizontalInputs}, {self.verticalInputs}, {self.output_data}'
        self.debugger.set_data(MessageType="LOG", Message=message)
    
    def handle_error(self, error):
        self.debugger.set_data(MessageType="ERROR", Message=error)
    
    def test_get_inputs(self):
        self.get_data()
    
    def test_calculate_motor_speeds(self):
        self.inputs = {
            "X": 0.5,
            "Y": 0.5,
            "Z": 0.5,
            "Roll": 0.5,
            "Pitch": 0.5,
            "Yaw": 0.5,
            "Claw": 1,
            "Torp1": 1,
            "Torp2": 1
        }
        self.split_data()
        self.calculate_motor_speeds()
        if self.debug:
            self.print_data()
    
    def test_send_data(self):
        self.horizontalMotors = [127, 127, 127, 127]
        self.verticalMotors = [127, 127, 127, 127]
        self.output_data['Claw'] = 0
        self.output_data['Torp1'] = 0
        self.output_data['Torp2'] = 0
        self.send_data()
        if self.debug:
            self.print_data()
    
    def run(self):
        while True:
            self.get_data()
            self.split_data()
            self.calculate_motor_speeds()
            self.send_data()
            if self.debug:
                self.print_data()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the Movement Package')
    parser.add_argument('--ip', type=str, default='localhost', help='IP to run the application on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the application on')
    parser.add_argument('--debug', action='store_true', help='Run the application in debug mode')
    args = parser.parse_args()
    
    movement_package = MovementPackage(args.ip, args.port, args.debug)
    movement_package.run()
    