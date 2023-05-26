import numpy as np
from numpysocket import NumpySocket

import yaml

import time
import datetime

import sys
import os

import threading
from threading import Thread
from threading import Queue
import logging

from typing import Any, Optional


class VlanController:
    def __init__(self):
        self.set_config("configs/main.yml")

        self.logger = logging.getLogger("VlanController")
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
            
        self.queues = {}
        
        self.ips = self.config['ips']
        self.ports = self.config['ports']

    def socket_thread(self, thread_id: int, ip: str, port: int):
        self.logger.info(f"Socket thread {thread_id} started")
        self.queues[thread_id] = Queue()
        
        with NumpySocket() as sock:
            with NumpySocket() as dest:
                sock.bind(port)
                self.logger.debug(f"Socket thread {thread_id} bound to {port}")

                while True:
                    sock.listen()
                    
                    with sock.accept() as conn:
                        data = conn.recv()
                        
                        dest, data = self.parse_data(data)
                        
                        dest.connect((ip, port))
                        self.logger.debug(f"Socket thread {thread_id} connected to {ip}:{port}")
                        
                        dest.sendall(data)
                        
    def parse_data(self, data: np.ndarray) -> np.ndarray:
        dest = data[0]
        data = data[1:]
        return dest, data

    def run(self):
        pass
    
    def stop(self):
        pass

    def set_config(self, config: dict):
        with open(config, "r") as f:
            self.config = yaml.safe_load(f)


if __name__ == "__main__":
    vc = VlanController()
    vc.run()