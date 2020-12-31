import calc_measurements as measurements
import math_classes as geo


class KinematicsCalculation(measurements.VehicleMeasure):
    """
    Calculates the measurements based on kinematics.
    """

    def calc_distance(self, box):
        """
        Calculates the distance of a vehicle detected (bounding box format) to the crosswalk (4 points).
        :param box: The bounding box of the vehicle detected.
        :type box: list<(int, int)>
        :return: the distance from the box to the crosswalk in meters.
        """
        line, side = self.choose_crosswalk_line(box)
        (x, y) = KinematicsCalculation.choose_point(box, line, side)
        print("POINT:")
        print(x, y)
        point = geo.Point(x, y)
        # TODO: convert units from pixels to real distance
        return point.dist_from_line(line) / self.pixels_ratio

    def choose_crosswalk_line(self, box):
        """
        In order to calculate the shortest distance from the crosswalk, we need to choose the
        closest line to the bounding box. This function calculates what line is the closest.
        :param box: The bounding box of a vehicle detected.
        :type box: list<(int, int)>
        :return: The closest crosswalk line, is the crosswalk leftward to the box
        :rtype: LinearLine object (from math_classes)
        """
        # Getting the dimensions of the bounding box
        (x, y) = (box[0], box[1])
        (width, height) = (box[2], box[3])

        # TODO: Add db access, and take crosswalk details from there

        # Define linear lines of the crosswalk
        crosswalk_line1 = geo.LinearLine.gen_line_from_points(self.crosswalk[0], self.crosswalk[2])
        crosswalk_line2 = geo.LinearLine.gen_line_from_points(self.crosswalk[1], self.crosswalk[3])

        # Getting the maximal and minimal values of the crosswalk
        crosswalk_max_x = max(self.crosswalk, key=lambda item: item[1])[0]
        crosswalk_min_x = min(self.crosswalk, key=lambda item: item[1])[0]

        '''
        Choosing the closest line based on the locations of the box and the crosswalk
        '''
        # The crosswalk is leftward to the box, and there is no intersection between them.
        if crosswalk_max_x < x:
            return crosswalk_line2, True
        # The crosswalk is rightward to the box, and there is no intersection between them.
        elif crosswalk_min_x > x + width:
            return crosswalk_line1, False
        # The objects intersect, so that a part of the box is within the crosswalk
        elif crosswalk_min_x < x < crosswalk_max_x:
            return None, None
        # The objects intersect, so that a part of the box is within the crosswalk
        elif x < crosswalk_min_x < x + width < crosswalk_max_x:
            print("CHOSE LINE 1")
            return None, None

    @staticmethod
    def choose_point(box, line, is_leftward):
        """
        Choose the extreme point from the box according to the crosswalk line and
        their locations.
        :param box: The bounding box of the vehicle detected.
        :param line: The crosswalk line closest to the box
        :param is_leftward: Is the crosswalk leftward to the box
        :return: The extreme point of the box
        """
        # Getting the dimensions of the bounding box
        (x, y) = (box[0], box[1])
        (width, height) = (box[2], box[3])

        if line.get_slope() > 0 and is_leftward:
            return x, y
        elif line.get_slope() > 0 and not is_leftward:
            return x, y + height
        elif line.get_slope() < 0 and not is_leftward:
            return x + width, y
        elif line.get_slope() < 0 and is_leftward:
            return x + width, y + height

    def calc_velocity(self, box1, box2, duration):
        dist_diff = self.calc_distance(box2) - self.calc_distance(box1)
        return dist_diff / (1 / self.camera_details.fps)

    def calc_acceleration(self, box1, box2, box3, duration):
        velocity_diff = self.calc_velocity(box2, box3) - self.calc_velocity(box1, box2)
        return velocity_diff / (1 / self.fps)
