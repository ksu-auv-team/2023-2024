from numpysocket import NumpySocket
import cv2

with NumpySocket() as s:
    s.bind(("", 5555))

    while True:
        try:
            s.listen()
            conn, addr = s.accept()

            while conn:
                frames = []
                for i in range(3):
                    frame = conn.recv()
                    if len(frame) == 0:
                        break
                    frames.append(frame)
                cv2.imshow("Frame", frames[0])
                cv2.imshow("Frame2", frames[1])
                cv2.imshow("Frame3", frames[2])

                # Press Q on keyboard to exit
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    exit(1)
        except ConnectionResetError:
            pass