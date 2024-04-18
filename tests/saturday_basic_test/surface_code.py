import logging
import pygame
import json
import requests

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
        
        self.joy_data = []

        # Each element in the map list is a list with three elements: element 0 is the button number, element 1 is the axis number, and element 2 is whether the axis is inverted.
        self.map = {
            'Arm': self.config['Arm'], 
            'Yaw': self.config['Yaw'], 
            'Z': self.config['Z'], 
            'X': self.config['X'], 
            'Y': self.config['Y'], 
            'Pitch': self.config['Pitch'], 
            'Roll': self.config['Roll'], 
            'Claw': self.config['Claw'], 
            'Torpedo_1': self.config['Torpedo_1'], 
            'Torpedo_2': self.config['Torpedo_2']
        }

        self.out_data = {"Arm": 0, "X": 0.0, "Y": 0.0, "Z": 0.0, "Pitch": 0.0, "Roll": 0.0, "Yaw": 0.0, "Claw": 0.0}

        orin_ip = '192.168.0.103'
        self.url = f"http://{orin_ip}:5000/post_input_data"

        # Configure logging
        logging.basicConfig(filename='static/logs/controller.log', level=logging.INFO, 
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
        pygame.event.pump()  # Process event queue
        self.joy_data = [round(self.joystick.get_axis(i), 2) for i in range(self.joystick.get_numaxes())]
        self.joy_data += [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
        self.joy_data += [self.joystick.get_hat(i) for i in range(self.joystick.get_numhats())]
        return self.joy_data

    def map_data(self):
        """
        Maps the joystick data based on configuration and button presses.
        """
        for control, settings in self.config.items():
            if settings[0] is None:  # No button press required
                axis_val = self.joy_data[settings[1]]
                if settings[2]:  # Invert the axis if necessary
                    axis_val = -axis_val
                self.out_data[control] = axis_val
            else:  # Button press affects the mapping
                if self.joy_data[settings[0]]:  # Check if the button is pressed
                    axis_val = self.joy_data[settings[1]]
                    if settings[2]:  # Invert the axis if necessary
                        axis_val = -axis_val
                    self.out_data[control] = axis_val

    def send_data(self):
        try:
            response = requests.post(self.url, json=self.out_data)
            print(f"Data sent to {self.url} with response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send data: {e}")

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
            self.send_data()
            # self.log_output(version = 0)
            pygame.time.wait(10)

