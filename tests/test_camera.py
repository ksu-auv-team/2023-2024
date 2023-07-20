import sys

sys.path.append('src')

import cv2
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

class cam:
    def __init__(self):
        self.so = Networking()
        self.cam = cv2.VideoCapture(0)

        self.bind()

    def bind(self):
        self.so.bind('10.0.0.34', 9999)
        self.so.listen(1)
        self.client, _ = self.so.accept()

    def send_frame(self, data):
        self.so.send_numpy(data)

    def get_image(self):
        image = self.cam.read()
        resize = image_resize(image, width=240)
        return resize

    def run(self):
        while True:
            frame = self.get_image()
            if frame is not None:
                self.send_frame(frame)
            else:
                print('No frame')
        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == '__main__':
    cam = cam() # type: ignore
    cam.run() # type: ignore