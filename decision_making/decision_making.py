import measurements_calculations.kinematics_calculation as kinematics
import cmath
import database.DB_Wrapper as db
import decision_making.weather_wrapper
import utils
import decision_making.weather_wrapper as weather_wrapper
import random

crosswalk = 0
m = kinematics.KinematicsCalculation(None, crosswalk)

HIGH_LEVEL = 3
MID_LEVEL = 2
LOW_LEVEL = 1


class Decision:
    def __init__(self, camera, location):
        self.duration = 1 / camera.get_fps()
        self.location = location

    def distance_change(self):
        raise NotImplementedError

    def calculate_time(self, distance, velocity, acceleration):
        raise NotImplementedError

    def make_decision(self, vehicles):
        raise NotImplementedError

    def make_decision_for_vehicle(self, vehicle):
        raise NotImplementedError


class DecisionMaker(Decision):
    def __init__(self, camera, location):
        super().__init__(camera, location)
        self.calculator = kinematics.KinematicsCalculation(camera, crosswalk)

    # TODO: this function doesn't get the weather - it changes the distance based on the weather
    # so change the name so that it fits
    # Also - it doesn't look at one car - it looks at the weather, and if it's risky, changes
    # the distance of all vehicles. The return should be a value that's put into all distances.
    # This function is not supposed to consider the vehicles.
    def distance_change(self):
        """
        ***I CHANGED THE DESCRIPTION BASED ON WHAT THIS FUNCTION NEEDS TO DO***
        This function calculates a scalar to the distance vector.
        The scalar is based on the current weather.
        :param: location: The location in which we want to get the weather
        :return: A scalar
        :rtype: float
        """
        weather_data = weather_wrapper.WeatherAPI(self.location)
        weather = weather_wrapper.WeatherWrapper(weather_data)
        total = weather.process_weather()
        return total

    def calculate_time(self, distance, velocity, acceleration):
        """
        The function will calculate the time until the vehicle reaches the crosswalk with the distance, velocity and the acceleration.
        :param: acceleration: The acceleration of the vehicle..
        :param: velocity: The velocity of the vehicle..
        :param: distance: The distance from the box to the crosswalk in meters.
        :return: Time until the vehicle reaching the crosswalk
        """
        # We calculate the time it takes for a vehicle to reach the crosswalk by using the equation:
        # total_distance = velocity * time + 0.5 * acceleration * time^2
        # Therefore, we need to solve this quadratic equation to get the time
        a = acceleration / 2
        b = velocity
        c = distance

        # Calculate the discriminant
        discriminant = (b ** 2) - (4 * a * c)

        if discriminant < 0 or a == 0:
            raise ZeroDivisionError
        else:
            disc = cmath.sqrt(discriminant)
            x1 = (-b + disc) / (2 * a)
            x2 = (-b - disc) / (2 * a)
            return x1.real, x2.real

    def make_decision(self, vehicles):
        """
        The function makes a decision for vehicles based on environment variables.
        :param vehicles: list of vehicles.
        :return: The decision - Is it safe to cross or not
        """

        for vehicle in vehicles:
            if not self.make_decision_for_vehicle(vehicle):
                return False
        return True

    def make_decision_for_vehicle(self, vehicle):
        """
        The function will make decision for specific vehicle based on environment variables.
        :param: vehicle: Object that will contain box and the distance, the velocity and the acceleration.
        :return: The decision - who to stop and who to let go.
        """
        calc = self.calculate_time(vehicle.distance, vehicle.velocity, vehicle.acceleration)

        if (0 < calc[0] < 20) or (0 < calc[1] < 20):
            return True
        else:
            return False


