import math_classes as geo
import cv2 as cv

LOW = 0
MED = 1
HIGH = 2


class CameraDetails:
    def __init__(self, camera_id, fps):
        self.fps = fps
        self.camera_id = camera_id

    def set_fps(self, fps):
        self.fps = fps

    def get_fps(self):
        return self.fps

    def get_id(self):
        return self.camera_id


class CrosswalkDetails:
    def __init__(self, points, width, length):

        self.points = []
        for point in points:
            self.points += geo.Point(point[0], point[1])
        self.width = width
        self.length = length

    def set_width(self, width):
        self.width = width

    def get_width(self):
        return self.width

    def set_length(self, length):
        self.length = length

    def get_length(self):
        return self.length


class Environment:
    def __init__(self, env_id, camera_id, crosswalk_points, bars, width, length):
        self.camera_id = camera_id
        self.bars = bars
        self.crosswalk_points = crosswalk_points
        self.environment_id = env_id
        self.width = width
        self.length = length

    def get_environment_id(self):
        return self.environment_id

    def get_camera_id(self):
        return self.camera_id

    def set_crosswalk_details(self, crosswalk_points):
        self.crosswalk_points = crosswalk_points

    def get_low_bar(self):
        return self.bars[LOW]

    def get_med_bar(self):
        return self.bars[MED]

    def get_high_bar(self):
        return self.bars[HIGH]

    def set_low_bar(self, bar):
        self.bars[LOW] = bar

    def set_med_bar(self, bar):
        self.bars[MED] = bar

    def set_high_bar(self, bar):
        self.bars[HIGH] = bar

    def get_width(self):
        return self.width

    def get_length(self):
        return self.length


def capture_mouse_click(event, x, y, flags, param):
    """
    crosswalk, image

    if event == cv.EVENT_LBUTTONDOWN:
        image = cv.circle(image, (x, y), radius=3, color=(255, 0, 0), thickness=-2)
        crosswalk += [(x, y)]
    """


def get_crosswalk(frame):
    """
    clone = frame.copy()
    cv.namedWindow("Traffix")
    cv.setMouseCallback("Traffix", capture_point)

    # Keep looping until the 'q' key is pressed
    while True:
        # Display the image and wait for a keypress
        cv.imshow("Traffix", frame)
        key = cv.waitKey(1) & 0xFF
        # If the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            frame = clone.copy()
        # If the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break

    if len(crosswalk) == 4:
        return
    """


def draw_shape(shape, frame):
    # Setting color and thickness of the lines drawn
    color = [255, 0, 0]
    thickness = 1

    # Drawing each line of the shape
    frame = cv.line(frame, shape[0], shape[1], color, thickness)
    frame = cv.line(frame, shape[1], shape[2], color, thickness)
    frame = cv.line(frame, shape[2], shape[3], color, thickness)
    frame = cv.line(frame, shape[3], shape[0], color, thickness)

    return frame
