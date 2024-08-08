import cv2
from ultralytics import YOLO
import argparse

class CameraPackage:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.cam = cv2.VideoCapture("http://localhost:5000/video_{camera_id}".format(camera_id=camera_id))
        self.model = YOLO("yolov8n.pt")
    
    def get_frame(self):
        _, frame = self.cam.read()
        return frame
    
    def detect_objects(self, frame):
        results = self.model(frame)
        return results
    
    def __del__(self):
        self.cam.release()
    
    def run(self):
        while True:
            frame = self.get_frame()
            results = self.detect_objects(frame)
            # print(results)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera_id", type=int, default=0)
    args = parser.parse_args()
    camera = CameraPackage(args.camera_id)
    camera.run()