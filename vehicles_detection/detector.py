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

    def __init__(self, threshold, min_confidence, tracker):
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
        self.tracker = tracker

    def detect_objects(self, frame):
        raise NotImplementedError

