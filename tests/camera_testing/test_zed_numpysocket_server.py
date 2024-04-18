#!/usr/bin/python3

import logging

from numpysocket import NumpySocket
import cv2

logger = logging.getLogger("OpenCV server")
logger.setLevel(logging.INFO)

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
    s.bind(("0.0.0.0", 9999))

    while True:
        try:
            s.listen()
            conn, addr = s.accept()

            logger.info(f"connected: {addr}")
            while conn:
                frame = conn.recv()
                if len(frame) == 0:
                    break

                # unsplit the frames into two separate frames
                # frame1 = frame[:240, :]
                # frame2 = frame[240:, :]

                frame1 = maintain_aspect_ratio_resize(frame, width=3840)
                # frame2 = maintain_aspect_ratio_resize(frame2, width=1920)
                cv2.imshow("Frame1", frame1)
                # cv2.imshow("Frame2", frame2)


                # Press Q on keyboard to exit
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    exit(1)
                logger.info(f"disconnected: {addr}")
        except ConnectionResetError:
            pass