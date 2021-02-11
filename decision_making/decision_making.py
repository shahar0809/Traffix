import measurements_calculations.kinematics_calculation as kinematics
import cmath
import database.DB_Wrapper as db
import decision_making.weather_wrapper

crosswalk = 0
m = kinematics.KinematicsCalculation(None, crosswalk)

HIGH_LEVEL = 3
MID_LEVEL = 2
LOW_LEVEL = 1


class Decision:
    def get_traffic_level_from_database(self):
        raise NotImplementedError

    def get_fps_from_database(self):
        raise NotImplementedError

    def get_weather(self, distance, box):
        raise NotImplementedError

    def calculate_time(self, distance, velocity, acceleration):
        raise NotImplementedError

    def make_decision(self, box, box1, box2, box3, duration):
        raise NotImplementedError

    def make_decision_for_vehicle(self, vehicle):
        raise NotImplementedError


class DecisionMaker(Decision):
    def __init__(self, vehicles, traffic_level, weather, camera, crosswalk):
        self.vehicles = vehicles
        self.traffic_level = traffic_level
        self.weather = weather
        self.calculator = kinematics.KinematicsCalculation(camera, crosswalk)

    # Not necessary :(
    def get_traffic_level_from_database(self):
        """
        The function asking the day and the hour which the user want the traffic level.
        The function will ask the user for the day and the hour of the loads from which he wants the traffic level
        to returned to the user the level.
        :return: traffic level
        """
        database = db.SqliteDatabase()
        try:
            day = int(input("Please enter a day from which you want the traffic level"))
            hour = int(input("Please enter a hour from which you want the traffic level"))
            return database.get_traffic_data(day, hour)

        except Exception as e:
            return e

    # Not necessary :(
    def get_fps_from_database(self):
        """
        The function will ask the user for the id of the camera from which he wants the fps
        to returned to the user the fps.
        :return: fps
        """
        database = db.SqliteDatabase()
        try:
            camera_id = int(input("Please enter a id from which you want the fps"))
            return database.get_camera_details(camera_id)

        except Exception as e:
            return e

    # TODO: this function doesn't get the weather - it changes the distance basedd on the weather
    # so change the name so that it fits
    # Also - it doesn't look at one car - it looks at the weather, and if it's risky, changes
    # the distance of all vehicles. The return should be a value that's put into all distances.
    # This function is not supposed to consider the vehicles.
    def get_weather(self, distance, box, location):
        """
        The function will recalculate the distance with the process weather.
        :param: box: The bounding box of the vehicle detected.
        :param: distance: The distance from the box to the crosswalk in meters.
        :return: Distance
        """
        weather_data = decision_making.weather_wrapper.WeatherAPI(location)
        weather_wrapper = decision_making.weather_wrapper.WeatherWrapper(weather_data)
        total = weather_wrapper.process_weather()
        dist = abs(self.calculator.calc_distance(box) * total / 5)

        return dist

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

    def make_decision(self, boxes, duration):
        """
        The function makes a decision for vehicles based on environment variables.
        :param boxes: The bounding boxes of the vehicle detected in the group of frames.
        :param duration: The fps from the camera details.
        :return: The decision - Is it safe to cross or not
        """
        # TODO: this needs to look at ALL vehicles in the frame. You only looked at one

        dist, velocity, acceleration = self.calculator.get_measurements(boxes)
        distance = self.get_weather(dist, box, m)

        calc = decision.calculate_time(distance, velocity, acceleration)
        if calc[0] < 20 or calc[1] < 20:
            return "Vehicles stopped. Pedestrians keep walking"
        else:
            return "Pedestrians stopped. Vehicles keep driving"

    def make_decision_for_vehicle(self, vehicle):
        """
        The function will make decision for specific vehicle based on environment variables.
        :param: vehicle: Object that will contain box and the distance, the velocity and the acceleration.
        :return: The decision - who to stop and who to let go.
        """
        #TODO: This needs to take care of ONE vehicle

        decision = Decision()

        calc = decision.calculate_time(vehicle.distance, vehicle.velocity, vehicle.acceleration)
        if calc[0] < 20 or calc[1] < 20:
            return "Vehicles stopped. Pedestrians keep walking"
        else:
            return "Pedestrians stopped. Vehicles keep driving"


