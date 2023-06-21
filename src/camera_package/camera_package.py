import os
import sys
import cv2
import yaml
import numpy as np
from threading import Thread
from numpysocket import NumpySocket

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

HOME = os.getcwd()
print(HOME)

with open(HOME + '/src/camera_package/configs/camera_package.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

ip = config['ip']
port = config['port']
send_width = config['send_width']
fps = config['fps']

class camera_package:
    def __init__(self):
        self.run()
    
    def thread(self, conn, addr, cam):
        print(conn, addr)
        camera = cv2.VideoCapture(cam)
        with NumpySocket() as s:
            try:
                while conn:
                    frame = camera.read()
                    image = image_resize(frame, width=send_width)
                    s.sendall(image)
            except:
                sys.exit(0)
    
    def run(self):
        with NumpySocket() as s:
            s.bind((ip, port))
            addr_list = []
            connections = []
            while True:
                try:
                    s.listen()
                    conn, addr = s.accept()
                    
                    # This while loop will run until the connection sends a message indicating which camera to use
                    while conn:
                        mess = conn.recv(1024)
                        if mess == b'0':
                            cam = 0
                            break
                        else:
                            cam = 1
                            break
                    
                    if addr not in addr_list:
                        addr_list.append(addr)
                        connections.append(Thread(target=self.thread, args=(conn, addr, cam)))
                        connections[-1].start()
                except:
                    for conn in connections:
                        conn.join()
                    break
                
if __name__ == '__main__':
    camera_package()