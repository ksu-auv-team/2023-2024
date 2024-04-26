import cv2
import numpy as np
import pyzed.sl as sl
import requests

class CameraPackage:
    def __init__(self):
        self.cam = cv2.VideoCapture(2)  # Assuming this is your OpenCV camera
        self.zed = sl.Camera()
        init_params = sl.InitParameters()
        init_params.camera_resolution = sl.RESOLUTION.AUTO
        init_params.camera_fps = 30
        init_params.coordinate_units = sl.UNIT.METER
        init_params.depth_mode = sl.DEPTH_MODE.NEURAL

        if self.zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
            print("Failed to open ZED camera")
            exit(1)

        self.resolution = self.zed.get_camera_information().camera_configuration.resolution
        self.zed_image = sl.Mat(self.resolution.width, self.resolution.height, sl.MAT_TYPE.U8_C4)
        self.zed_depth_image = sl.Mat(self.resolution.width, self.resolution.height, sl.MAT_TYPE.U8_C4)

    def get_frame(self):
        if self.zed.grab() == sl.ERROR_CODE.SUCCESS:
            ret, frame = self.cam.read()
            self.zed.retrieve_image(self.zed_image, sl.VIEW.LEFT)
            self.zed.retrieve_measure(self.zed_depth_image, sl.MEASURE.DEPTH)
            # Encode the ZED image to JPEG format
            zed_image_cv = self.zed_image.get_data()[:, :, :3]
            _, zed_image_encoded = cv2.imencode('.jpg', zed_image_cv)
            # Encode the OpenCV webcam image to JPEG format
            _, frame_encoded = cv2.imencode('.jpg', frame)
            return zed_image_encoded.tobytes(), self.zed_depth_image.get_data(), frame_encoded.tobytes()
        return None, None, None

    def post_frame(self, url):
        zed_image, zed_depth, frame = self.get_frame()
        if zed_image and frame:
            files = {'zed_image': ('zed.jpg', zed_image, 'image/jpeg'),
                     'webcam_image': ('webcam.jpg', frame, 'image/jpeg')}
            response = requests.post(url, files=files)
            return response.text
        return "Failed to capture frames"
