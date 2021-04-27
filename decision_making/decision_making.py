import measurements_calculations.kinematics_calculation as kinematics
import cmath
import decision_making.weather_wrapper as weather_wrapper
from database import SQLiteDatabase
from datetime import datetime
from utils import HIGH_LEVEL, MEDIUM_LEVEL, LOW_LEVEL
crosswalk = 0



class Decision:
    def __init__(self, camera, location):
        self.duration = 1 / camera.get_fps()
        self.location = location
        self.weather_indication = ""
        self.dist_scalar = 1

    def distance_change(self):
        raise NotImplementedError

    def calculate_time(self, distance, velocity, acceleration):
        raise NotImplementedError

    def make_decision(self, vehicles):
        raise NotImplementedError

    def make_decision_for_vehicle(self, vehicle, scalar):
        raise NotImplementedError


class DecisionMaker(Decision):
    def __init__(self, camera, location, env_id):
        super().__init__(camera, location)
        self.weather_data = weather_wrapper.WeatherAPI(self.location)
        self.weather = weather_wrapper.WeatherWrapper(self.weather_data)
        self.database = SQLiteDatabase.SQLiteDatabase('..\\database\\traffixDB.db')
        self.env_id = env_id

    def distance_change(self):
        """
        This function calculates a scalar to the distance vector.
        The scalar is based on the current weather.
        :param: location: The location in which we want to get the weather
        :return: A scalar
        :rtype: float
        """
        print("we here")
        self.dist_scalar, self.weather_indication = self.weather.process_weather()
        print("WEATHER")
        print(self.weather_indication)

    def get_weather_indication(self):
        return self.weather_indication

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
        self.distance_change()
        print("YOOOOOOOOOO")
        load_scalar = self.process_loads()
        print("YOOOOOOOOOOppppp")
        for vehicle in vehicles:
            decision = self.make_decision_for_vehicle(vehicle, load_scalar)
            if decision is not None and not decision:
                return False
        return True

    def make_decision_for_vehicle(self, vehicle, load_scalar):
        """
        The function will make decision for specific vehicle based on environment variables.
        :param: vehicle: Object that will contain box and the distance, the velocity and the acceleration.
        :return: The decision - who to stop and who to let go.
        """
        print(vehicle.distance)

        # Case in which the vehicle passed the crosswalk
        if vehicle.distance < 0:
            return True

        # Case in which the vehicle is on the crosswalk
        if vehicle.distance == 0:
            return False

        try:
            print("real")
            print(vehicle.distance)
            print("after")
            print(vehicle.distance * self.dist_scalar * load_scalar)
            calc = self.calculate_time(vehicle.distance * self.dist_scalar * load_scalar, vehicle.velocity, vehicle.acceleration)
        except ZeroDivisionError:
            print("errorrrrr")
            return None

        if (0 < calc[0] < 20) or (0 < calc[1] < 20):
            return True
        else:
            return False

    def process_loads(self):
        curr_hour = str(datetime.now().time())[:2]
        curr_day = datetime.now().strftime("%A")
        load_level = self.database.get_traffic_data(curr_day, curr_hour, self.env_id)

        if load_level == LOW_LEVEL:
            return 2
        elif load_level == MEDIUM_LEVEL:
            return 1
        else:
            return 0.5



