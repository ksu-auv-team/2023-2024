import cv2
import yaml
import logging
import numpy as np
from numpysocket import NumpySocket()


def camera_package():
    # Set up logging to file
    logging.basicConfig(filename='../logs/camera_package.log', level=logging.DEBUG)

    # load config file and store
    with open('../assets/configs/camera_config.yml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        
    # set up numpy socket to receive images from one socket and split into two
    with NumpySocket() as n:
        n.connect((config['camera']['ip'], config['camera']['port']))
        while True:
            pass


if __name__ == '__main__':
    camera_package()