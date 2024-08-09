import cv2
from ultralytics import YOLO
import argparse
import numpy as np

class CameraPackage:
    #initializes camera
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.cam = cv2.VideoCapture("http://localhost:5000/video_{camera_id}".format(camera_id=camera_id))
        self.model = YOLO("yolov8n.pt")

    def adjust_camera(center_x, center_y, frame_center_x, frame_center_y):
        centered_x = False
        centered_y = False

        # tolerance used to represent room for error
        # decrease to make function less lenient, increase to make more lenient
        tolerance = 40
        if center_x < frame_center_x - tolerance:
            print("Move camera to the left")
        elif center_x > frame_center_x + tolerance:
            print("Move camera to the right")
        else:
            centered_x = True
        
        if center_y < frame_center_y - tolerance:
            print("Move camera up")
        elif center_y > frame_center_y + tolerance:
            print("Move camera down")
        else:
            centered_y = True
        
        if((centered_x == True) and (centered_y == True)):
            print("Object is centered")
    
    #is returning the frames based off the URL passed in
    def frames(self, cNum):  
        while True:
            if cNum == 0:
                success, frame = self.cam
                print("Zed camera:")
            else:
                #will have 2nd ip after testing 2nd camera
                #success, frame = camera_1.read()
                print("2nd Webcam:")
            if not success:
                break
            else:
                center_x , center_y = self.box_center(frame)
                # 240x320 is half the dimension of the cameras tested
                # adjust these values depending on your cameras resolution
                self.adjust_camera(center_x, center_y, 240, 320)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


    # find the center of the objects bounding box when detected
    def box_center(self, frame):
        results = self.model.predict(frame)
        for result in results:
            for box in result.boxes:
                left, top, right, bottom = np.array(box.xyxy.cpu(), dtype=np.int).squeeze()
                center_x = (left + right) // 2
                center_y = (top + bottom) // 2
        return center_x, center_y



    
    
    def __del__(self):
        self.cam.release()
    
    def run(self):
        while True:
            #continously gets the camera frames, performs object detection on them
            #prints the results of the object detection
            frame = self.frames()
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