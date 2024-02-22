import cv2
import numpy as np
from multiprocessing import Process, Queue
import logging
from numpysocket import NumpySocket  # Ensure NumpySocket class is accessible

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

def receive_data(queue, port):
    """
    Function to receive images or depth maps.
    """
    logging.basicConfig(level=logging.INFO)
    receiver = NumpySocket()
    try:
        receiver.bind(('0.0.0.0', port))
        receiver.listen(1)
        logging.info(f"Listening on port {port}...")
        conn, addr = receiver.accept()
        logging.info(f"Connection established with {addr} on port {port}")

        while True:
            data_np = conn.recv()
            if data_np.size == 0:
                break
            queue.put(data_np)
    finally:
        receiver.close()

def display_image(queue_image):
    """
    Function to display images from the queue.
    """
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    while True:
        image_np = queue_image.get()
        image_np = image_resize(image_np, width=640, height=360)
        if image_np is None:  # Check for the sentinel value to end the display process
            break
        cv2.imshow("Image", image_np)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def display_depth(queue_depth):
    """
    Function to display depth maps from the queue.
    """
    cv2.namedWindow("Depth", cv2.WINDOW_NORMAL)
    while True:
        depth_np = queue_depth.get()
        depth_np = image_resize(depth_np, width=640, height=360)
        if depth_np is None:  # Check for the sentinel value to end the display process
            break
        # Convert depth to a visible format if necessary
        depth_display = cv2.convertScaleAbs(depth_np, alpha=0.03)  # Example conversion for visualization
        cv2.imshow("Depth", depth_display)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def main():
    # Queues for images and depth maps
    queue_image = Queue(maxsize=10)
    queue_depth = Queue(maxsize=10)

    # Ports for images and depth maps
    image_port = 9998
    depth_port = 9999

    # Start receiver processes for images and depth maps
    receiver_process_image = Process(target=receive_data, args=(queue_image, image_port))
    receiver_process_depth = Process(target=receive_data, args=(queue_depth, depth_port))
    receiver_process_image.start()
    receiver_process_depth.start()

    # Start display processes for images and depth maps
    display_process_image = Process(target=display_image, args=(queue_image,))
    display_process_depth = Process(target=display_depth, args=(queue_depth,))
    display_process_image.start()
    display_process_depth.start()

    # Wait for receiver processes to complete
    receiver_process_image.join()
    receiver_process_depth.join()

if __name__ == "__main__":
    main()
