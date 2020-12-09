# import the necessary packages
import numpy as np
import detector
import imutils
import time
import cv2
import os

class YoloDetector(detector.Detector):
    """
    Runs detections of relevant objects using YOLOv3.
    :cvar ROOT_DIR: The root directory of the project.
    :type ROOT_DIR: str
    :cvar CFG_PATH: The directory of the  net's configurations file.
    :type CFG_PATH: str
    :cvar WEIGHTS_PATH: The directory of the  net's weights file.
    :type WEIGHTS_PATH: str
    :cvar LABELS: The directory of the  net's output labels.
    :type LABELS: str
    """
    # TODO: Complete docstring of YOLO detector class

    # Define absolute paths
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CFG_PATH = os.path.join(ROOT_DIR, 'yolo', 'yolov3-tiny.cfg')
    WEIGHTS_PATH = os.path.join(ROOT_DIR, 'yolo', 'yolov3-tiny.weights')
    LABELS = os.path.join(ROOT_DIR, 'yolo', 'coco.names')

    # Net / Net parameters
    net = None
    layer_names = None
    layer_outputs = None

    def __init__(self, input_path, output_path, min_confidence, threshold):
        super().__init__(input_path, output_path)
        self.min_confidence = min_confidence
        self.threshold = threshold

    def load_net(self):
        """
        Loads the net from the config and weights files.
        Loads the classes names from the coco.names file.
        :return: None
        """
        # Initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3), dtype="uint8")

        # Load the YOLO object detector was trained on COCO dataset and
        # determine only the *output* layer names that we need from YOLO
        print("[INFO] loading YOLO from disk...")

        self.net = cv2.dnn.readNet(self.CFG_PATH, self.WEIGHTS_PATH)
        self.layer_names = self.net.getLayerNames()

        self.layer_names = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def init_lists(self):
        # initialize our lists of detected bounding boxes, confidences, and class IDs, respectively
        boxes = [], confidences = [], classIDs = []

        # loop over each of the layer outputs
        for output in self.layer_outputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > self.min_confidence:
                    # scale the bounding box coordinates back relative to
                    # the size of the image, keeping in mind that YOLO
                    # actually returns the center (x, y)-coordinates of
                    # the bounding box followed by the boxes' width and
                    # height
                    box = detection[0:4] * np.array([self.width,
                                                     self.height,
                                                     self.width,
                                                     self.height])
                    (centerX, centerY, self.width, self.height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top
                    # and and left corner of the bounding box
                    x = int(centerX - (self.width / 2))
                    y = int(centerY - (self.height / 2))

                    # update our list of bounding box coordinates, confidences, and class IDs
                    boxes.append([x, y, int(self.width), int(self.height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

                return boxes, confidences, classIDs

    def show_bounding_box(self, index, frame):
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

    # 1st version of trying to divide into functions
    def run_detection(self):
        """
        Detects the relevant objects in the input video according to the minimal confidence and threshold.
        :keyword Relevant objects: cars, trucks, bicycles, motorbikes and buses.
        :param input_video: Path to input video
        :type input_video: str
        :param output_video: Path to output video
        :type output_video: str
        :param min_confidence: Minimum probability to filter weak detections
        :type min_confidence: int
        :param threshold: Threshold when applying non-maxima suppression
        :type min_confidence: threshold
        :return:
        """
        # TODO: move docstring of args to class docstring

        self.load_net()

        # Initialize the video stream, pointer to output video file, and frame dimensions
        video = cv2.VideoCapture(self._input_path)
        # Getting height and width of the video
        self.height, self.width = video.get(cv2.CAP_PROP_FRAME_HEIGHT), video.get(cv2.CAP_PROP_FRAME_WIDTH)

        # Initialize video writer
        writer = cv2.VideoWriter(self.output_video, cv2.VideoWriter_fourcc(*"MJPG"), 30,
                                 (self.width, self.height), True)

        # Determine the total number of frames in the video file
        try:
            prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
                else cv2.CAP_PROP_FRAME_COUNT

            total = int(video.get(prop))
            print("[INFO] {} total frames in video".format(total))

        # Error occurred while trying to determine the total number of frames in the video file
        except:
            print("[INFO] could not determine # of frames in video")
            print("[INFO] no approx. completion time can be provided")
            total = -1

        # Loop over frames from the video file stream
        while True:
            # read the next frame from the file
            (grabbed, frame) = video.read()

            # if the frame was not grabbed, then we have reached the end of the stream
            if not grabbed: break

            # construct a blob from the input frame and then perform a forward
            # pass of the YOLO object detector, giving us our bounding boxes
            # and associated probabilities
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
            self.net.setInput(blob)
            start = time.time()
            layerOutputs = self.net.forward(self.layer_names)
            end = time.time()

            self.init_lists(layerOutputs)

            # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
            idxs = cv2.dnn.NMSBoxes(self.boxes, self.confidences, self.min_confidence, self.threshold)

            # Ensure at least one detection exists
            if len(idxs) > 0:
                # Loop over the indexes we are keeping
                for i in idxs.flatten():
                    self.show_bounding_box(i, frame)

                # Some information on processing single frame
                if total > 0:
                    elap = (end - start)
                    print("[INFO] single frame took {:.4f} seconds".format(elap))
                    print("[INFO] estimated total time to finish: {:.4f}".format(elap * total))

            # write the output frame to disk
            writer.write(frame)

        # release the file pointers
        print("[INFO] cleaning up...")
        writer.release()
        video.release()

    # 2nd version of trying to divide into functions
    def run_detections2(self):
        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3), dtype="uint8")

        # load our YOLO object detector trained on COCO dataset (80 classes)
        # and determine only the *output* layer names that we need from YOLO
        print("[INFO] loading YOLO from disk...")
        net = cv2.dnn.readNetFromDarknet(self.CFG_PATH, self.WEIGHTS_PATH)
        self.layer_names = net.getLayerNames()
        self.layer_names = [self.layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # initialize the video stream, pointer to output video file, and
        # frame dimensions
        vs = cv2.VideoCapture(self._input_path)
        writer = None
        (self.width, self.height) = (None, None)

        # try to determine the total number of frames in the video file
        try:
            prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
                else cv2.CAP_PROP_FRAME_COUNT
            total = int(vs.get(prop))
            print("[INFO] {} total frames in video".format(total))

        # an error occurred while trying to determine the total number of frames in the video file
        except:
            print("[INFO] could not determine # of frames in video")
            print("[INFO] no approx. completion time can be provided")
            total = -1

        # loop over frames from the video file stream
        while True:
            # read the next frame from the file
            (grabbed, frame) = vs.read()

            # if the frame was not grabbed, then we have reached the end of the stream
            if not grabbed:
                break

            # if the frame dimensions are empty, grab them
            if self.width is None or self.height is None:
                (self.height, self.width) = frame.shape[:2]

            # construct a blob from the input frame and then perform a forward pass of the YOLO
            # object detector, giving us our bounding boxes and associated probabilities
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
            net.setInput(blob)
            start = time.time()
            self.layer_outputs = net.forward(self.layer_names)
            end = time.time()

            # initialize our lists of detected bounding boxes, confidences, and class IDs, respectively
            boxes = []
            confidences = []
            classIDs = []

            # loop over each of the layer outputs
            for output in self.layer_outputs:
                # loop over each of the detections
                for detection in output:
                    # extract the class ID and confidence (i.e., probability) of the current object detection
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]

                    # filter out weak predictions by ensuring the detected probability is
                    # greater than the minimum probability
                    if confidence > self.min_confidence:
                        # scale the bounding box coordinates back relative to
                        # the size of the image, keeping in mind that YOLO
                        # actually returns the center (x, y)-coordinates of
                        # the bounding box followed by the boxes' width and height
                        box = detection[0:4] * np.array([self.width, self.height, self.width, self.height])
                        (centerX, centerY, width, height) = box.astype("int")

                        # use the center (x, y)-coordinates to derive the top
                        # and and left corner of the bounding box
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        # update our list of bounding box coordinates,
                        # confidences, and class IDs
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)

            # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.min_confidence, self.threshold)

            # ensure at least one detection exists
            if len(idxs) > 0:
                # loop over the indexes we are keeping
                for i in idxs.flatten():
                    # extract the bounding box coordinates
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])

                    # draw a bounding box rectangle and label on the frame
                    color = [int(c) for c in self.COLORS[classIDs[i]]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    text = "{}: {:.4f}".format(self.LABELS[classIDs[i]], confidences[i])
                    cv2.putText(frame, text, (x, y - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # check if the video writer is None
            if writer is None:
                # initialize our video writer
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter(output, fourcc, 30, (frame.shape[1], frame.shape[0]), True)

                # some information on processing single frame
                if total > 0:
                    elap = (end - start)
                    print("[INFO] single frame took {:.4f} seconds".format(elap))
                    print("[INFO] estimated total time to finish: {:.4f}".format(
                        elap * total))

            # write the output frame to disk
            writer.write(frame)

        # release the file pointers
        print("[INFO] cleaning up...")
        writer.release()
        vs.release()

    # original code from tutorial
    def run_detections(self):
        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),
                                   dtype="uint8")

        # load our YOLO object detector trained on COCO dataset (80 classes)
        # and determine only the *output* layer names that we need from YOLO
        print("[INFO] loading YOLO from disk...")
        net = cv2.dnn.readNetFromDarknet(self.CFG_PATH, self.WEIGHTS_PATH)
        self.layer_names = net.getLayerNames()
        self.layer_names = [self.layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # initialize the video stream, pointer to output video file, and
        # frame dimensions
        vs = cv2.VideoCapture(self._input_path)
        writer = None
        (self.width, self.height) = (None, None)

        # try to determine the total number of frames in the video file
        try:
            prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
                else cv2.CAP_PROP_FRAME_COUNT
            total = int(vs.get(prop))
            print("[INFO] {} total frames in video".format(total))

        # an error occurred while trying to determine the total
        # number of frames in the video file
        except:
            print("[INFO] could not determine # of frames in video")
            print("[INFO] no approx. completion time can be provided")
            total = -1

        # loop over frames from the video file stream
        while True:
            # read the next frame from the file
            (grabbed, frame) = vs.read()

            # if the frame was not grabbed, then we have reached the end
            # of the stream
            if not grabbed:
                break

            # if the frame dimensions are empty, grab them
            if self.width is None or self.height is None:
                (self.height, self.width) = frame.shape[:2]

            # construct a blob from the input frame and then perform a forward
            # pass of the YOLO object detector, giving us our bounding boxes
            # and associated probabilities
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                         swapRB=True, crop=False)
            net.setInput(blob)
            start = time.time()
            self.layer_outputs = net.forward(self.layer_names)
            end = time.time()

            # initialize our lists of detected bounding boxes, confidences,
            # and class IDs, respectively
            boxes = []
            confidences = []
            classIDs = []

            # loop over each of the layer outputs
            for output in self.layer_outputs:
                # loop over each of the detections
                for detection in output:
                    # extract the class ID and confidence (i.e., probability)
                    # of the current object detection
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]

                    # filter out weak predictions by ensuring the detected
                    # probability is greater than the minimum probability
                    if confidence > self.min_confidence:
                        # scale the bounding box coordinates back relative to
                        # the size of the image, keeping in mind that YOLO
                        # actually returns the center (x, y)-coordinates of
                        # the bounding box followed by the boxes' width and
                        # height
                        box = detection[0:4] * np.array([self.width, self.height, self.width, self.height])
                        (centerX, centerY, width, height) = box.astype("int")

                        # use the center (x, y)-coordinates to derive the top
                        # and and left corner of the bounding box
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        # update our list of bounding box coordinates,
                        # confidences, and class IDs
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)

            # apply non-maxima suppression to suppress weak, overlapping
            # bounding boxes
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.min_confidence,
                                    self.threshold)

            # ensure at least one detection exists
            if len(idxs) > 0:
                # loop over the indexes we are keeping
                for i in idxs.flatten():
                    # extract the bounding box coordinates
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])

                    # draw a bounding box rectangle and label on the frame
                    color = [int(c) for c in self.COLORS[classIDs[i]]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    text = "{}: {:.4f}".format(self.LABELS[classIDs[i]],
                                               confidences[i])
                    cv2.putText(frame, text, (x, y - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # check if the video writer is None
            if writer is None:
                # initialize our video writer
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter(self._output_path, fourcc, 30,
                                         (frame.shape[1], frame.shape[0]), True)

                # some information on processing single frame
                if total > 0:
                    elap = (end - start)
                    print("[INFO] single frame took {:.4f} seconds".format(elap))
                    print("[INFO] estimated total time to finish: {:.4f}".format(
                        elap * total))

            # write the output frame to disk
            writer.write(frame)

        # release the file pointers
        print("[INFO] cleaning up...")
        writer.release()
        vs.release()


