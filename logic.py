# Import necessary libraries
import cv2 as cv
from queue import Queue

# Modules
import vehicles_detection.yolo_detection as yolo
import capture_video as cap
import measurements_calculations.kinematics_calculation as kinematics
import multiprocessing as mp
import utils
import vehicles_detection.centroid_tracking as tracker
import decision_making.decision_making as decision_making


class System:
    def __init__(self, frames_queue, results_queue, env, db, video_path=None):
        """
        An initializer to the System object. Initializes all the components and modules that the logic unit uses:
        * Objects detection
        * Objects tracking
        * Measurements calculation
        * Database
        * Decision making
        :param env_id: The ID (in the db) of the environment.
        :type env_id: int
        :param video_path:
        :type video_path: str
        """
        self.result_queue = results_queue
        self.frames_queue = frames_queue

        # Initializing database connection and getting env
        self.db = db
        self.env = env

        # Asking user to mark the crosswalk in the frame
        # self.crosswalk_mark = utils.CaptureCrosswalk()
        # crosswalk_points = self.crosswalk_mark.get_crosswalk(frame)
        # print(crosswalk_points)

        # crosswalk = utils.CrosswalkDetails(crosswalk_points, 30, 5, True)
        # self.db.set_crosswalk_details(crosswalk, 1)

        # Getting camera and crosswalk details from database
        self.camera = self.db.get_camera_details(self.env.get_camera_id())
        self.crosswalk = self.env.get_crosswalk_details()

        # Initializing the frames capturing module
        self.capture = cap.LiveCapture(self.frames_queue, self.result_queue, -1)

        # Initializing an object tracker
        self.tracker = tracker.CentroidTracker(self.crosswalk)

        # Initializing the vehicle detection module
        threshold = 0.3
        confidence = 0.5
        self.detector = yolo.YoloDetector(threshold, confidence, self.tracker)

        # Initialize class to calculate measurements
        self.calculator = kinematics.KinematicsCalculation(self.camera, self.crosswalk)

        # Initializing a decision maker
        self.decision_maker = decision_making.DecisionMaker(self.camera, [32.793542374788785, 34.98896391998108])

        # Init thread of capturing frames
        self.stop_event = mp.Event()
        self.cap_thread = mp.Process(target=self.capture.capture_frames, args=(self.stop_event,), daemon=True)
        self.frames_thread = mp.Process(target=self.pop_frames, args=(), daemon=True)

    def on_close(self):
        self.stop_event.set()

    def run(self):
        """
        Manages the order of the operations, and manages the queues in the program.
        :return: None
        """
        self.cap_thread.start()
        self.frames_thread.start()

    def pop_frames(self):
        while not self.stop_event.is_set():
            if self.frames_queue.qsize() > 0:
                frames = self.frames_queue.get()
                print("loop")
                self.handle_frames(frames)

    def get_weather_indication(self):
        return self.decision_maker.weather_indication, self.decision_maker.dist_scalar

    def handle_frames(self, frames):
        """
        Handles a group of 3 frames and performs the next operations:
        - Applies vehicles detection on each frame
        - Calculates distance, velocity and acceleration of each vehicle
        - Makes a decision if it's safe to pass the crosswalk
        - Inserts the result frame and the final decision into the result queue.
        :param frames: The group of 3 frames
        :type frames: list<Matrix>
        :return None
        """
        # Lists containing detection data for each frame
        boxes = []
        result_frames = []
        vehicles = []

        # For each frame, apply object detection

        for i in range(self.capture.GROUP_SIZE):
            boxes_result, frame = self.apply_detection(frames[i])
            # Append results of the frame to the lists
            boxes.append(boxes_result)
            result_frames.append(frame)

        # Applying measurements calculations
        objects = self.tracker.get_objects()
        amount = self.tracker.get_amount_of_objects()

        boxes_on_frame = []
        for object_id in range(amount[0]):
            try:
                disappearances = self.tracker.get_disappearances(object_id)
            except KeyError:
                pass
            else:
                # Checking that the object is in the frame
                if disappearances == 0:
                    appearances = objects[object_id]
                    if appearances[0] is None or appearances[1] is None or appearances[2] is None:
                        continue
                    # Getting the boxes of the vehicle in the last 3 frames
                    vehicle_boxes = [appearances[0].get_box(),
                                     appearances[1].get_box(),
                                     appearances[2].get_box()]
                    # The box that will be shown in the frame is the "middle" one
                    # since the measurements calculation is based on the previous and next data
                    boxes_on_frame.append(appearances[1].get_box())
                    # Adding the calculations of the vehicle to the frame's vehicles list
                    vehicles.append(self.calculator.get_measurements(vehicle_boxes, object_id))

        # Putting the frame with the bounding boxes in the result queue
        decision = self.decision_maker.make_decision(vehicles)
        self.result_queue.put((self.make_frame(vehicles, result_frames[1]), decision))

    def apply_detection(self, frame):
        """
        Applies YOLO vehicle detection on a single frame.
        :param frame: The frame to apply detection on
        :type frame: image (OpenCV object)
        :return: The bounding boxes detected by the machine, and the frame with the bounding boxes
        drawn over it.
        :rtype: list<Box object>, Image(OpenCV object)
        """
        boxes, frame = self.detector.detect_objects(frame)
        return boxes, frame

    @staticmethod
    def make_frame(vehicles, frame):
        """
        :param vehicles: A list of vehicles objects (contain all data about vehicle)
        :type vehicles: list<Vehicle>
        :param frame: The frame inputted from the source
        :type frame: OpenCV frame (a matrix)
        :return: A frame with the bounding boxes marked, and with the vehicles' data
        :rtype: OpenCV frame (a matrix)
        """
        for vehicle in vehicles:
            frame = utils.put_bounding_box(frame, vehicle)
        return frame


if __name__ == '__main__':
    sys = System(1, 1, 'ttt.mp4')
    sys.run()
