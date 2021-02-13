# Import necessary libraries
import cv2 as cv
from queue import Queue
import numpy as np

# Modules
import vehicles_detection.yolo_detection as yolo
import capture_video as cap
import measurements_calculations.kinematics_calculation as kinematics
import database.DB_Wrapper as database
import utils
import vehicles_detection.centroid_tracking as tracker
import decision_making.decision_making as decision_making


class System:
    def __init__(self, camera_id, env_id):
        self.result_queue = Queue()
        self.frames_queue = Queue()

        self.db = database.SqliteDatabase()

        # Initializing the frames capturing module
        self.capture = cap.StaticCapture('ttt.mp4')

        # TODO: ADD a function that adds a crosswalk to the db
        # self.db.add_crosswalk_details(crosswalk_points)

        # Initializing database connection
        camera = self.db.get_camera_details(camera_id)
        crosswalk = self.db.get_crosswalk_details(env_id)

        # Initializing an object tracker
        self.tracker = tracker.CentroidTracker(crosswalk)

        # Initializing the vehicle detection module
        threshold = 0.3
        confidence = 0.5
        self.detector = yolo.YoloDetector(threshold, confidence, self.tracker)

        # Initialize class to calculate measurements
        self.calculator = kinematics.KinematicsCalculation(camera, crosswalk)

        # Initializing a decision maker
        self.decision_maker = decision_making.DecisionMaker(camera, crosswalk, [32.793542374788785, 34.98896391998108])

        self.crosswalk_mark = utils.CaptureCrosswalk()

    def run(self):
        self.capture.capture_frames(self.frames_queue)
        self.frames_queue.get()
        self.frames_queue.get()
        self.frames_queue.get()
        crosswalk_points = self.crosswalk_mark.get_crosswalk(self.frames_queue.get()[0])
        print(crosswalk_points)

        while self.frames_queue.qsize() > 0:
            frames = self.frames_queue.get()

            self.handle_frames(frames)

            res_frame = self.result_queue.get()
            cv.imshow('Traffix', res_frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        cv.destroyAllWindows()

    def handle_frames(self, frames):
        """
        Handles a group of 3 frames.
        - Applies detection on each frame
        - Calculates distance, velocity and acceleration of each vehicle
        - Makes a decision
        :param frames: the group of 3 frames
        """
        # Lists containing detection data for each frame
        boxes = []
        result_frames = []
        vehicles = []

        # For each frame, apply object detection
        for i in range(cap.Capture.GROUP_SIZE):
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
                if disappearances == 0:
                    appearances = objects[object_id]
                    if appearances[0] is None or appearances[1] is None or appearances[2] is None:
                        continue
                    vehicle_boxes = [appearances[0].get_box(),
                                     appearances[1].get_box(),
                                     appearances[2].get_box()]
                    boxes_on_frame.append(appearances[1].get_box())

                    vehicles.append(self.calculator.get_measurements(vehicle_boxes, object_id))

        # Putting the frame with the bounding boxes in the result queue
        print("Can pedestrians pass:")
        print(self.decision_maker.make_decision(boxes_on_frame))
        self.result_queue.put(self.make_frame(vehicles, result_frames[1]))

    def apply_detection(self, frame):
        boxes, frame = self.detector.detect_objects(frame)
        return boxes, frame

    @staticmethod
    def make_frame(vehicles, frame):
        for vehicle in vehicles:
            frame = utils.put_bounding_box(frame, vehicle)
        return frame


if __name__ == '__main__':
    sys = System(1, 1)
    sys.run()
