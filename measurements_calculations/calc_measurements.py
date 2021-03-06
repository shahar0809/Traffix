import measurements_calculations.math_classes as geo
import utils

X = 0
Y = 1


class VehicleMeasure:
    def __init__(self, camera_details, crosswalk_details):
        """
        Constructor for the vehicle measure class. Initialized by the camera's details and
        the crosswalk's details.
        :param camera_details: Details about the camera in order to calculate distance in meters.
        :param crosswalk_details: The location of the crosswalk in the frame, and its size in meters.
        """
        self.camera_details = camera_details
        self.crosswalk = crosswalk_details
        # Get the known width and length of the crosswalk
        # width, length = self.crosswalk.width, self.crosswalk.length
        width = crosswalk_details.get_width() / 100
        length = crosswalk_details.get_length() / 100

        point1, point2, point3 = crosswalk_details.get_points()[0:3]

        # Get the pixels-to-meters ratio from know size
        ratio_by_length = point1.distance(point2) / length
        ratio_by_width = point2.distance(point3) / width

        # Taking the average of the ratios (Assuming that the marking of the crosswalk isn't accurate)
        self.pixels_ratio = (ratio_by_length + ratio_by_width) / 2

    def calc_distance(self, box):
        """
        Calculates the distance of a vehicle detected (bounding box format) to the crosswalk (4 points).
        :param box: The bounding box of the vehicle detected.
        :type box: list<(int, int)>
        :return: the distance from the box to the crosswalk in meters.
        """
        raise NotImplementedError

    def calc_velocity(self, box1, box2, duration):
        raise NotImplementedError

    def calc_acceleration(self, box1, box2, box3, duration):
        raise NotImplementedError

    def get_measurements(self, boxes, object_id):
        """
        Returns the measurements of each vehicle detected (as the Vehicle class).
        :return: Vehicle
        """

        print("ID: " + str(object_id))
        box1 = boxes[0]
        box2 = boxes[1]
        box3 = boxes[2]

        # Calculating distances of all boxes
        dist2 = self.calc_distance(box2)

        # Calculate velocity
        velocity1_2 = self.calc_velocity(box1, box2, 1 / self.camera_details.get_fps())

        # Calculate acceleration
        acceleration = self.calc_acceleration(box1, box2, box3, 1 / self.camera_details.get_fps())

        return utils.Vehicle(box2, object_id, dist2, velocity1_2, acceleration)
