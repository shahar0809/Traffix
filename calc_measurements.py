import cv2 as cv
import math_classes as geo
import math

X = 0
Y = 1


class VehicleMeasure:
    camera = None
    crosswalk = None
    vehicles = None
    fps = 0

    def __init__(self, camera_details, crosswalk_details):
        self.camera = camera_details
        self.crosswalk = crosswalk_details

    def get_measurements(self):
        """
        Returns the measurements of each vehicle detected (as the Vehicle class).
        :return: Vehicle
        """
        raise NotImplementedError

    @staticmethod
    def calc_distance(box):
        """
        Calculates the distance of a vehicle detected (bounding box format) to the crosswalk.
        :param box: The bounding box of the vehicle detected.
        :type box:
        :return:
        """
        line, side = VehicleMeasure.choose_line(box)
        (x, y) = VehicleMeasure.choose_point(box, line, side)
        point = geo.Point(x, y)
        # TODO: convert units from pixels to real distance based on camera calibration
        return point.dist_from_line(line)

    def choose_line(self, box):
        # Getting dimensions of the bounding box
        (x, y) = (box[0], box[1])
        (w, h) = (box[2], box[3])

        # Crosswalk built from 4 points - for now we'll put random numbers
        # TODO: Add db access, and take crosswalk details from there

        # Define linear lines of the crosswalk
        cw_line1 = geo.LinearLine.gen_line_from_points(self.crosswalk[0], self.crosswalk[1])
        cw_line2 = geo.LinearLine.gen_line_from_points(self.crosswalk[2], self.crosswalk[3])

        max_x = max(self.crosswalk, key=lambda item:item[1])[0]
        min_x = min(self.crosswalk, key=lambda item:item[1])[0]

        if max_x < x:
            return cw_line2, True
        elif min_x > x + w:
            return cw_line1, False
        # Intersection 1
        elif min_x < x < max_x:
            return cw_line2, False
        # Intersection 2
        elif min_x < x + w < max_x:
            return cw_line1, True

    @staticmethod
    def choose_point(box, line, side):
        # Getting dimensions of the bounding box
        (x, y) = (box[0], box[1])
        (w, h) = (box[2], box[3])

        # TODO: Add support to intersecting boxes
        if line.get_slope() < 0 and side:
            return x, y
        elif line.get_slope < 0 and not side:
            return x, y + h
        elif line.get_slope() > 0 and not side:
            return x + w, y
        elif line.get_slope() > 0 and side:
            return x + w, y + h

    def calc_velocity(self, box1, box2, duration):
        dist_diff = self.calc_distance(box2) - self.calc_distance(box1)
        return dist_diff / (1 / self.fps)

    def calc_acceleration(self, box1, box2, box3, duration):
        velocity_diff = self.calc_velocity(box2, box3) - self.calc_velocity(box1, box2)
        return velocity_diff / (1 / self.fps)
