
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
    
# Create the GUI layout and supporting variables
title_size = (20, 1)
data_label_size = (15, 1)
data_size = (10, 1)
text_input_size = (25, 1)
battery_label_size = (20, 1)
battery_size = (5, 1)
font_size = 20
font = ("Arial", font_size)
placeholder_image = 'images/placeholder.png'
camera_feed_size = (1280, 720)
progress_bar_size = (15, 10)
button_size = (15, 1)
val = 100

# Some helper functions for the GUI layout
def create_text_data_pair(text, data, key):
    """Generate a row with a text label and data label

    Args:
        text (string): Data label text to be displayed
        data (string): Data to be displayed
    """
    return [sg.Text(text, size=data_label_size, font=font, justification='left'), sg.Text(data, size=data_size, font=font, justification='left', key=key)]

def create_battery_status(i):
    return sg.Column(
        [
            [
                sg.Text('Battery ' + i + ' Voltage: ', size=battery_label_size, font=font, justification='left'), 
                sg.Text('0', size=battery_size, font=font, justification='left', key='battery_' + i + '_voltage'),
                sg.Text('V', size=battery_size, font=font, justification='left')
            ],
            [
                sg.Text('Battery ' + i + ' Current: ', size=battery_label_size, font=font, justification='left'), 
                sg.Text('0', size=battery_size, font=font, justification='left', key='battery_' + i + '_current'),
                sg.Text('A', size=battery_size, font=font, justification='left')
            ],
        ]
    )

# Main class
class GCS:
    def __init__(self):
        # Create the log folder
        date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        os.mkdir(f'logs/{date}')
        
        # Create the logger which outputs a log file to the log folder that was just created
        logging.basicConfig(filename=f'src/ground_control_station/logs/{date}/gcs.log', level=logging.DEBUG)
        
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
        with open('src/ground_control_station/configs/gcs.yml', 'r') as file:
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
        
        # Set the theme for the GUI
        sg.theme('DarkAmber')
        
        self.joystick_list = []
        
        # Create the right column layout (configuration panel)
        # Home panel layout (GCS)
        tabbed_panel_1 = [
            [sg.Text('Home', size=title_size, font=font, justification='center')],
            [sg.HorizontalSeparator()],
            
        ]
        # Camera panel layout (camera_package)
        tabbed_panel_2 = [
            [sg.Text('Camera', size=title_size, font=font, justification='center')],
            [sg.HorizontalSeparator()],
            [sg.Text('Camera Feed 1 Configuration', size=data_label_size, font=font, justification='left')],
            [sg.HorizontalSeparator()],
            [sg.Text('IP Address: ', size=data_label_size, font=font, justification='left'), sg.InputText('', size=text_input_size, font=font, justification='left', key='camera_feed_1_ip_address')],
            [sg.Text('Port: ', size=data_label_size, font=font, justification='left'), sg.InputText('', size=text_input_size, font=font, justification='left', key='camera_feed_1_port')],
            [sg.Text('Size: ', size=data_label_size, font=font, justification='left'), sg.InputText('', size=text_input_size, font=font, justification='left', key='camera_feed_1_size')],
            [sg.Text('FPS: ', size=data_label_size, font=font, justification='left'), sg.InputText('', size=text_input_size, font=font, justification='left', key='camera_feed_1_fps')],
            [sg.Text('Camera Feed 2 Configuration', size=data_label_size, font=font, justification='left')],
            [sg.Text('IP Address: ', size=data_label_size, font=font, justification='left'), sg.InputText('', size=text_input_size, font=font, justification='left', key='camera_feed_2_ip_address')],
            [sg.Text('Port: ', size=data_label_size, font=font, justification='left'), sg.InputText('', size=text_input_size, font=font, justification='left', key='camera_feed_2_port')],
            [sg.Text('Size: ', size=data_label_size, font=font, justification='left'), sg.InputText('', size=text_input_size, font=font, justification='left', key='camera_feed_2_size')],
            [sg.Text('FPS: ', size=data_label_size, font=font, justification='left'), sg.InputText('', size=text_input_size, font=font, justification='left', key='camera_feed_2_fps')],
            [sg.HorizontalSeparator()],
            [sg.Button('Start Camera Feed 1', size=button_size, font=font, key='start_camera_feed_1', button_color=('white', 'red'))],
            [sg.Button('Start Camera Feed 2', size=button_size, font=font, key='start_camera_feed_2', button_color=('white', 'red'))],
        ]
        # Joystick panel layout (joystick_package)
        tabbed_panel_3 = [
            [sg.Text('Joystick', size=title_size, font=font, justification='center')],
            [sg.HorizontalSeparator()],
            [sg.RadioButton('Internal Joystick', 'joystick', default=True, size=button_size, font=font, key='internal_joystick')]
            [sg.RadioButton('External Joystick', 'joystick', size=button_size, font=font, key='external_joystick')],
            [sg.Text('Axis Configuration', size=data_label_size, font=font, justification='left')],
            [sg.HorizontalSeparator()],
            [sg.Text('X Deadzone: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='x_axis')],
            [sg.Text('Y Deadzone: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='y_axis')],
            [sg.Text('Z Deadzone: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='z_axis')],
            [sg.Text('Throttle Deadzone: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='throttle_axis')],
            [sg.Text('Accelerator Deadzone: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='hat_switch')],
            [sg.Text('Button Configuration', size=data_label_size, font=font, justification='left')],
            [sg.HorizontalSeparator()],
            [sg.Text('Button 1: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='button_1')],
            [sg.Text('Button 2: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='button_2')],
            [sg.Text('Button 3: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='button_3')],
            [sg.Text('Button 4: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='button_4')],
            [sg.Text('Button 5: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='button_5')],
            [sg.Text('Button 6: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='button_6')],
            [sg.Text('Button 7: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='button_7')],
            [sg.Text('Button 8: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='button_8')],
            [sg.Text('Button 9: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='button_9')],
            [sg.Text('Button 10: ', size=data_label_size, font=font, justification='left'), sg.InputText('0', size=text_input_size, font=font, justification='left', key='button_10')],
        ]
        # Machine Vision panel layout (machine_vision_package)
        tabbed_panel_4 = [
            [sg.Text('Machine Vision', size=title_size, font=font, justification='center')],
            [sg.HorizontalSeparator()],
        ]
        # Movement panel layout (movement_package)
        tabbed_panel_5 = [
            [sg.Text('Movement Package', size=title_size, font=font, justification='center')],
            [sg.HorizontalSeparator()],
        ]
        # Sensor panel layout (sensor_package)
        tabbed_panel_6 = [
            [sg.Text('Sensor Package', size=title_size, font=font, justification='center')],
            [sg.HorizontalSeparator()],
        ]
        # State panel layout (state_package)
        tabbed_panel_7 = [
            [sg.Text('State Machine', size=title_size, font=font, justification='center')],
            [sg.HorizontalSeparator()],
        ]
        # Data panel layout (data_package)
        tabbed_panel_8 = [
            [sg.Text('Data: ', size=title_size, font=font, justification='center')],
            [sg.HorizontalSeparator()],
            [sg.Text('Time: ', size=data_label_size, font=font, justification='left'), sg.Text('0', size=data_size, font=font, justification='left', key='time')],
            create_text_data_pair('Motor 1: ', '0', key='motor_0'),
            create_text_data_pair('Motor 2: ', '0', key='motor_1'),
            create_text_data_pair('Motor 3: ', '0', key='motor_2'),
            create_text_data_pair('Motor 4: ', '0', key='motor_3'),
            create_text_data_pair('Motor 5: ', '0', key='motor_4'),
            create_text_data_pair('Motor 6: ', '0', key='motor_5'),
            create_text_data_pair('Motor 7: ', '0', key='motor_6'),
            create_text_data_pair('Motor 8: ', '0', key='motor_7'),
            [sg.HorizontalSeparator()],
            create_text_data_pair('Servo 1: ', '0', key='servo_0'),
            create_text_data_pair('Servo 2: ', '0', key='servo_1'),
            [sg.HorizontalSeparator()],
            create_text_data_pair('X: ', '0', key='imu_x'),
            create_text_data_pair('Y: ', '0', key='imu_y'),
            create_text_data_pair('Z: ', '0', key='imu_z'),
            [sg.HorizontalSeparator()],
            create_text_data_pair('Latitude: ', '0', key='latitude'),
            create_text_data_pair('Longitude: ', '0', key='longitude'),
            create_text_data_pair('Altitude: ', '0', key='altitude'),
            [sg.HorizontalSeparator()],
            create_text_data_pair('Temperature: ', '0', key='temperature'),
            [sg.HorizontalSeparator()],
            create_text_data_pair('Humidity: ', '0', key='humidity'),
            [sg.HorizontalSeparator()],
        ]
        # Left column layout = tabbed panel
        left_column = [
            [
                sg.TabGroup(
                    [
                        [sg.Tab('Home', tabbed_panel_1, key='home_config')],
                        [sg.Tab('Cam', tabbed_panel_2, key='camera_config')],
                        [sg.Tab('Joy', tabbed_panel_3, key='joystick_config')],
                        [sg.Tab('MV', tabbed_panel_4, key='robot_config')],
                        [sg.Tab('MP', tabbed_panel_5, key='movement_config')],
                        [sg.Tab('SP', tabbed_panel_6, key='sensor_config')],
                        [sg.Tab('SM', tabbed_panel_7, key='state_config')],
                        [sg.Tab('Data', tabbed_panel_8, key='data_config')]
                    ], tab_location='left', size=(600, 1080), key='tabbed_panel'
                )
            ]
        ]
        
        # Middle column layout = camera feed and battery status' and start/stop/kill buttons (these are also physical buttons on the GCS)
        middle_column = [
            [sg.Image(placeholder_image, size=camera_feed_size, key='camera_feed')],
            [sg.HorizontalSeparator()],
            [
                sg.VerticalSeparator(),
                create_battery_status('1'),
                sg.VerticalSeparator(),
                create_battery_status('2'),
            ],
            [sg.HorizontalSeparator()],
            [
                sg.VerticalSeparator(),
                create_battery_status('3'),
                sg.VerticalSeparator(),
                create_battery_status('4'),
            ],
            [sg.HorizontalSeparator()],
            [
                sg.Button('Start', size=button_size, font=font, key='start_button', button_color=('white', 'green')), 
                sg.Button('Stop', size=button_size, font=font, key='stop_button', button_color=('white', 'orange')), 
                sg.Button('Kill', size=button_size, font=font, key='kill_button', button_color=('white', 'red'))
            ],
        ]
        
        # Create the main layout
        window_layout = [
            [sg.Text('KSU Control Panel', size=title_size, font=font, justification='center')],
            [sg.HorizontalSeparator()],
            [
                sg.Column(
                    left_column, element_justification='left', size=(600, 1080)
                ),
                sg.Column(
                    middle_column, element_justification='center', size=(1280, 1080), key='middle_column'
                )
            ]
        ]    
        
        self.window = sg.Window('KSU Control Panel', window_layout, size=(1920, 1080), finalize=True)
        self.window.Maximize()
    
    # Query and store the connected joystick devices
    def get_joystick_devices(self):
        pass
    
    def ping_orin(self):
        pass
    
    def ssh_orin(self):
        pass
    
    def controller_input(self):
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