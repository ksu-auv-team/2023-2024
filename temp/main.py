import PySimpleGUI as sg
import numpy as np
from numpysocket import NumpySocket

import logging
import time
import threading
import os
import sys
import yaml

# Import the main assets


class Main:
    def __init__(self):
        # Define some constants
        bar_max = 2000
        bar_min = 1000
        bar_mid = (bar_max + bar_min) / 2

        # Set the gui theme
        sg.theme('DarkAmber')

        # Create the layout for the GUI
        # Right layout (motor data) ( 8 motors and 3 servos)
        right_layout = [
            [sg.Text('Actuator Data', font=('Helvetica', 25))],
            [sg.HorizontalSeparator()],
            [sg.Text('Motor Data', font=('Helvetica', 25))],
            [sg.HorizontalSeparator()],
            [sg.Text('Motor 1', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor1')],
            [],
            [sg.Text('Motor 2', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor2')],
            [],
            [sg.Text('Motor 3', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor3')],
            [],
            [sg.Text('Motor 4', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor4')],
            [],
            [sg.Text('Motor 5', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor5')],
            [],
            [sg.Text('Motor 6', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor6')],
            [],
            [sg.Text('Motor 7', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor7')],
            [],
            [sg.Text('Motor 8', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor8')],
            [sg.HorizontalSeparator()],
            [sg.Text('Servo Data', font=('Helvetica', 25))],
            [sg.HorizontalSeparator()],
            [sg.Text('Servo 1', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='servo1')],
            [],
            [sg.Text('Servo 2', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='servo2')],
            [],
            [sg.Text('Servo 3', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='servo3')],
        ]

        # Left layout (sensor data and button controls) (Depth, Temperature, Humidity, Voltage, Current, and Power Draw)
        left_layout = [
            [sg.Text('Sensor Data', font=('Helvetica', 25))],
            [sg.HorizontalSeparator()],
            [sg.Text('Depth', font=('Helvetica', 20)), sg.Text('0', font=('Helvetica', 20), key='depth'), sg.Text('m', font=('Helvetica', 20))],
            [],
            [sg.Text('Temperature', font=('Helvetica', 20)), sg.Text('0', font=('Helvetica', 20), key='temperature'), sg.Text('°C', font=('Helvetica', 20))],
            [],
            [sg.Text('Humidity', font=('Helvetica', 20)), sg.Text('0', font=('Helvetica', 20), key='humidity'), sg.Text('%', font=('Helvetica', 20))],
            [],
            [sg.Text('Voltage', font=('Helvetica', 20)), sg.Text('0', font=('Helvetica', 20), key='voltage'), sg.Text('V', font=('Helvetica', 20))],
            [],
            [sg.Text('Current', font=('Helvetica', 20)), sg.Text('0', font=('Helvetica', 20), key='current'), sg.Text('A', font=('Helvetica', 20))],
            [],
            [sg.Text('Power Draw', font=('Helvetica', 20)), sg.Text('0', font=('Helvetica', 20), key='power_draw'), sg.Text('W', font=('Helvetica', 20))],
            [sg.HorizontalSeparator()],
            [sg.Text('Controls', font=('Helvetica', 25))],
            [sg.HorizontalSeparator()],
            [sg.Checkbox('Enable Motors', font=('Helvetica', 20), key='enable_motors')],
            [sg.Checkbox('Enable Servos', font=('Helvetica', 20), key='enable_servos')],
            [sg.Checkbox('Enable Sensors', font=('Helvetica', 20), key='enable_sensors')],
            [sg.Checkbox('Enable Camera', font=('Helvetica', 20), key='enable_camera')],
            [sg.HorizontalSeparator()],
            [sg.Button('Update Config', font=('Helvetica', 15), key='update_config', size=(18, 1))],
            [sg.Button('Save Config', font=('Helvetica', 15), key='save_config', size=(18, 1))],
            [sg.Button('Load Config', font=('Helvetica', 15), key='load_config', size=(18, 1))],
            [sg.Button('Start', font=('Helvetica', 15), key='start', size=(18, 1))],
            [sg.Button('Stop', font=('Helvetica', 15), key='stop', size=(18, 1))],
            [sg.Button('Exit', font=('Helvetica', 15), key='exit', size=(18, 1))]
        ]

        # Middle layout (Title, camera feed, and quick settings) ( # TODO: Add quick settings)
        middle_layout = [
            [sg.Text('Surface Station', font=('Helvetica', 25), justification='center')],
            [sg.Image(filename='imgs/placeholder.png', key='camera_feed', size=(1280, 720))],
            [sg.HorizontalSeparator()],
            [sg.Text('Quick Settings', font=('Helvetica', 25))],
            [sg.HorizontalSeparator()],
            [
                sg.VerticalSeparator(),
                sg.Column(
                    [
                        [sg.Text('Motor Power Execution', font=('Helvetica', 20))],
                        [sg.Slider(range=(0, 100), default_value=50, orientation='h', size=(30, 20), key='motor_power_efficiency')],
                        [sg.HorizontalSeparator()],
                        [sg.Text('Camera FPS', font=('Helvetica', 20))],
                        [sg.Slider(range=(30, 60), default_value=60, orientation='h', size=(30, 20), key='camera_fps')],
                    ], justification='center', element_justification='center'
                ),
                sg.VerticalSeparator(),
                sg.Column(
                    [
                        [sg.Button('Save Settings', font=('Helvetica', 20), key='save_settings')],
                        [sg.Button('Load Settings', font=('Helvetica', 20), key='load_settings')],
                        [sg.Button('Reset Settings', font=('Helvetica', 20), key='reset_settings')]
                    ], justification='center', element_justification='center'
                )
            ]
        ]

        # Main layout (combines all layouts into one)
        layout = [
            [
                sg.Column(right_layout, key='motor_data', size=(320, 1080), element_justification='center'),
                sg.Column(middle_layout, key='settings', size=(1280, 1080), element_justification='center'),
                sg.Column(left_layout, key='sensor_data', size=(320, 1080), element_justification='center')
            ]
        ]
        
        # Create the window
        self.window = sg.Window('Surface Station', layout, size=(1920, 1080), element_justification='center')
        
        with open('configs/main.yml', 'r') as f:
            self.config = yaml.safe_load(f)

    # Create the start function to start each thread on the Orin
    def start_sub(self):
        pass
    
    
    # Create the update data function to update the data on the GUI (i.e. joystick data, sensor data, motor data, etc.)
    def update_data(self, data: np.ndarray):
        # Example data
        # data = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
        # data[:8] = motors
        # data[8:12] = servos
        # data[12:] = sensors
        # TODO: Update the data on the GUI
        pass
    
    # Create the update camera function to update the camera feed on the GUI
    def update_camera(self, frame: np.ndarray):
        pass
    
    # Handles the connection to the robot
    def numpySocket(self, thread_id: int) -> np.ndarray:
        with NumpySocket() as nps:
            nps.connect((self.config['robot_ip'], self.config['robot_port']))
            
            while True:
                pass 
    
    # Handles the parsing of the incoming data (contains the sensor and camera data)
    def parseIncomingData(self, data: np.ndarray) -> np.ndarray:
        pass
    
    # Handles the parsing of the outgoing data (contains the motor data)
    def parseOutgoingData(self, data: np.ndarray) -> np.ndarray:
        pass
    
    # Handles the connection to the controller
    def controllerSocket(self) -> np.ndarray:
        pass
    
    # Run the GUI and accept inputs
    def run(self):
        event, values = self.window.read()
        if self.config['enable_motors']:
            self.window.Element('enable_motors').update(value=True)
        if self.config['enable_servos']:
            self.window.Element('enable_servos').update(value=True)
        if self.config['enable_sensors']:
            self.window.Element('enable_sensors').update(value=True)
        if self.config['enable_camera']:
            self.window.Element('enable_camera').update(value=True)
        while True:
            event, values = self.window.read()
            print(event, values)
            if event == sg.WIN_CLOSED:
                break

# TODO: Create the necessary functions to both start and stop the code remotely
# TODO: Create the necessary functions to handle event loops and callbacks
# TODO: Create the necessary functions to handle the data (i.e. read and parse the joystick data)

if __name__ == '__main__':
    surface_station = Main()
    surface_station.run()