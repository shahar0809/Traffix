import calc_measurements as calc


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
        distance = calc.distance()
        if distance > 2:
            print("Vehicles stopped. Pedestrians keep walking")
        elif distance < 2:
            print("Pedestrians stopped. Vehicles keep driving")

    def make_decision_for_vehicle(self, vehicle):
        pass
