# This class will be used to implement object detection using YOLO
# will take in feed from the existing camera process and then perform continuous object detection
# will let user know the object is not in the center

class NeuralNetwork:
    def __init__(self):
        pass

    # find the center of the objects bounding box when detected
    def box_center(frame):
        results = model.predict(frame)
        for result in results:
            for box in result.boxes:
                left, top, right, bottom = np.array(box.xyxy.cpu(), dtype=np.int).squeeze()
                center_x = (left + right) // 2
                center_y = (top + bottom) // 2
        return center_x, center_y