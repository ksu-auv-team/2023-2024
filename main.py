### Everything between these lines is for logging and system information  ###
# _________________________________________________________________________ #

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
def create_logger(filename="logfile"):
    """
    Creates and returns a logging object that writes log messages to a file.
    The filename includes a timestamp in the format "logfile_YYYY-MM-DD_HH-MM-SS.log".

    :return: Logger object configured with a timestamped file handler
    :rtype: logging.Logger
    """
    logger_ = logging.getLogger(__name__)
    logger_.setLevel(logging.INFO)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_handler = logging.FileHandler(f"logs/{filename}_{timestamp}.log")
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
logger.info(f"Python executable: {sys.executable}")

# _________________________________________________________________________ #

### The following is a template comment box for use later ###
# _________________________________________________________________________ #



# _________________________________________________________________________ #

### Regular Camera ### 
# _________________________________________________________________________ #
import cv2
import numpy as np

cam = cv2.VideoCapture(0)

while True:
    _, frame = cam.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break


# _________________________________________________________________________ #

### ZED Camera and Depth Measurements ###
# _________________________________________________________________________ #



# _________________________________________________________________________ #

### Machine Vision ###
# _________________________________________________________________________ #



# _________________________________________________________________________ #

### CNN's ###
# _________________________________________________________________________ #



# _________________________________________________________________________ #

### Hardware Interface ###
# _________________________________________________________________________ #



# _________________________________________________________________________ #

### Ground Control Station ###
# _________________________________________________________________________ #



# _________________________________________________________________________ #

### Main Function ###
# _________________________________________________________________________ #



# _________________________________________________________________________ #