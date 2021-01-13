import kinematics_calculation as kinematics
import cmath


class Decision:

    def make_decision(self, box, box1, box2, box3, duration, m):
        raise NotImplementedError

    def make_decision_for_vehicle(self, vehicle):
        raise NotImplementedError


class DecisionMaker(Decision):
    def __init__(self, vehicles, traffic_level, weather):
        self.vehicles = vehicles
        self.traffic_level = traffic_level
        self.weather = weather

    def make_decision(self, box, box1, box2, box3, duration, m):

        velocity = m.calc_velocity(box1, box2, duration)
        acceleration = m.calc_acceleration(box1, box2, box3, duration)
        distance = m.calc_distance(box)

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
            if x1.real < float(180) or x2.real < float(180):
                return "Vehicles stopped. Pedestrians keep walking"

            else:
                return "Pedestrians stopped. Vehicles keep driving"

    def make_decision_for_vehicle(self, vehicle):
        a = vehicle.acceleration / 2
        b = vehicle.velocity
        c = vehicle.distance

        # calculate the discriminant
        calc_dis = (b ** 2) - (4 * a * c)

        if calc_dis < 0 or a == 0:
            return "Impossible calculator"

        else:
            d = cmath.sqrt(calc_dis)
            x1 = (-b + d) / (2 * a)
            x2 = (-b - d) / (2 * a)
            if x1.real < float(180) or x2.real < float(180):
                return "Vehicles stopped. Pedestrians keep walking"

            else:
                return "Pedestrians stopped. Vehicles keep driving"


def main():
    decision_maker = DecisionMaker()
    m = kinematics.KinematicsCalculation(None, [(2, 60), (60, 60), (80, 2), (1, 80)])
    box = [(1, 60), (60, 60), (80, 2), (1, 80)]
    box1 = [(1, 60), (60, 60), (80, 2), (1, 80)]
    box2 = [(1, 60), (80, 60), (1, 1), (1, 80)]
    box3 = [(1, 60), (80, 60), (1, 1), (1, 80)]
    duration = 1 / 0.2456

    decision_maker.make_decision(box, box1, box2, box3, duration, m)


if __name__ == '__main__':
    main()
