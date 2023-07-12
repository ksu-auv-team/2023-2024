import cv2
import numpy as np

from src.modules.networking.networking import Networking

# https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

class Regular:
    def __init__(self, host, port, camera_id):
        self.host = host
        self.port = port
        try:
            self.cam = cv2.VideoCapture(camera_id)  # Open the camera with specified camera_id
        except Exception as e:
            print("Error initializing camera: ", e)
        self.connect()

    def connect(self):
        try:
            # Create a networking socket
            self.np_socket = Networking()
            # Bind the socket to host and port
            self.np_socket.bind((self.host, self.port))
            # Start listening for incoming connections
            self.np_socket.listen(1)
            # Accept the client connection
            self.client, _ = self.np_socket.accept()
            print('Client connected')
        except Exception as e:
            print("Error in connect: ", e)

    def send_frame(self):
        try:
            # Read a frame from the camera
            ret, frame = self.cam.read()
            if not ret:
                print("Failed to get frame")
                return
            # Resize the frame to lower the data to be sent
            frame = image_resize(frame, width=480)
            # Ensure the datatype
            frame = np.array(frame, dtype='uint8')
            # Send the frame to the client as a numpy array
            self.client.send_numpy(frame)
        except Exception as e:
            print("Error in send_frame: ", e)

    def close(self):
        try:
            # Close the client connection
            self.client.close()
            # Close the server socket
            self.np_socket.close()
            # Release the camera
            self.cam.release()
        except Exception as e:
            print("Error in close: ", e)

    def run(self):
        try:
            # Continuously read frames from the camera and send them to the client
            while True:
                self.send_frame()
        except KeyboardInterrupt:
            print("Interrupted")
        finally:
            # Gracefully close the resources when done
            self.close()

# Run the camera as a standalone application for debugging purposes
if __name__ == '__main__':
    try:
        # Create the Regular object and start sending frames
        camera = Regular('192.168.1.246', 9999, 0)
        camera.run()
    except Exception as e:
        print("Error in main: ", e)