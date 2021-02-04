# Import necessary libraries
import cv2 as cv
import queue
import threading
# Modules
import vehicles_detection.yolo_detection as yolo
import capture_video as cap
import measurements_calculations.kinematics_calculation as kinematics
import database.DB_Wrapper as db
import utils

queue = queue.Queue()


class System:
    def __init__(self, camera_id, env_id):
        self.result_queue = queue.Queue()

        # Initializing the frames capturing module
        self.capture = cap.StaticCapture('traffic.mp4')

        # Initializing the vehicle detection module
        threshold = 0.3
        confidence = 0.5
        self.detector = yolo.YoloDetector(threshold, confidence)

        # Initializing database connection
        self.db = db.SqliteDatabase()
        database = db.SqliteDatabase()
        camera = database.get_camera_details(camera_id)
        crosswalk = database.get_crosswalk_details(env_id)

        self.calculator = kinematics.KinematicsCalculation(camera, crosswalk)

    def run(self):
        self.capture = cap.StaticCapture('traffic.mp4')
        # Defining a daemon thread (background) to capture frames
        capture_thread = threading.Thread(target=self.capture.capture_frames, name='capture', daemon=True)
        # Defining a daemon thread (background) to retrieve frames
        retrieve_frames_thread = threading.Thread(target=self.capture.get_frames, name='retrieve_frames', daemon=True)
        # Defining a daemon thread (background) to display frames

    def manage_frames(self, frames):
        boxes = []
        # Getting bounding boxes
        for i in range(3):
            boxes[i], frames[i] = self.apply_detection(frames[i])

        # Calculating measurements for each vehicle detected
        vehicles = []
        for i in range(3):
            vehicles[i] = self.calculator.get_measurements(boxes[i][0], boxes[i][1], boxes[i][2])

    def apply_detection(self, frame):
        # Init
        frames = self.capture.get_frames()
        boxes, frame = self.detector.detect_objects(frame)
        return boxes, frame

    def yolo_detection_on_frame(self, boxes, frame, crosswalk):
        m = kinematics.KinematicsCalculation(None, crosswalk)
        for box_index in boxes.flatten():
            dist = m.calc_distance(self.detector.boxes[box_index])
            utils.draw_shape(crosswalk, frame)

            frame = self.detector.put_bounding_box(box_index, frame, dist)
            # Saving image
            cv.imwrite("result.jpg", frame)
            # Showing image
            cv.imshow('Traffix', frame)
            cv.waitKey(0)

    def apply_measurements_on_vehicle(self, frame):
        pass
    
    def show_frame(self):
        if self.result_queue.siz() > 0:
            frame = self.result_queue.pop()


if __name__ == '__main__':
    sys = System()
    sys.run()

"""
    m = kinematics.KinematicsCalculation(None, crosswalk)
    boxes, frame = detector.detect_objects(frame1)

    for box_index in boxes.flatten():
        dist = m.calc_distance(detector.boxes[box_index])
        utils.draw_shape(crosswalk, frame)
        

        frame = detector.put_bounding_box(box_index, frame, dist)
        # Saving image
        cv.imwrite("result.jpg", frame)
        # Showing image
        cv.imshow('Traffix', frame)
        cv.waitKey(0)
"""
