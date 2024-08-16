import cv2


class WebCam:
    '''webcam class has ip and camera number attributes so the cameras can exist
    across multiple files'''
    def __init__(self, ip=None, camera_number=None):
        self.ip = ip
        self.camera_number = camera_number
        self.capture = None

    def get_frame(self, capture):
        while True:
            hasFrame, frame = capture.read()
            if (self.camera_number == 0):
                frame = self.crop_frame(frame)
            if not hasFrame:
                raise Exception("Camera frame not obtained")

            _, jpeg = cv2.imencode('.jpg', frame)
            
            return jpeg.tobytes()

    def crop_frame(self, frame):
        # Get the dimensions of the frame
        try:
            height, width, _ = frame.shape
            # Crop the right half of the frame
            cropped_frame = frame[:, width // 2:]
            
            return cropped_frame
        except AttributeError as e:
            print('None frame')
            return None