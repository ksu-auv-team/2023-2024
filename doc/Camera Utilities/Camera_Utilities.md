# `CameraUtilities` Class Documentation

## Import Libraries

- `numpysocket`: This library allows you to send numpy arrays over a socket connection.
- `cv2`: OpenCV is a library used for real-time computer vision.
- `yaml`: This module provides methods to parse YAML syntax and convert them to Python objects.
- `typing`: A standard Python library used for type hinting.

## `CameraUtilities` class

The `CameraUtilities` class captures video from a specified camera, resizes the frames, and sends them as numpy arrays over a socket connection.

### Class Initialization

```python
class CameraUtilities:
    def __init__(self, cam: int, fps:int = 30, dest: str = 'localhost', port: int = 9996):
        self.cap = cv2.VideoCapture(cam)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.dest = dest        
        self.port = port
```
#### Parameters:

- `cam`: Integer value specifying which camera to use. In OpenCV, 0 usually refers to the default camera.
- `fps`: (Optional) Desired frame rate for the camera capture. Default is 30.
- `dest`: (Optional) Destination hostname to which the numpy arrays are sent. Default is 'localhost'.
- `port`: (Optional) Port number for the connection. Default is 9996.

### `run` Method

```python
def run(self):
    with NumpySocket() as s:
        s.connect((self.dest, self.port))
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            frame_resize = cv2.resize(frame, (320, 180))
            if ret is True:
                try:
                    s.sendall(frame_resize)
                except:
                    break
            else:
                break
```

The `run` method starts the video capture, resizes the frames, and sends them as numpy arrays over a socket connection. If any error occurs during the frame sending, the loop breaks and the method ends.

## Example Usage:

```python
# Initialize CameraUtilities object for default camera, with a frame rate of 30, sending frames to localhost on port 9996
cam_util = CameraUtilities(cam=0, fps=30, dest='localhost', port=9996)

# Run the video capture and frame sending
cam_util.run()
```

## Note

Although this class provides an easy way to capture video from a camera and send the frames as numpy arrays over a network, it currently lacks comprehensive error handling and logging, which would be necessary for a more robust, production-ready implementation.