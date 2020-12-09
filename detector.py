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
    _input_path = ''
    _output_path = ''

    height = 0
    width = 0

    min_confidence = 0
    threshold = 0
    COLORS = None

    # Results of predictions
    boxes = []
    confidences = []
    classIDs = []

    def __init__(self, input_path, output_path):
        """
        Initializes the detector with the input and output paths.
        :param path: Path to input video
        :type path: str
        :param output_name: Path to output video
        :type output_name: str
        :return:
        """
        self._input_path = input_path.replace('"', '')
        self._output_path = output_path.replace('"', '')

    def show_video(self):
        """
        Displays an image that's located in the path inputted.
        :return: None
        """
        cap = cv2.VideoCapture(self._path)

        while True:
            # Reading frames from the video
            ret, frame = cap.read()
            if ret is False: break

            # Getting width and height of the frame
            height, width = frame.shape[:2]

            # Smoothing the frame
            resized_image = cv2.resize(frame, (3 * width, 3 * height), interpolation=cv2.INTER_CUBIC)

            # Displaying the frame in a window that fits the screen
            cv2.namedWindow('Traffix Video Stream', cv2.WINDOW_NORMAL)
            cv2.imshow("Traffix Video Stream", resized_image)

            # Release the capture
            cap.release()
            cv2.destroyAllWindows()

    def run_detections(self):
        raise NotImplementedError

