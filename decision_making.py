import kinematics_calculation as kinematics
import cmath
import DB_Wrapper as db
import weather_wrapper

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

    def get_weather(self, distance, box, m):
        raise NotImplementedError

    def calculate_time(self, distance, velocity, acceleration):
        raise NotImplementedError

    def make_decision(self, box, box1, box2, box3, duration, m):
        raise NotImplementedError

    def make_decision_for_vehicle(self, vehicle):
        raise NotImplementedError


class DecisionMaker(Decision):
    def __init__(self, vehicles, traffic_level, weather):
        self.vehicles = vehicles
        self.traffic_level = traffic_level
        self.weather = weather

    def get_traffic_level_from_database(self):
        database = db.SqliteDatabase()
        try:
            day = int(input("Please enter a day from which you want the traffic level"))
            hour = int(input("Please enter a day from which you want the traffic level"))
            return database.get_traffic_data(day, hour)

        except Exception as e:
            return e

    def get_fps_from_database(self):
        database = db.SqliteDatabase()
        try:
            camera_id = int(input("Please enter a id from which you want the fps"))
            return database.get_camera_details(camera_id)

        except Exception as e:
            return e

    def get_weather(self, distance, box, m):
        w = weather_wrapper.WeatherAPI([32.08472326847056, 34.77643445486234])
        weather = weather_wrapper.WeatherWrapper(w)
        p = weather.process_weather()
        dist = abs(m.calc_distance(box) * p / 5)

        return dist

    def calculate_time(self, distance, velocity, acceleration):
        a = acceleration / 2
        b = velocity
        c = distance

        # calculate the discriminant
        calc_dis = (b ** 2) - (4 * a * c)

        if calc_dis < 0 or a == 0:
            return "Impossible calculator"
        else:
            d = cmath.sqrt(calc_dis)
            x1 = (-b + d) / (2 * a)
            x2 = (-b - d) / (2 * a)
            return x1.real, x2.real

    def make_decision(self, box, box1, box2, box3, duration, m):
        decision = Decision()

        distance = m.calc_distance(box)
        velocity = m.calc_velocity(box1, box2, duration)
        acceleration = m.calc_acceleration(box1, box2, box3, duration)

        calc = decision.calculate_time(distance, velocity, acceleration)
        if calc[0] < 20 or calc[1] < 20:
            return "Vehicles stopped. Pedestrians keep walking"
        else:
            return "Pedestrians stopped. Vehicles keep driving"

    def make_decision_for_vehicle(self, vehicle):
        decision = Decision()

        calc = decision.calculate_time(vehicle.distance, vehicle.velocity, vehicle.acceleration)
        if calc[0] < 20 or calc[1] < 20:
            return "Vehicles stopped. Pedestrians keep walking"
        else:
            return "Pedestrians stopped. Vehicles keep driving"


