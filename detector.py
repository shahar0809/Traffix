"""
This module is responsible for detecting vehicles in specific frames.
Using YOLO, we can detect cars, motorbikes, trucks, bicycles and buses.
"""
import cv2


class Detector:
    """
    Detects relevant object in a certain frame or a video.
    The relevant object are vehicles such as cars, buses, trucks, bicycles and motorbikes.
    This class may be extended to a self made model (not YOLO).
    :param `_path`: The path of the input video
    :type _path: str
    :param `_output_name`: The name of the output video that contains detections
    :type _output_name: str
    """

    height = 0
    width = 0
    NET_INPUT_SIZE = 416

    min_confidence = 0
    threshold = 0
    COLORS = None
    LABELS = None

    # Results of predictions
    boxes = []
    confidences = []
    classIDs = []

    def __init__(self, threshold, min_confidence):
        """
        Initializes the detector with the input and output paths.
        :param `threshold`: Threshold when applying non-maxima suppression
        :type threshold: float
        :param `min_confidence`: Minimum probability to filter weak detections
        :type min_confidence: float
        :return:
        """
        self.threshold = threshold
        self.min_confidence = min_confidence

    def detect_objects(self, frame):
        raise NotImplementedError

    def put_bounding_box(self, index, frame):
        # extract the bounding box coordinates
        (x, y) = (self.boxes[index][0], self.boxes[index][1])
        (w, h) = (self.boxes[index][2], self.boxes[index][3])

        # Get the color of the label detected
        color = [int(c) for c in self.COLORS[self.classIDs[index]]]
        # Create a rectangle according to the bounding box's coordinates
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        # Creating a text with the class of the prediction and its confidence
        text = "{}: {:.4f}".format(self.LABELS[self.classIDs[index]], self.confidences[index])
        # Putting the text to display
        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return frame
