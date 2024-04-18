#!/usr/bin/python3

from numpysocket import NumpySocket
import cv2

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(3)

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
        # ref_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_resize = maintain_aspect_ratio_resize(frame, width=240)
        frame_resize2 = maintain_aspect_ratio_resize(frame2, width=240)

        # add the two frames together
        frame_resize = cv2.hconcat([frame_resize, frame_resize2])

        if ret is True:
            try:
                s.sendall(frame_resize)
            except Exception:
                break
        else:
            break