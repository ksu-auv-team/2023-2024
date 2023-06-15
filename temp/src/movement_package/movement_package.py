import numpy as np
from numpysocket import NumpySocket

import os
import sys

import logging
from datetime import datetime

import yaml


class MovementPackage:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.filename = f'../../logs/{datetime.now().strftime("%Y%m%d_%H%M%S")}/movement_package.log'
        self.logger.setLevel(logging.DEBUG)
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        ch.setFormatter(formatter)
        
        self.logger.addHandler(ch)
        
        self.logger.info("Movement Package initialized")
        self.logger.info("Loading config file")
        
        with open('../../configs/movement_config.yaml', 'r') as stream:
            try:
                self.config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                self.logger.error(exc)
                
        self.logger.info("Config file loaded")
        
    def parse_data(self, data):
        motors = data[0:8]
        servos = data[8:12]
        
        return motors, servos    
    
    def run_AUV(self):
        self.logger.info("Initializing numpy socket")
        with NumpySocket() as nps:
            nps.bind((self.config['AUV_IP'], self.config['AUV_PORT']))
            
            nps.listen()
            
            conn, addr = nps.accept()
            with conn:
                self.logger.info('Connected by', addr)
                
                while True:
                    self.data = conn.recv()
                    
                    motors, servos = self.parse_data(self.data)
                    
                    self.logger.info(f'Motors: {motors} Servos: {servos}')
                    
    def run_ROV(self):
        self.logger.info("Initializing numpy socket")
        with NumpySocket() as nps:
            nps.connect((self.config['ROV_IP'], self.config['ROV_PORT']))
            
            nps.listen()
            
            conn, addr = nps.accept()
            with conn:
                self.logger.info('Connected by', addr)
                
                while True:
                    self.data = conn.recv()
                    
                    motors, servos = self.parse_data(self.data)
                    
                    self.logger.info(f'Motors: {motors} Servos: {servos}')