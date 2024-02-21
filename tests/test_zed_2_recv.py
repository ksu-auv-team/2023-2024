from numpysocket import NumpySocket
import cv2

with NumpySocket() as s:
    s.bind(("", 5555))

    while True:
        try:
            s.listen()
            conn, addr = s.accept()

            while conn:
                frames = conn.recv()
                if len(frames) == 0:
                    break
                cv2.imshow("Frame", frames[0])
                cv2.imshow("Frame3", frames[1])

                # Press Q on keyboard to exit
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    exit(1)
        except ConnectionResetError:
            pass