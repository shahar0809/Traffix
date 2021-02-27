import measurements_calculations.math_classes as geo
import cv2
import vehicles_detection.centroid_tracking as tracker

# Indices
LOW_BAR = 0
MEDIUM_BAR = 1
HIGH_BAR = 2

# Values
LOW_LEVEL = 0
MEDIUM_LEVEL = 1
HIGH_LEVEL = 2


class Vehicle:
    def __init__(self, box, id, distance, velocity, acceleration):
        self.distance = distance
        self.velocity = velocity
        self.acceleration = acceleration
        self.box = box
        self.id = id

    def get_id(self):
        return self.id

    def get_box(self):
        return self.box

    def get_distance(self):
        return self.distance

    def get_velocity(self):
        return self.velocity

    def get_acceleration(self):
        return self.acceleration


class CameraDetails:
    def __init__(self, name, fps, opencv_index, id=None):
        self.name = name
        self.opencv_index = opencv_index
        self.fps = fps
        self.id = id

    def get_camera_index(self):
        return self.opencv_index

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_fps(self, fps):
        self.fps = fps

    def get_fps(self):
        return self.fps

    def get_id(self):
        if id is None:
            raise KeyError
        else:
            return self.id


class CrosswalkDetails:
    def __init__(self, points, width, length, is_above):
        self.points = points
        self.width = width
        self.length = length
        self.is_above = is_above

    def get_points(self):
        return self.points

    def set_points(self, points):
        self.points = points

    def set_width(self, width):
        self.width = width

    def get_width(self):
        return self.width

    def set_length(self, length):
        self.length = length

    def get_length(self):
        return self.length

    def get_is_above(self):
        return self.is_above


class Environment:
    def __init__(self, camera_id, crosswalk, bars, location, id=None):
        self.camera_id = camera_id
        self.bars = bars
        self.crosswalk = crosswalk
        self.location = location
        self.id = id

    def get_id(self):
        if id is None:
            raise KeyError
        else:
            return self.id

    def get_location(self):
        return self.location

    def get_camera_id(self):
        return self.camera_id

    def set_crosswalk_details(self, crosswalk):
        self.crosswalk = crosswalk

    def get_low_bar(self):
        return self.bars[LOW_BAR]

    def get_med_bar(self):
        return self.bars[MEDIUM_BAR]

    def get_high_bar(self):
        return self.bars[HIGH_BAR]

    def set_low_bar(self, bar):
        self.bars[LOW_BAR] = bar

    def set_med_bar(self, bar):
        self.bars[MEDIUM_BAR] = bar

    def set_high_bar(self, bar):
        self.bars[HIGH_BAR] = bar


def draw_shape(shape, frame):
    # Setting color and thickness of the lines drawn
    color = [255, 0, 0]
    thickness = 1

    # Drawing each line of the shape
    frame = cv2.line(frame, shape[0], shape[1], color, thickness)
    frame = cv2.line(frame, shape[1], shape[2], color, thickness)
    frame = cv2.line(frame, shape[2], shape[3], color, thickness)
    frame = cv2.line(frame, shape[3], shape[0], color, thickness)

    return frame


def put_bounding_box(frame, vehicle):
    box = vehicle.get_box()
    # Extract the bounding box coordinates
    (x, y) = (box[0], box[1])
    (w, h) = (box[2], box[3])

    # Get the color of the label detected
    color = [0, 0, 255]
    # Create a rectangle according to the bounding box's coordinates
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)

    text = str(vehicle.get_id()) + ": " +\
        str('%.2f' % vehicle.get_distance())

    cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
    frame = cv2.circle(frame, tracker.CentroidTracker.calculate_centroid(box), radius=2, color=(0, 100, 200), thickness=2)
    return frame
