
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
            
        # Make sure the serial port is open and send the start bit
        if self.serial.is_open:
            self.serial.write(b'1\n')
            
        # Create the GUI layout and supporting variables
        title_size = (20, 1)
        data_label_size = (15, 1)
        data_size = (10, 1)
        font_size = 20
        font = ("Helvetica", font_size)
        placeholder_image = 'images/placeholder.png'
        camera_feed_size = (1280, 720)
        progress_bar_size = (20, 10)
        button_size = (20, 1)
        
        config_button_column = sg.Column(
            [
                [sg.Button('', image_filename='images/icons/icons8-home-25.svg', image_size=(25, 25), border_width=0, key='home')],
                [sg.HorizontalSeparator()],
                [sg.Button('', image_filename='images/icons/icons8-camera-25.svg', image_size=(25, 25), border_width=0, key='camera')],
                [sg.HorizontalSeparator()],
                [sg.Button('', image_filename='images/icons/icons8-joystick-25.svg', image_size=(25, 25), border_width=0, key='joystick')],
                [sg.HorizontalSeparator()],
                [sg.Button('', image_filename='images/icons/icons8-robot-25.svg', image_size=(25, 25), border_width=0, key='settings')],
                [sg.HorizontalSeparator()],
                [sg.Button('', image_filename='images/icons/icons8-movement-25.svg', image_size=(25, 25), border_width=0, key='settings')],
                [sg.HorizontalSeparator()],
                [sg.Button('', image_filename='images/icons/icons8-sensor-25.svg', image_size=(25, 25), border_width=0, key='settings')],
                [sg.HorizontalSeparator()],
                [sg.Button('', image_filename='images/icons/icons8-state-25.svg', image_size=(25, 25), border_width=0, key='settings')],
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
                [sg.Image(imag=placeholder_image, size=camera_feed_size, key='camera_feed')],
                [sg.HorizontalSeparator()],
                [
                    sg.Column([
                    [
                        sg.Column([
                            sg.Text('Batt 1 (V)', size=data_label_size, font=font),
                            sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='battery_1_voltage')
                        ]),
                        sg.Column([
                            sg.Text('Batt 2 (V)', size=data_label_size, font=font),
                            sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='battery_2_voltage')
                        ]),
                        sg.Column([
                            sg.Text('Batt 3 (V)', size=data_label_size, font=font),
                            sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='battery_3_voltage')
                        ]),
                        sg.Column([
                            sg.Text('Batt 4 (V)', size=data_label_size, font=font),
                            sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='battery_4_voltage')
                        ])
                    ]]), 
                    sg.Column([
                    [
                        sg.Column([
                            sg.Text('Batt 1 (A)', size=data_label_size, font=font),
                            sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='battery_1_current')
                        ]),
                        sg.Column([
                            sg.Text('Batt 2 (A)', size=data_label_size, font=font),
                            sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='battery_2_current')
                        ]),
                        sg.Column([
                            sg.Text('Batt 3 (A)', size=data_label_size, font=font),
                            sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='battery_3_current')
                        ]),
                        sg.Column([
                            sg.Text('Batt 4 (A)', size=data_label_size, font=font),
                            sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='battery_4_current')
                        ])
                    ]]),    
                    sg.Column([
                        [sg.Text('Orin IP: ', size=data_label_size, font=font), sg.InputText('', size=data_size, font=font, key='orin_ip')],
                        [sg.Button('Start', size=button_size, font=font, key='start')],
                        [sg.Button('Stop', size=button_size, font=font, key='stop')],
                        [sg.Button('Reset', size=button_size, font=font, key='reset')],
                        [sg.Button('Connect', size=button_size, font=font, key='connect')]
                    ])
                ]
            ], size=(1550, 1080), element_justification='center'
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
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_x')],
                        ]
                    ),
                    # Axis Y
                    sg.Column(
                        [
                            [sg.Text('Y', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_y')],
                        ]
                    ),
                    # Axis Z
                    sg.Column(
                        [
                            [sg.Text('Z', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_z')],
                        ]
                    ),
                    # Axis T (throttle)
                    sg.Column(
                        [
                            [sg.Text('T', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_t')],
                        ]
                    ),
                    # Axis A (Acceleration)
                    sg.Column(
                        [
                            [sg.Text('A', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_a')],
                        ]
                    ),
                ],
                [
                    # Button 1 Column
                    sg.Column(
                        [
                            [sg.Text('B1', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_b0')],
                        ]
                    ),
                    # Button 2 Column
                    sg.Column(
                        [
                            [sg.Text('B2', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_b1')],
                        ]
                    ),
                    # Button 3 Column
                    sg.Column(
                        [
                            [sg.Text('B3', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_b2')],
                        ]
                    ),
                    # Button 4 Column
                    sg.Column(
                        [
                            [sg.Text('B4', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_b3')],
                        ]
                    ),
                    # Button 5 Column
                    sg.Column(
                        [
                            [sg.Text('B5', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_b4')],
                        ]
                    ),
                ],
                [
                    # Button 6 Column
                    sg.Column(
                        [
                            [sg.Text('B6', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_b5')],
                        ]
                    ),
                    # Button 7 Column
                    sg.Column(
                        [
                            [sg.Text('B7', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_b6')],
                        ]
                    ),
                    # Button 8 Column
                    sg.Column(
                        [
                            [sg.Text('B8', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_b7')],
                        ]
                    ),
                    # Button 9 Column
                    sg.Column(
                        [
                            [sg.Text('B9', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_b8')],
                        ]
                    ),
                    # Button 10 Column
                    sg.Column(
                        [
                            [sg.Text('B10', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_b9')],
                        ]
                    ),
                ],
                [sg.HorizontalSeparator()],
                [sg.Text('Motor Data', size=title_size, font=font)],
                [
                    # Motor 1 Column
                    sg.Column(
                        [
                            [sg.Text('M1', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_m0')],
                        ]
                    ),
                    # Motor 2 Column
                    sg.Column(
                        [
                            [sg.Text('M2', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_m1')],
                        ]
                    ),
                    # Motor 3 Column
                    sg.Column(
                        [
                            [sg.Text('M3', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_m2')],
                        ]
                    ),
                    # Motor 4 Column
                    sg.Column(
                        [
                            [sg.Text('M4', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_m3')],
                        ]
                    ),
                    # Motor 5 Column
                    sg.Column(
                        [
                            [sg.Text('M5', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_m4')],
                        ]
                    ),
                ],
                [
                    # Motor 6 Column
                    sg.Column(
                        [
                            [sg.Text('M6', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_m5')],
                        ]
                    ),
                    # Motor 7 Column
                    sg.Column(
                        [
                            [sg.Text('M7', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_m6')],
                        ]
                    ),
                    # Motor 8 Column
                    sg.Column(
                        [
                            [sg.Text('M8', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_m7')],
                        ]
                    ),
                    # Motor 9 Column
                    sg.Column(
                        [
                            [sg.Text('M9', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_m8')],
                        ]
                    ),
                    # Motor 10 Column
                    sg.Column(
                        [
                            [sg.Text('M10', size=data_label_size, font=font)],
                            [sg.ProgressBar(value=50, size=progress_bar_size, orientation='v', key='controller_m9')],
                        ]
                    ),
                ],
                [sg.HorizontalSeparator()],
            ], size=(320, 1080), element_justification='center'
        )
        
        layout = [
            config_button_column,
            [
                home_config,
                camera_config,
                joystick_config,
                robot_config,
                movement_config,
                sensor_config,
                state_config
            ],
            middle_column,
            data_config
        ]
        
        self.window = sg.Window('KSU Control Panel', layout, size=(1920, 1080), finalize=True)
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
            
            if event == sg.WIN_CLOSED:
                break

if __name__ == '__main__':
    gui = GCS()
    gui.run()