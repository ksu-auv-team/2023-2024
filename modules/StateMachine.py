from statemachine import StateMachine, State
from statemachine.contrib.diagram import DotGraphMachine

import json
import logging
import requests

# Import the necessary modules from the statemachine_modules folder

class AUVStateMachine(StateMachine):
    pass

if __name__ == '__main__':
    m = AUVStateMachine()
    graph = DotGraphMachine(m)
    dot = graph()
    dot.write_png('static/docs/pngs/AUVStateMachine.png')


#this works with just printing how it needs to be adjust
#possibly replace with the motor adjustments?
def frames(cNum):  
    while True:
        if cNum == 0:
            success, frame = camera_0.read()
            print("Zed camera:")
        else:
            #will have 2nd ip after testing 2nd camera
            #success, frame = camera_1.read()
            print("2nd Webcam:")
            break
        if not success:
            break
        else:
            center_x , center_y = box_center(frame)
            # 240x320 is half the dimension of the cameras tested
            # adjust these values depending on your cameras resolution
            adjust_camera(center_x, center_y, 240, 320)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# find the center of the objects bounding box when detected
def box_center(frame):
    results = model.predict(frame)
    for result in results:
        for box in result.boxes:
            left, top, right, bottom = np.array(box.xyxy.cpu(), dtype=np.int).squeeze()
            center_x = (left + right) // 2
            center_y = (top + bottom) // 2
    return center_x, center_y