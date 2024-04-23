from modules.NetworkingProtocol import NetworkingProtocol
import numpy as np
import logging
import pygame
import json

class CM:
    def __init__(self, mapping_choice='regular'):
        pygame.init()
        self.network_protocol = NetworkingProtocol()
        self.init_joystick()

        with open('configs/controller.json', 'r') as f:
            self.config = json.load(f)
            self.config = self.config['FlightController']

        self.map = self.config  # Simplified access to mapping from the config
        self.out_data = {key: 0 for key in self.map.keys()}

        logging.basicConfig(filename='logs/controller.log', level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    def init_joystick(self):
        while True:
            joystick_count = pygame.joystick.get_count()
            if joystick_count > 0:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                print(f"{joystick_count} joystick(s) found. Using the first one.")
                break
            else:
                print("No joystick found. Retrying in 3 seconds.")
                pygame.time.wait(3000)

    def get_data(self):
        pygame.event.pump()  # Process event queue
        self.joy_data = [round(self.joystick.get_axis(i), 2) for i in range(self.joystick.get_numaxes())] \
                      + [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())] \
                      + [self.joystick.get_hat(i) for i in range(self.joystick.get_numhats())]
        return self.joy_data

    def map_data(self):
        for control, settings in self.map.items():
            button, axis, inverted = settings
            value = None
            if axis is not None:
                value = self.joy_data[axis]
                if inverted:
                    value = -value
            if button is not None and self.joy_data[button]:
                value = 1 if not inverted else -1
            if value is not None:
                self.out_data[control] = value

    def post_data(self):
        self.network_protocol.send_data(self.out_data)  # Simulated network send

    def log_output(self, version=1):
        if version == 1:
            raw_data_log = f"Raw Data: {self.joy_data}"
            mapped_data_log = f"Mapped Data: {self.out_data}"
            logging.info(raw_data_log)
            logging.info(mapped_data_log)
            print(raw_data_log)
            print(mapped_data_log)

    def run(self):
        try:
            while True:
                self.get_data()
                self.map_data()
                self.post_data()
                self.log_output(version=1)
                pygame.time.wait(10)
        except KeyboardInterrupt:
            print("Terminated by user")

if __name__ == "__main__":
    cm = CM()
    cm.run()
