import cv2
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

class Regular:
    def __init__(self, host, port, camera_id):
        self.host = host
        self.port = port
        self.camera_id = camera_id
        self.cam = cv2.VideoCapture(self.camera_id)
        self.server_socket = Networking()

    def start(self):
        # Start the server
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server started at {self.host}:{self.port}")

        print("Waiting for a connection...")
        self.client_socket, addr = self.server_socket.accept()
        print(f"Client connected from {addr}")

        try:
            while True:
                # Capture a frame
                ret, frame = self.cam.read()
                frame = image_resize(frame, width=360)

                if not ret:
                    print("Failed to capture frame")
                    break

                # Send the frame
                self.client_socket.send_numpy(frame)
        except Exception as e:
            print(e)

            # Release the webcam and close the socket when done
            self.cam.release()
            self.client_socket.close()
            self.server_socket.close()

if __name__ == "__main__":
    HOST = '10.0.0.34'  # or your IP
    PORT = 9999  # or your port
    CAMERA_ID = 0  # or your camera id

    server = Regular(HOST, PORT, CAMERA_ID)
    server.start()
