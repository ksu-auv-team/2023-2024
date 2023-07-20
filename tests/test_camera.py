import cv2
import numpy as np
from src.modules.networking import Networking


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

class WebcamClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = Networking()

    def start(self):
        # Connect to the server
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to the server at {self.host}:{self.port}")

        while True:
            # Receive a frame
            frame = self.client_socket.recv_numpy()
            frame = image_resize(frame, width=1920)

            # Display the frame
            cv2.imshow("Webcam", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Close the window and the socket when done
        cv2.destroyAllWindows()
        self.client_socket.close()

if __name__ == "__main__":
    HOST = '10.0.0.34'  # or the server IP
    PORT = 9999  # or the server port

    client = WebcamClient(HOST, PORT)
    client.start()
