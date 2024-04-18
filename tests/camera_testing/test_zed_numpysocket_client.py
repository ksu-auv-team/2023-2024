#!/usr/bin/python3

from numpysocket import NumpySocket
import cv2

cap = cv2.VideoCapture(2)
cap2 = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Resizes a image and maintains aspect ratio
def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # Grab the image size and initialize dimensions
    dim = None
    (h, w) = image.shape[:2]

    # Return original image if no need to resize
    if width is None and height is None:
        return image

    # We are resizing height if width is none
    if width is None:
        # Calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # We are resizing width if height is none
    else:
        # Calculate the ratio of the width and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # Return the resized image
    return cv2.resize(image, dim, interpolation=inter)

with NumpySocket() as s:
    s.connect(("10.0.0.163", 9999))
    while cap.isOpened():
        ret, frame = cap.read()
        ret2, frame2 = cap2.read()

        # print(frame.shape)

        zed_right = frame[:, 1920:]
        zed_left = frame[:, :1920]

        zed_right_resize = maintain_aspect_ratio_resize(zed_right, width=240)
        zed_left_resize = maintain_aspect_ratio_resize(zed_left, width=240)
        frame2_resize = maintain_aspect_ratio_resize(frame2, width=240)

        frame_resize = cv2.hconcat([zed_left_resize, zed_right_resize, frame2_resize])
        print(frame_resize.shape)

        if ret is True:
            try:
                s.sendall(frame_resize)
            except Exception:
                break
        else:
            break