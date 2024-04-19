import numpy as np
import requests
import logging
import pygame
import json

# Mapping choices
# - regular: The default mapping.
# - flipped: The mapping with the two axis flipped.
# - inverted: The mapping with the two axis inverted.
# - inverted_flipped: The mapping with the two axis flipped and inverted.

# Example of the regular mapping:
# - Axis 0: Left stick, left-right : Yaw
# - Axis 1: Left stick, up-down : Z
# - Axis 2: Right stick, up-down : X
# - Axis 3: Right stick, left-right : Y
# - Axis 4: Button Press + Right Stick, up-down : Pitch
# - Axis 5: Button Press + Right Stick, left-right : Roll
# - Axis 6: Knob Axis, left-right : Claw


class CM:
    def __init__(self, mapping_choice : str = 'regular'):
        self.joystick = None
        self.init_joystick()

        with open('static/configs/controller.json') as f:
            self.config = json.load(f)
            self.config = self.config['controller']
        
        self.joy_data = []

        # Each element in the map list is a list with three elements: element 0 is the button number, element 1 is the axis number, and element 2 is whether the axis is inverted.
        self.map = {'Arm': [None, 19, 0], 'Yaw': [None, 0, 0], 'Z': [None, 1, 0], 'X': [None, 3, 0], 'Y': [None, 4, 0], 'Pitch': [20, 3, 0], 'Roll': [20, 4, 0], 'Claw': [None, 7, 0], 'Torpedo_1': [None, 11, 0], 'Torpedo_2': [None, 12, 0]}

        self.out_data = {"Arm": 0, "X": 0.0, "Y": 0.0, "Z": 0.0, "Pitch": 0.0, "Roll": 0.0, "Yaw": 0.0, "Claw": 0.0}
        self.mapping_choice = mapping_choice


        orin_ip = '127.0.0.1'
        self.url = f"http://{orin_ip}:5000/post_input_data"

        # Configure logging
        logging.basicConfig(filename='static/logs/app.log', level=logging.INFO, 
                            format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    def init_joystick(self):
        pygame.init()
        while True:
            joystick_count = pygame.joystick.get_count()
            if joystick_count > 0:
                print(f"{joystick_count} joystick(s) found. Using the first one.")
                break
            else:
                print("No joystick found. Retrying in 3 seconds.")
                pygame.time.wait(3000)
        
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def parse_mapping(self):
        pass

    def get_data(self):
        """
        Update the `data` array with the latest joystick values.
        
        ### Returns
        - `data`: The updated data array.

        ### Example
            Left Stick, Left-Right: 0.06
            Left Stick, Up-Down: -0.02
            Left Back Knob: -0.07
            Right Stick, Left-Right: -0.01
            Right Stick, Up-Down: 0.0
            Right Back Knob: -0.06
            Unknown: -1.0
            Top Knob: 0.93
            Left Button: 20th index
        - `data`: [0.06, -0.02, -0.07, -0.01, 0.0, -0.06, -1.0, 0.93, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.joystick.init()

        self.joy_data = [round(self.joystick.get_axis(i), 2) for i in range(self.joystick.get_numaxes())]
        for i in range(self.joystick.get_numbuttons()):
            self.joy_data.append(self.joystick.get_button(i))
        for i in range(self.joystick.get_numhats()):
            self.joy_data.append(self.joystick.get_hat(i))
        return self.joy_data

    def map_data(self):
        pass

    def post_data(self):
        pass

    def log_output(self, version: int = 0):
        if version == 0:
            logging.info(self.out_data)
            print(self.out_data)
        elif version == 1:
            temp = ""
            for i in range(len(self.joy_data)):
                temp += f'   {i}: {self.joy_data[i]}   |'
            logging.info(temp)
            print(temp)

    def run(self):
        while True:
            self.get_data()
            self.parse_mapping()
            self.map_data()
            self.post_data()
            self.log_output(version = 1)
            pygame.time.wait(10)

if __name__ == "__main__":
    cm = CM()
    cm.run()