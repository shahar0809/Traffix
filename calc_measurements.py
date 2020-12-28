import cv2 as cv
import math_classes as geo
import math

X = 0
Y = 1


class VehicleMeasure:
    camera = None
    crosswalk = [(661, 366), (825, 679), (1010, 679), (860, 366)]
    vehicles = None
    fps = 0

    def __init__(self, camera_details, crosswalk_details):
        self.camera = camera_details
        self.crosswalk = crosswalk_details

    def get_measurements(self, box1, box2, box3):
        """
        Returns the measurements of each vehicle detected (as the Vehicle class).
        :return: Vehicle
        """
        return self.calc_distance(box1)

    def calc_distance(self, box):
        """
        Calculates the distance of a vehicle detected (bounding box format) to the crosswalk.
        :param box: The bounding box of the vehicle detected.
        :type box:
        :return:
        """
        line, side = self.choose_line(box)
        (x, y) = VehicleMeasure.choose_point(box, line, side)
        print("POINT:")
        print(x, y)
        point = geo.Point(x, y)
        # TODO: convert units from pixels to real distance based on camera calibration
        return point.dist_from_line(line)

    def choose_line(self, box):
        # Getting dimensions of the bounding box
        (x, y) = (box[0], box[1])
        (w, h) = (box[2], box[3])
        print("BOX:")
        print(x, y)
        print(x, y+h)
        print(x+w, h+y)
        print(x+w, y)

        # Crosswalk built from 4 points - for now we'll put random numbers
        # TODO: Add db access, and take crosswalk details from there

        # Define linear lines of the crosswalk
        cw_line1 = geo.LinearLine.gen_line_from_points(self.crosswalk[0], self.crosswalk[2])
        print("LINE1: ")
        print(self.crosswalk[0])
        print(self.crosswalk[2])
        cw_line2 = geo.LinearLine.gen_line_from_points(self.crosswalk[1], self.crosswalk[3])
        print("LINE2: ")
        print(self.crosswalk[1])
        print(self.crosswalk[3])

        max_x = max(self.crosswalk, key=lambda item:item[1])[0]
        min_x = min(self.crosswalk, key=lambda item:item[1])[0]

        if max_x < x:
            print("CHOSE LINE 2")
            return cw_line2, True
        elif min_x > x + w:
            print("CHOSE LINE 1")
            return cw_line1, False
        # Intersection 1
        elif min_x < x < max_x:
            print("CHOSE LINE 2")
            return cw_line2, False
        # Intersection 2
        elif min_x < x + w < max_x:
            print("CHOSE LINE 1")
            return cw_line1, True

    @staticmethod
    def choose_point(box, line, side):
        # Getting dimensions of the bounding box
        (x, y) = (box[0], box[1])
        (w, h) = (box[2], box[3])

        # TODO: Add support to intersecting boxes
        if -line.get_slope() < 0 and side:
            return x, y
        elif -line.get_slope() < 0 and not side:
            return x, y + h
        elif -line.get_slope() > 0 and not side:
            return x + w, y
        elif -line.get_slope() > 0 and side:
            return x + w, y + h

    def calc_velocity(self, box1, box2, duration):
        # TODO: Get fps from capture
        dist_diff = self.calc_distance(box2) - self.calc_distance(box1)
        return dist_diff / (1 / self.fps)

    def calc_acceleration(self, box1, box2, box3, duration):
         # TODO: Get fps from capture
        velocity_diff = self.calc_velocity(box2, box3) - self.calc_velocity(box1, box2)
        return velocity_diff / (1 / self.fps)



