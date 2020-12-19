# import the necessary packages
import numpy as np
import detector
import cv2
import os


class YoloDetector(detector.Detector):
    """
    Detects the relevant objects in the input video according to the minimal confidence and threshold.
    :keyword Relevant objects: cars, trucks, bicycles, motorbikes and buses.
    :cvar ROOT_DIR: The root directory of the project.
    :type ROOT_DIR: str
    :cvar CFG_PATH: The directory of the  net's configurations file.
    :type CFG_PATH: str
    :cvar WEIGHTS_PATH: The directory of the  net's weights file.
    :type WEIGHTS_PATH: str
    :cvar LABELS_PATH: The directory of the  net's output labels.
    :type LABELS_PATH: str
    :cvar CLASSES_IDS:
    :type CLASSES_IDS:
    :param `net`: The YOLO net loaded from the files.
    :type net: Net (OpenCV class)
    :param `layer_names`: Names of layers with unconnected outputs in the net.
    :type layer_names: list<str>
    :param `layer_outputs`: Blob for first output of the unconnected layers.
    :type layer_outputs: Mat (OpenCv class) [n dimensional dense array]
    """

    CLASSES_IDS = {1, 2, 3, 5, 7}

    # Define absolute paths
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CFG_PATH = os.path.join(ROOT_DIR, 'yolo', 'yolov3.cfg')
    WEIGHTS_PATH = os.path.join(ROOT_DIR, 'yolo', 'yolov3.weights')
    LABELS_PATH = os.path.join(ROOT_DIR, 'yolo', 'coco.names')

    # Net / Net parameters
    net = None
    layer_names = None
    layer_outputs = None

    def __init__(self, threshold, min_confidence):
        super().__init__(threshold, min_confidence)
        self.load_net()

    def load_net(self):
        """
        Loads the net from the config and weights files, and initializes it.
        :return: None
        """
        self.LABELS = open(self.LABELS_PATH).read().strip().split("\n")

        # Initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3), dtype="uint8")

        # Reads the net from the config and weights files.
        self.net = cv2.dnn.readNetFromDarknet(self.CFG_PATH, self.WEIGHTS_PATH)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

        # Loading net's layers names
        self.layer_names = self.net.getLayerNames()
        self.layer_names = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def init_lists(self):
        # Loop over each of the layer outputs
        for output in self.layer_outputs:
            # Loop over each of the detections
            for detection in output:
                # Extract the class ID and confidence of the current object detection
                scores = detection[5:]
                class_id = np.argmax(scores)

                if class_id not in self.CLASSES_IDS: continue

                confidence = scores[class_id]

                # Filter out weak predictions
                if confidence > self.min_confidence:
                    # Scale the bounding box coordinates back relative to the size of the image
                    box = detection[0:4] * np.array([self.width, self.height,
                                                     self.width, self.height])
                    (centerX, centerY, w, h) = box.astype("int")

                    # Use the center (x, y)-coordinates to derive the top and and left corner of the bounding box
                    x = int(centerX - (w / 2))
                    y = int(centerY - (h / 2))

                    # Update our list of bounding box coordinates, confidences, and class IDs
                    self.boxes.append([x, y, int(w), int(h)])
                    self.confidences.append(float(confidence))
                    self.classIDs.append(class_id)

    def detect_objects(self, frame):
        self.classIDs = []
        self.boxes = []
        self.confidences = []

        # Getting height and width of the video
        (self.height, self.width) = frame.shape[:2]

        # Create a blob (input of the net) from the frame
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (self.NET_INPUT_SIZE, self.NET_INPUT_SIZE),
                                     swapRB=True, crop=False)
        # Set the input to be the blob created
        self.net.setInput(blob)
        self.layer_outputs = self.net.forward(self.layer_names)

        # Get bounding boxes with confidences and classes
        self.init_lists()

        # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
        boxes = cv2.dnn.NMSBoxes(self.boxes, self.confidences, self.min_confidence, self.threshold)

        # If no objects were detected, return the original frame
        if len(boxes) == 0: return frame

        for box in boxes.flatten():
            frame = self.put_bounding_box(box, frame)

        print("FINISHED")
        return frame
