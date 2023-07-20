import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

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


so = Networking()
cam = cv2.VideoCapture(0)

so.bind('', 9999)
so.listen(1)
client, _ = so.accept()

while True:
    image = cam.read()[1]
    resize = image_resize(image, width=240)
    client.send_numpy(resize)
    print('sent')
    # cv2.imshow('image', resize)
    # cv2.waitKey(1)