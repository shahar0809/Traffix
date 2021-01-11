import yolo_detection as yolo
import kinematics_calculation as kinematics


class Decision:
    def __init__(self, vehicles, traffic_level, weather):
        self.vehicles = vehicles
        self.traffic_level = traffic_level
        self.weather = weather

    def make_decision(self):
        raise NotImplementedError

    def make_decision_for_vehicle(self, vehicle):
        raise NotImplementedError


class DecisionMaker(Decision):
    def __init__(self, vehicles, traffic_level, weather):
        Decision.__init__(self, vehicles, traffic_level, weather)

    def make_decision(self):

        velocity = kinematics.calc_velocity(box1, box2, duration)
        acceleration = kinematics.calc_acceleration(box1, box2, box3, duration)
        distance = kinematics.calc_distance(box)

        if distance > 2:
            if velocity/acceleration > 180:
                print("Pedestrians stopped. Vehicles keep driving")
            print("Vehicles stopped. Pedestrians keep walking")

        elif distance < 2:
            if velocity/acceleration < 180:
                print("Vehicles stopped. Pedestrians keep walking")
            print("Pedestrians stopped. Vehicles keep driving")

    def make_decision_for_vehicle(self, vehicle):
        if vehicle.distance > 2:
            if vehicle.velocity/vehicle.acceleration > 180:
                print("Pedestrians stopped. Vehicles keep driving")
            print("Vehicles stopped. Pedestrians keep walking")

        elif vehicle.distance < 2:
            if  vehicle.velocity/vehicle.acceleration < 180:
                print("Vehicles stopped. Pedestrians keep walking")
            print("Pedestrians stopped. Vehicles keep driving")
