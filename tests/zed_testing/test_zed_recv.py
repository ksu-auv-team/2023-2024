# Import necessary libraries
import cv2
import logging
from NumpySocket import NumpySocket  # Ensure NumpySocket class is accessible

def main():
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Initialize NumpySocket for receiving
    receiver = NumpySocket()
    receiver.bind(('0.0.0.0', PORT))  # Bind to all interfaces on the PORT
    receiver.listen(1)
    logging.info("Waiting for connection...")
    conn, addr = receiver.accept()
    logging.info("Connection from: " + str(addr))

    while True:
        try:
            # Receive image and depth map
            image_np = conn.recv()
            depth_np = conn.recv()

            if image_np.size == 0 or depth_np.size == 0:
                break  # Break if empty frame received

            # Display received image and depth map
            cv2.imshow("Received Image", image_np)
            cv2.imshow("Received Depth", depth_np)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
        except Exception as e:
            logging.error("Receiving error: " + str(e))
            break

    # Cleanup
    conn.close()
    receiver.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
