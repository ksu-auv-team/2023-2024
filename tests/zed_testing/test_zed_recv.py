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

def receive_images(queue):
    """
    Function to run in a separate process for receiving images.
    """
    logging.basicConfig(level=logging.INFO)
    receiver = NumpySocket()
    try:
        receiver.bind(('0.0.0.0', 9999))  # Bind to all interfaces on the specified PORT
        receiver.listen(1)
        logging.info("Waiting for connection...")
        conn, addr = receiver.accept()
        logging.info(f"Connection established with {addr}")

        while True:
            combined_np = conn.recv()
            if combined_np.size == 0:
                break  # Break if an empty array is received, indicating end of transmission
            queue.put(combined_np)
    finally:
        receiver.close()

def display_images(queue):
    """
    Function to display images from the queue.
    """
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Depth", cv2.WINDOW_NORMAL)
    while True:
        combined_np = queue.get()
        if combined_np is None:  # Check for the sentinel value to end the display process
            break

        # Separate the combined array back into the image and depth map
        mid_point = combined_np.shape[1] // 2
        image_np = combined_np[:, :mid_point]
        depth_np = combined_np[:, mid_point:]

        # Optionally resize images back to original resolution if needed
        image_np = image_resize(image_np, width=1280, height=720)
        depth_np = image_resize(depth_np, width=1280, height=720)

        # Display the image and depth map
        cv2.imshow("Image", image_np)
        cv2.imshow("Depth", depth_np)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def main():
    logging.basicConfig(level=logging.INFO)

    # Create a multiprocessing Queue
    queue = Queue(maxsize=10)  # Limit the queue size to manage memory usage

    # Start the receiver process
    receiver_process = Process(target=receive_images, args=(queue,))
    receiver_process.start()

    # Start the display process
    display_process = Process(target=display_images, args=(queue,))
    display_process.start()

    # Wait for the processes to complete
    receiver_process.join()
    queue.put(None)  # Send a sentinel value to indicate the end of transmission to the display process
    display_process.join()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
