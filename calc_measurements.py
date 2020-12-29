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
        self.camera = camera_details
        self.crosswalk = crosswalk_details

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

    def get_measurements(self, box1, box2, box3):
        """
        Returns the measurements of each vehicle detected (as the Vehicle class).
        :return: Vehicle
        """
        # Calculating distances of all boxes
        dist1 = self.calc_distance(box1)
        dist2 = self.calc_distance(box2)
        dist3 = self.calc_distance(box3)

        # Calculate velocity
        velocity1_2 = self.calc_velocity(box1, box2, 1 / self.camera.fps)
        velocity2_3 = self.calc_velocity(box2, box3, 1 / self.camera.fps)

        # Calculate acceleration
        acceleration = self.calc_acceleration(box1, box2, box3, 1 / self.camera.fps)

        return dist2, velocity1_2, acceleration
