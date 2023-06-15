#!/usr/bin/python3

from numpysocket import NumpySocket
import cv2
import yaml

from typing import int, dict, str, Optional

class CameraUtilities:
    def __init__(self):
        with open('configs/camera_utilities.yaml') as f:
            self.config = yaml.load(f, Loader=yaml.SafeLoader)
        
        cam = self.config['cam']
        res = self.config['res']
        fps = self.config['fps']
        self.dest = self.config['dest']
        self.port = self.config['port']    
        
        if self.config['zed']:
            global sl
            import pyzed.sl as sl
            
            self.zed = sl.Camera()
            
            # Create a InitParameters object and set configuration parameters
            init_params = sl.InitParameters()
            init_params.camera_resolution = sl.RESOLUTION.FHD1080  # Use HD720 video mode (default fps: 60)
            # Use a right-handed Y-up coordinate system
            init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

            # Open the camera
            err = self.zed.open(init_params)
            if err != sl.ERROR_CODE.SUCCESS:
                exit(-1)

            # Create and set RuntimeParameters after opening the camera
            self.runtime_parameters = sl.RuntimeParameters()
            
        else:
            self.cap = cv2.VideoCapture(cam)

            # Set camera frame rate
            self.cap.set(cv2.CAP_PROP_FPS, fps)

    def run(self):
        with NumpySocket() as s:
            s.connect((self.dest, self.port))
            
            image = sl.Mat()
            depth = sl.Mat()
            
            if self.config['zed']:
                while True:
                    if self.zed.grab(self.runtime_parameters) == sl.ERROR_CODE.SUCCESS:
                        # Retrieve left image
                        self.zed.retrieve_image(image, sl.VIEW.LEFT)
                        # Retrieve depth map. Depth is aligned on the left image
                        self.zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
                        
                        image_np = image.get_data()
                        image_np.append(depth.get_data())
                        
                        print(image_np.shape)
                        
                        # try:
                        #     s.sendall(image_np)
                        # except: 
                        #     break
                    else:
                        break
            else:
                while True:
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
