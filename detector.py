"""
This module is responsible for detecting vehicles in specific frames.
Using YOLO, we can detect cars, motorbikes, trucks, bicycles and buses.
"""
from typing import List, Any

import cv2


class Detector:
    """
    Wrapper for ML.
    Detects relevant object in a certain frame or a video.
    The relevant object are vehicles such as cars, buses, trucks, bicycles and motorbikes.
    This class may be extended to a self made model (not YOLO).
    :param `height`: Height of the current image.
    :type height: int
    :param `width`: Width of the current image.
    :type width: int
    :cvar `NET_INPUT_SIZE`: Size (width and height) of the net's input image.
    :type NET_INPUT_SIZE: int
    :param `min_confidence`: Minimum probability to filter weak detections.
    :type min_confidence: float
    :param `threshold`: Threshold for non-maxima suppression.
    :type threshold: float
    :param `COLORS`: Contains the color for each class (label).
    :type COLORS: list<tuple(int, int, int)>
    :param `LABELS`: Contains the labels of the classes that can be detected.
    :type LABELS: list<str>
    :param `boxes`: A list of the bounding boxes of the objects detected.
    :type boxes: Depends on the implementation.
    :param `confidences`: A list of the confidences of each object detected.
    :type confidences: list<float>
    :param `classIDs`: A list of the classes of the objects detected.
    :type classIDs: list<int>
    """

    height = 0
    width = 0
    NET_INPUT_SIZE = 416

    min_confidence = 0
    threshold = 0
    COLORS = None
    LABELS = None

    # Results of predictions
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

    def put_bounding_box(self, index, frame, dist):
        # extract the bounding box coordinates
        (x, y) = (self.boxes[index][0], self.boxes[index][1])
        (w, h) = (self.boxes[index][2], self.boxes[index][3])

        # Get the color of the label detected
        color = [0, 0, 255]
        # Create a rectangle according to the bounding box's coordinates
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)
        # Creating a text with the class of the prediction and its confidence
        #text = "{}: {:.4f}".format(self.LABELS[self.classIDs[index]], self.confidences[index])
        text = str('%.3f' % dist)
        # Putting the text to display
        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        return frame
