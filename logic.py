# Import necessary libraries
import cv2 as cv
import time
from queue import Queue
import threading
import _thread

# Modules
import vehicles_detection.yolo_detection as yolo
import capture_video as cap
import measurements_calculations.kinematics_calculation as kinematics
import database.DB_Wrapper as database
import utils


class System:
    def __init__(self, camera_id, env_id):
        self.result_queue = Queue()
        self.frames_queue = Queue()

        # Initializing the frames capturing module
        self.capture = cap.StaticCapture('traffic.mp4')

        # Initializing the vehicle detection module
        threshold = 0.3
        confidence = 0.5
        self.detector = yolo.YoloDetector(threshold, confidence)

        # Initializing database connection
        self.db = database.SqliteDatabase()
        camera = self.db.get_camera_details(camera_id)
        crosswalk = self.db.get_crosswalk_details(env_id)
        # Initialize class to calculate measurements
        self.calculator = kinematics.KinematicsCalculation(camera, crosswalk)

    def run(self):
        self.capture = cap.StaticCapture('traffic.mp4')
        self.capture.capture_frames(self.frames_queue)

        while self.frames_queue.qsize() > 0:
            frames = self.frames_queue.get()
            self.handle_frames(frames)

            res_frame = self.result_queue.get()
            cv.imshow('Traffix', res_frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        cv.destroyAllWindows()

    def handle_frames(self, frames):
        # Applying object detection on input frame
        boxes = []
        result_frames = []
        vehicles = []

        for i in range(cap.Capture.GROUP_SIZE):
            boxes_result, frame = self.apply_detection(frames[i])

            boxes.append(boxes_result)
            result_frames += [frame]

        # Applying measurements calculations

        max_size = min(len(boxes[0]), min(len(boxes[1]), len(boxes[2])))
        for i in range(max_size):
            vehicle_boxes = [boxes[0][i], boxes[1][i], boxes[2][i]]
            vehicles.append(self.calculator.get_measurements(vehicle_boxes))

        self.result_queue.put(self.make_frame(vehicles, result_frames[1]))

    def apply_detection(self, frame):
        boxes, frame = self.detector.detect_objects(frame)
        return boxes, frame

    def make_frame(self, vehicles, frame):
        for vehicle in vehicles:
            frame = utils.put_bounding_box(frame, vehicle)
        return frame



if __name__ == '__main__':
    sys = System(1, 1)
    sys.run()
