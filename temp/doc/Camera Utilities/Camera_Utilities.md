# Camera Utilities Documentation

## Imports

```python
from numpysocket import NumpySocket
import cv2
import yaml

from typing import int, dict, str, Optional
```
The program uses several Python packages including numpysocket, cv2 (OpenCV), yaml, and typing.

- numpysocket: This is a utility that helps to send and receive numpy arrays over sockets.

- cv2: This is a popular computer vision library.

- yaml: This is a library for parsing YAML files, which are commonly used for configuration.

- typing: This module is used for hinting Python types.

## Class `CameraUtilities`

```python
class CameraUtilities:
```
This is the main class of the program that implements camera utilities.

### Constructor `__init__`

```python
def __init__(self):
```

The constructor reads a configuration file named `camera_utilities.yaml` to initialize a set of parameters including camera device, resolution, fps, destination IP and port number.

If the `zed` parameter in the config file is set to True, the ZED camera is used. The ZED SDK is imported as `sl` and the camera is opened with the specified parameters. If there is an error in opening the camera, the program will exit with status code `-1`.

If the `zed` parameter is not set or is False, a regular OpenCV camera is opened and the fps is set.

### Method `run`

```python
def run(self):
```

The `run` method starts the capture and streaming of video frames. 

A numpy socket is created and connected to the specified destination.

If the `zed` parameter in the config file is set to True, the ZED camera is used to capture stereo images and depth maps. The depth map is then appended to the image array. If there is an error in grabbing the image and depth map, the loop will exit.

If the `zed` parameter is not set or is False, a regular OpenCV camera is used. The captured frames are resized to 320x180 and then sent over the socket. If there is an error in capturing or sending the frame, the loop will exit.

**Note**: The lines to send the images and depth maps over the socket are currently commented out. Uncomment these lines to enable sending the data.