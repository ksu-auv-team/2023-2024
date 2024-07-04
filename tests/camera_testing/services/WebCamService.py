#WebCamService.py
import cv2


class WebCam:
    
    #giving attributes so each camera has a number and ip making it easier to call across different files
    def __init__(self, ip=None, camera_number=None):
        self.ip = ip
        self.camera_number = camera_number
        self.capture = None

    def get_frame(self, capture):
        while True:
            hasFrame, frame = capture.read()

            if not hasFrame:
                raise Exception("Camera frame not obtained")

            _, jpeg = cv2.imencode('.jpg', frame)
            
            return jpeg.tobytes()
