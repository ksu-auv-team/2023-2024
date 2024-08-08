import cv2
import argparse

class recorder:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.cam = cv2.VideoCapture("http://192.168.1.246:5000/video_{camera_id}".format(camera_id=camera_id))

    def setup(self):
        frame_width = int(self.cam.get(3)) 
        frame_height = int(self.cam.get(4)) 
   
        size = (frame_width, frame_height) 

        self.result = cv2.VideoWriter('path/media/user/7000-8000/AUV/recording'+str(self.camera_id)'.mp4',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         30, size) 
    def run(self):
        while(True): 
            ret, frame = self.cam.read() 
        
            if ret == True:  
        
                # Write the frame into the 
                # file 'filename.avi' 
                self.result.write(frame) 
        
                # # Display the frame 
                # # saved in the file 
                # cv2.imshow('Frame', frame) 
        
                # # Press S on keyboard  
                # # to stop the process 
                # if cv2.waitKey(1) & 0xFF == ord('s'): 
                #     break
        
            # Break the loop 
            else: 
                break
        
        # When everything done, release  
        # the video capture and video  
        # write objects 
        self.cam.release() 
        self.result.release() 
            
        # Closes all the frames 
        cv2.destroyAllWindows() 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera_id", type=int, default=0)
    args = parser.parse_args()
    recorder = recorder(args.camera_id)
    recorder.setup()
    recorder.run()