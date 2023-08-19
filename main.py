# Import necessary libraries
import os
import sys
import logging
import datetime
import platform
import yaml

# Detect OS platform
system_os = platform.system()

# Dependent on OS, toggle os type flag
if system_os == "Windows":
    os_type = "windows"
elif system_os == "Linux":
    os_type = "linux"
elif system_os == "Darwin":
    os_type = "mac"
else:
    print("Unsupported OS")
    sys.exit()

# Configure config file path
config_file_path = os.path.join(os.path.dirname(__file__), "configs/main.yml")
with open(config_file_path, mode="r", encoding="utf-8") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)


# Configure log file path
def create_logger():
    """
    Creates and returns a logging object that writes log messages to a file.
    The filename includes a timestamp in the format "logfile_YYYY-MM-DD_HH-MM-SS.log".

    :return: Logger object configured with a timestamped file handler
    :rtype: logging.Logger
    """
    logger_ = logging.getLogger(__name__)
    logger_.setLevel(logging.INFO)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_handler = logging.FileHandler(f"logs/logfile_{timestamp}.log")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger_.addHandler(file_handler)
    return logger_


# Create a logger object
logger = create_logger()
logger.info("Logger created")

# Log system information
logger.info(f'Date: {datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
logger.info(f"OS: {os_type}")
logger.info(f"Python version: {sys.version}")

# depending on config file [debug] flag, toggle debug flag
if config["debug"]:
    debug = True
else:
    debug = False

# Log debug flag
logger.info(f"Debug: {debug}")

# depending on config file [train] flag, toggle train flag
if config["train"]:
    train = True
else:
    train = False

# Log train flag
logger.info(f"Train: {train}")

# Import necessary libraries
import cv2
import numpy as np


# Define regular camera class
class RegCamera:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, config["camera"]["width"])
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, config["camera"]["height"])
        self.cam.set(cv2.CAP_PROP_FPS, config["camera"]["fps"])

    def get_frame(self):
        _, frame = self.cam.read()
        return frame

    def image_resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

    def release(self):
        self.cam.release()
