
# Import the necessary python libraries
import os
import sys
import datetime
import logging
import platform
import subprocess
from dataclasses import dataclass

# Import the necessary custom libraries
import PySimpleGUI as sg
import numpy as np
from numpysocket import NumpySocket
import serial
import yaml
from inputs import get_gamepad, devices


# Define the dataclass for the ground control station joystick data
@dataclass
class Joystick:
    x_axis: float = 0.0
    y_axis: float = 0.0
    z_axis: float = 0.0
    
# Define the dataclass for the ground control station controller data
@dataclass
class Controller:
    left: Joystick
    right: Joystick
    buttons: dict
    

# Main class
class GCS:
    def __init__(self):
        # Create the log folder
        date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        os.mkdir(f'logs/{date}')
        
        # Create the logger which outputs a log file to the log folder that was just created
        logging.basicConfig(filename=f'logs/{date}/gcs.log', level=logging.DEBUG)
        
        # Create the logger which outputs to the console
        self.console = logging.StreamHandler()
        
        # Set the logging level for the console logger
        self.console.setLevel(logging.INFO)
        
        # Create the formatter for the console logger
        console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.console.setFormatter(console_format)
        
        # Add the console logger to the logger
        logging.getLogger('').addHandler(self.console)
        
        # Log the start of the program
        logging.info('Starting the ground control station')
        
        # Load the configuration file
        with open('configs/gcs.yml', 'r') as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
            
        # Log the configuration file
        logging.info(f'Configuration file: {self.config}')
        
        # if self.config['serial'] == True:
        if self.config['serial']['enabled']:
            # Log that the serial port is being opened
            logging.info('Opening the serial port')
            
            # Open the serial port
            self.serial = serial.Serial(
                port=self.config['serial']['serial_port'],
                baudrate=self.config['serial']['serial_baudrate'],
                timeout=self.config['serial']['serial_timeout'],
            )
            
            # Log that the serial port was opened
            logging.info('Serial port opened at ' + str(self.serial.name))
        else:
            self.serial = None
        
        # Make sure the serial port is open and send the start bit
        if self.serial is not None:
            self.serial.write(b'1\n')
        
        # Create the GUI layout and supporting variables
        title_size = (20, 1)
        data_label_size = (15, 1)
        data_size = (15, 1)
        font_size = 20
        font = ("Arial", font_size)
        placeholder_image = 'images/placeholder.png'
        camera_feed_size = (1280, 720)
        progress_bar_size = (25, 20)
        button_size = (15, 1)
        val = 100
        
        # Set the theme for the GUI
        sg.theme('DarkAmber')
        
        self.joystick_list = []
        
        config_button_column = sg.Column(
            [
                [sg.Button('', image_filename='images/icons/icons8-home-25.png', image_size=(25, 25), border_width=0, key='home')],
                [sg.HorizontalSeparator()],
                [sg.Button('', image_filename='images/icons/icons8-home-25.png', image_size=(25, 25), border_width=0, key='camera')],
                [sg.HorizontalSeparator()],
                [sg.Button('', image_filename='images/icons/icons8-home-25.png', image_size=(25, 25), border_width=0, key='joystick')],
                [sg.HorizontalSeparator()],
                [sg.Button('', image_filename='images/icons/icons8-home-25.png', image_size=(25, 25), border_width=0, key='settings')],
                [sg.HorizontalSeparator()],
                [sg.Button('', image_filename='images/icons/icons8-home-25.png', image_size=(25, 25), border_width=0, key='settings')],
                [sg.HorizontalSeparator()],
                [sg.Button('', image_filename='images/icons/icons8-home-25.png', image_size=(25, 25), border_width=0, key='settings')],
                [sg.HorizontalSeparator()],
                [sg.Button('', image_filename='images/icons/icons8-home-25.png', image_size=(25, 25), border_width=0, key='settings')],
                [sg.HorizontalSeparator()]
            ], size=(50, 1080), element_justification='center'
        )        
        home_config = sg.Column(
            [
                [sg.Text('Ground Station Config', size=title_size, font=font)],
                [sg.HorizontalSeparator()],
                [sg.Text('Arduino Config', size=title_size, font=font)],
                [sg.Text('Serial Port', size=data_label_size, font=font), sg.InputText(self.config['serial']['serial_port'], size=data_size, key='serial_port'), sg.Button('Update', size=button_size, key='update_serial_port')],
                [sg.Text('Serial Baudrate', size=data_label_size, font=font), sg.InputText(self.config['serial']['serial_baudrate'], size=data_size, key='serial_baudrate'), sg.Button('Update', size=button_size, key='update_serial_baudrate')],
                [sg.Text('Serial Timeout', size=data_label_size, font=font), sg.InputText(self.config['serial']['serial_timeout'], size=data_size, key='serial_timeout'), sg.Button('Update', size=button_size, key='update_serial_timeout')],
                [sg.HorizontalSeparator()]
            ], size=(270, 1080), element_justification='center', visible=False
        )
        camera_config = sg.Column(
            [
                [sg.Text('Camera Config', size=title_size, font=font)],
                [sg.Text('Camera IP', size=data_label_size, font=font), sg.InputText(self.config['camera']['camera_ip'], size=data_size, key='camera_ip'), sg.Button('Update', size=button_size, key='update_camera_ip')],
                [sg.Text('Camera Port', size=data_label_size, font=font), sg.InputText(self.config['camera']['camera_port'], size=data_size, key='camera_port'), sg.Button('Update', size=button_size, key='update_camera_port')],
                [sg.Text('Camera Resolution', size=data_label_size, font=font), sg.InputText(self.config['camera']['camera_resolution'], size=data_size, key='camera_resolution'), sg.Button('Update', size=button_size, key='update_camera_resolution')],
                [sg.Text('Camera FPS', size=data_label_size, font=font), sg.InputText(self.config['camera']['camera_fps'], size=data_size, key='camera_fps'), sg.Button('Update', size=button_size, key='update_camera_fps')],
                [sg.HorizontalSeparator()]
            ], size=(270, 1080), element_justification='center', key='camera_config', visible=False
        )
        joystick_config = sg.Column(
            [
                [sg.Text('Joystick Config', size=title_size, font=font)],
                [sg.HorizontalSeparator()],
                [sg.Text('Select Controller: ', size=data_label_size, font=font), sg.Combo(self.joystick_list, size=data_size, key='joystick_list'), sg.Button('Update', size=button_size, key='update_joystick_list')],
                [sg.HorizontalSeparator()],
            ], size=(270, 1080), element_justification='center', key='joystick_config', visible=False
        )
        robot_config = sg.Column(
            [
                [sg.Text('Robot Config', size=title_size, font=font)],
            ], size=(270, 1080), element_justification='center', key='robot_config', visible=False
        )
        movement_config = sg.Column(
            [
                [sg.Text('Movement Config', size=title_size, font=font)]
            ], size=(270, 1080), element_justification='center', key='movement_config', visible=False
        )
        sensor_config = sg.Column(
            [
                [sg.Text('Sensor Config', size=title_size, font=font)]
            ], size=(270, 1080), element_justification='center', key='sensor_config', visible=False
        )
        state_config = sg.Column(
            [
                [sg.Text('State Config', size=title_size, font=font)]
            ], size=(270, 1080), element_justification='center', key='state_config', visible=False
        )
        middle_column = sg.Column(
            [
                [sg.Image(placeholder_image, size=camera_feed_size, key='camera_feed')],
                [sg.HorizontalSeparator()],
                [
                    sg.Column(
                        [
                            [sg.Text('Batt 1 (V)', size=data_label_size, font=font)],
                            [sg.ProgressBar(max_value=val, size=progress_bar_size, orientation='v', key='battery_1_voltage')],
                            [sg.Text('Batt 1 (A)', size=data_label_size, font=font)],
                            [sg.ProgressBar(max_value=val, size=progress_bar_size, orientation='v', key='battery_1_current')]
                        ], size=(1550/10, (1080-720)), element_justification='center', justification='center'
                    ),
                    sg.Column(
                        [
                            [sg.Text('Batt 2 (V)', size=data_label_size, font=font)],
                            [sg.ProgressBar(max_value=val, size=progress_bar_size, orientation='v', key='battery_2_voltage')],
                            [sg.Text('Batt 2 (A)', size=data_label_size, font=font)],
                            [sg.ProgressBar(max_value=val, size=progress_bar_size, orientation='v', key='battery_2_current')]
                        ], size=(1550/10, (1080-720)), element_justification='center'
                    ),
                    sg.Column(
                        [
                            [sg.Text('Batt 3 (V)', size=data_label_size, font=font)],
                            [sg.ProgressBar(max_value=val, size=progress_bar_size, orientation='v', key='battery_3_voltage')],
                            [sg.Text('Batt 3 (A)', size=data_label_size, font=font)],
                            [sg.ProgressBar(max_value=val, size=progress_bar_size, orientation='v', key='battery_3_current')]
                        ], size=(1550/10, (1080-720)), element_justification='center'
                    ),
                    sg.Column(
                        [
                            [sg.Text('Batt 4 (V)', size=data_label_size, font=font)],
                            [sg.ProgressBar(max_value=val, size=progress_bar_size, orientation='v', key='battery_4_voltage')],
                            [sg.Text('Batt 4 (A)', size=data_label_size, font=font)],
                            [sg.ProgressBar(max_value=val, size=progress_bar_size, orientation='v', key='battery_4_current')]
                        ], size=(1550/10, (1080-720)), element_justification='center'
                    ),
                    sg.Column(
                        [
                            [sg.Text('Orin IP: ', size=data_label_size, font=font), sg.InputText(default_text=self.config['orin']['orin_ip'], size=data_size, font=font, key='orin_ip')],
                            [sg.Button('Start', size=button_size, font=font, key='start')],
                            [sg.Button('Stop', size=button_size, font=font, key='stop')],
                            [sg.Button('Reset', size=button_size, font=font, key='reset')],
                            [sg.Button('Connect', size=button_size, font=font, key='connect')]
                        ], size=(775, (1080-720)), element_justification='center'
                    )
                ]
            ], size=(1550, 1080), element_justification='left'
        )
        data_config = sg.Column(
            [
                [sg.Text('Data', size=title_size, font=font)],
                [sg.HorizontalSeparator()],
                [sg.Text('Controller Data', size=title_size, font=font)],
                [
                    # Axis X
                    sg.Column(
                        [
                            [sg.Text('X', size=data_label_size, font=font)],
                            [sg.ProgressBar(max_value=val, size=progress_bar_size, orientation='v', key='controller_x')],
                        ], size=(64, 150), element_justification='left'
                    ),
                    # Axis Y
                    sg.Column(
                        [
                            [sg.Text('Y', size=data_label_size, font=font)],
                            [sg.ProgressBar(max_value=val, size=progress_bar_size, orientation='v', key='controller_y')],
                        ], size=(64, 150), element_justification='left'
                    ),
                    # Axis Z
                    sg.Column(
                        [
                            [sg.Text('Z', size=data_label_size, font=font)],
                            [sg.ProgressBar(max_value=val, size=progress_bar_size, orientation='v', key='controller_z')],
                        ], size=(64, 150), element_justification='left'
                    )
                ],
                [
                    # Axis T (throttle)
                    sg.Column(
                        [
                            [sg.Text('T', size=data_label_size, font=font)],
                            [sg.ProgressBar(max_value=val, size=progress_bar_size, orientation='v', key='controller_t')],
                        ], size=(64, 150), element_justification='left'
                    ),
                    # Axis A (Acceleration)
                    sg.Column(
                        [
                            [sg.Text('A', size=data_label_size, font=font)],
                            [sg.ProgressBar(max_value=val, size=progress_bar_size, orientation='v', key='controller_a')],
                        ], size=(64/5, 150), element_justification='left'
                    )
                ],
                [sg.HorizontalSeparator()],
            ], size=(320, 1080), element_justification='center'
        )
        try:
            window_layout = [
                [
                    config_button_column,
                    sg.VerticalSeparator(),
                    home_config,
                    camera_config,
                    joystick_config,
                    robot_config,
                    movement_config,
                    sensor_config,
                    state_config,
                    middle_column,
                    sg.VerticalSeparator(),
                    data_config
                ]
            ]
        except Exception as e:
            logging.error(e)        
        
        self.window = sg.Window('KSU Control Panel', window_layout, size=(1920, 1080), finalize=True)
        self.window.Maximize()
    
    def config_button_click(self, button):
        if button == 'home':
            self.window['home_config'].update(visible=True)
            self.window['camera_config'].update(visible=False)
            self.window['joystick_config'].update(visible=False)
            self.window['robot_config'].update(visible=False)
            self.window['movement_config'].update(visible=False)
            self.window['sensor_config'].update(visible=False)
            self.window['state_config'].update(visible=False)
            self.window['middle_column'].update(size=(1280, 1080))
        elif button == 'camera':
            self.window['home_config'].update(visible=False)
            self.window['camera_config'].update(visible=True)
            self.window['joystick_config'].update(visible=False)
            self.window['robot_config'].update(visible=False)
            self.window['movement_config'].update(visible=False)
            self.window['sensor_config'].update(visible=False)
            self.window['state_config'].update(visible=False)
            self.window['middle_column'].update(size=(1280, 1080))
        elif button == 'joystick':
            self.window['home_config'].update(visible=False)
            self.window['camera_config'].update(visible=False)
            self.window['joystick_config'].update(visible=True)
            self.window['robot_config'].update(visible=False)
            self.window['movement_config'].update(visible=False)
            self.window['sensor_config'].update(visible=False)
            self.window['state_config'].update(visible=False)
            self.window['middle_column'].update(size=(1280, 1080))
        elif button == 'robot':
            self.window['home_config'].update(visible=False)
            self.window['camera_config'].update(visible=False)
            self.window['joystick_config'].update(visible=False)
            self.window['robot_config'].update(visible=True)
            self.window['movement_config'].update(visible=False)
            self.window['sensor_config'].update(visible=False)
            self.window['state_config'].update(visible=False)
            self.window['middle_column'].update(size=(1280, 1080))
        elif button == 'movement':
            self.window['home_config'].update(visible=False)
            self.window['camera_config'].update(visible=False)
            self.window['joystick_config'].update(visible=False)
            self.window['robot_config'].update(visible=False)
            self.window['movement_config'].update(visible=True)
            self.window['sensor_config'].update(visible=False)
            self.window['state_config'].update(visible=False)
            self.window['middle_column'].update(size=(1280, 1080))
        elif button == 'sensor':
            self.window['home_config'].update(visible=False)
            self.window['camera_config'].update(visible=False)
            self.window['joystick_config'].update(visible=False)
            self.window['robot_config'].update(visible=False)
            self.window['movement_config'].update(visible=False)
            self.window['sensor_config'].update(visible=True)
            self.window['state_config'].update(visible=False)
            self.window['middle_column'].update(size=(1280, 1080))
        elif button == 'state':
            self.window['home_config'].update(visible=False)
            self.window['camera_config'].update(visible=False)
            self.window['joystick_config'].update(visible=False)
            self.window['robot_config'].update(visible=False)
            self.window['movement_config'].update(visible=False)
            self.window['sensor_config'].update(visible=False)
            self.window['state_config'].update(visible=True)
            self.window['middle_column'].update(size=(1280, 1080))
        else:
            self.window['home_config'].update(visible=False)
            self.window['camera_config'].update(visible=False)
            self.window['joystick_config'].update(visible=False)
            self.window['robot_config'].update(visible=False)
            self.window['movement_config'].update(visible=False)
            self.window['sensor_config'].update(visible=False)
            self.window['state_config'].update(visible=False)
            self.window['middle_column'].update(size=(1550, 1080))

    def ping_orin(self):
        pass
    
    def ssh_orin(self):
        pass
    
    def run(self):
        while True:
            event, values = self.window.read(timeout=100)
            
            # Log the event and values for debugging
            if event != '__TIMEOUT__':
                logging.info(f'Event: {event}, Values: {values}')
            else:
                pass
                    
            if event == sg.WIN_CLOSED:
                break

if __name__ == '__main__':
    gui = GCS()
    gui.run()