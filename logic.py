# Import necessary libraries and modules
import cv2 as cv
import queue
import threading
import yolo_detection as yolo
import capture_video as cap
import kinematics_calculation as kinematics
import utils

queue = queue.Queue()


class System:
    def __init__(self):
        # Initializing the frames capturing module
            self.capture = cap.StaticCapture('traffic.mp4')

    def run(self):

        capture = cap.StaticCapture('traffic.mp4')
        # Defining a daemon thread (background) to capture frames
        capture_thread = threading.Thread(target=capture.capture_frames, name='capture', daemon=True)
        # Defining a daemon thread (background) to retrieve frames
        retrieve_frames_thread = threading.Thread(target=capture.get_frames, name='retrieve_frames', daemon=True)

        # Initializing the vehicle detection module
        threshold = 0.3
        confidence = 0.5
        detector = yolo.YoloDetector(threshold, confidence)


    def apply_detection(self, frame):

        # Ini


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
