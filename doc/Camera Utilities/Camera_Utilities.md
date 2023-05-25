# Camera Utilities Package Documentation
## Overview
The Camera Utilities Package is a Python-based utility that captures video frames from a configured camera, resizes the frames, and transmits them to a specified IP address and port. The application runs inside a Docker container, which simplifies the setup and ensures compatibility across different platforms.

## Setup and Installation
1. **Prerequisites:** Ensure Docker is installed on your system. If not, refer to the official Docker [installation guide](https://docs.docker.com/get-docker/).
2. **Clone or download the Camera Utilities package from the repository** and navigate to the project directory.
3. **Build the Docker image** by running the following command in your terminal:
```
docker build -t camera-utilities .
```
This command will create a Docker image named "camera-utilities".

## Configuration
Before running the package, you'll need to configure it via the `config.yml` file:
- `CAM`: The index of the camera to capture video frames from. Generally, 0 is the default for the system's main camera.
- `FPS`: The frames per second at which to capture video.
- `Transmission_Location`: The IP address to send the video frames to.
- `Transmission_Port`: The port to send the video frames to.

Here is an example of a configuration:
```yaml
CAM: 0
FPS: 30
Transmission_Location: "192.168.1.145"
Transmission_Port: 9998
```

## Running the Application
To run the application, execute the following command: (If you recieve )
```
docker run -it --device=/dev/video0 --group-add video camera_utilities:latest
```
This command will start a container with the "camera-utilities" Docker image and launch the `camera_utilities.py` script. 
