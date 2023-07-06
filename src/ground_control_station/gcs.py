"""
    Ground Control Station (GCS) module.
    Will contain the Graphical Interface code for the GCS.
    calls each of the other modules from the assets folder. 
    (TBD)
"""

import os
import sys
import yaml
import time
import numpy as np
import pandas as pd
import PySimpleGUI as sg
from datetime import datetime
import matplotlib.pyplot as plt

""" 
    Import the modules from the modules folder
    # modules/camera/camera.py -> Camera
    # modules/controller/controller.py -> Controller
"""
from modules.camera.camera import Camera
from modules.controller.controller import Controller


class GCS:
    """
        GCS class. 
        Contains the GUI code for the GCS.
        Calls the modules from the assets folder.
        Input:
            config_file: path to the config file.
            controller: boolean, if True, will initialize the controller module.
            camera: boolean, if True, will initialize the camera module.
        
        Output:
            None

        Needs to Contain:
            - Camera view port (two cameras on toggle button or two tabs)
            - Controller data (buttons, joysticks, etc.)
            - Data logging (to csv file)
            - Data plotting (matplotlib)
            - Data analysis (pandas)
            - Data visualization (matplotlib)
            - Config editing (yaml)
            - Config saving (yaml)
            - Config loading (yaml)
    """
    def create_text_element(self, text, size, font):
        """
            Creates a text element for the GUI.
            Input:
                text: string, text to be displayed.
                size: tuple, size of the text element.
                font: string, font of the text element.
                justification: string, justification of the text element.
            Output:
                text_element: PySimpleGUI text element.
        """
        text_element = sg.Text(text, size=size, font=font)
        return text_element
    
    def create_button_element(self, text, size, font, key):
        """
            Creates a button element for the GUI.
            Input:
                text: string, text to be displayed.
                size: tuple, size of the text element.
                font: string, font of the text element.
                key: string, key of the button element.
            Output:
                button_element: PySimpleGUI button element.
        """
        button_element = sg.Button(text, size=size, font=font, key=key)
        return button_element
    
    def create_input_element(self, size, font, key):
        """
            Creates an input element for the GUI.
            Input:
                size: tuple, size of the text element.
                font: string, font of the text element.
                key: string, key of the button element.
            Output:
                input_element: PySimpleGUI input element.
        """
        input_element = sg.Input(size=size, font=font, key=key)
        return input_element
    
    def create_slider_element(self, size, font, key):
        """
            Creates a slider element for the GUI.
            Input:
                size: tuple, size of the text element.
                font: string, font of the text element.
                key: string, key of the button element.
            Output:
                slider_element: PySimpleGUI slider element.
        """
        slider_element = sg.Slider(size=size, font=font, key=key)
        return slider_element
    
    def create_dropdown_element(self, values, size, font, key):
        """
            Creates a dropdown element for the GUI.
            Input:
                values: list, values of the dropdown element.
                size: tuple, size of the text element.
                font: string, font of the text element.
                key: string, key of the button element.
            Output:
                dropdown_element: PySimpleGUI dropdown element.
        """
        dropdown_element = sg.DropDown(values, size=size, font=font, key=key)
        return dropdown_element
    
    def create_data_view(self, labels, data, size, font, key):
        """
            Creates a data view element for the GUI.
            Input:
                data: list, data to be displayed.
                size: tuple, size of the text element.
                font: string, font of the text element.
                key: string, key of the button element.
            Output:
                data_view_element: PySimpleGUI data view element.
        """
        data_view = sg.Table(values=data, headings=labels, size=size, font=font, key=key)
        return data_view
    
    def __init__(self):
        pass

    
    
    