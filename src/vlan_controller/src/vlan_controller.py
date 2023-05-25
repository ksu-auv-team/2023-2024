import numpy as np
from numpysocket import NumpySocket

import yaml

import time
import datetime

import sys
import os

import threading
import logging

from typing import Any, Optional


class VlanController:
    def __init__(self):
        self.set_config("configs/main.yml")

        self.logger = logging.getLogger("VlanController")
        self.logger.info("VlanController initialized")

        if self.config['verbose']:
            self.logger.info("Verbose mode enabled")
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def socket_thread(self, thread_id: int, port: int):
        pass

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