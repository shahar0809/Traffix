from utils import LOW_BAR, MEDIUM_BAR, HIGH_BAR, LOW_LEVEL, MEDIUM_LEVEL, HIGH_LEVEL


class TrafficDetector:
    def __init__(self):
        self.boxes = None

    def detect_traffic_level(self, boxes, traffic_bars):
        self.boxes = boxes
        num_of_vehicles = len(self.boxes)

        if num_of_vehicles <= traffic_bars[LOW_BAR]:
            traffic_level = LOW_LEVEL
        elif traffic_bars[LOW_BAR] < num_of_vehicles <= traffic_bars[MEDIUM_BAR]:
            traffic_level = LOW_BAR
        elif traffic_bars[MEDIUM_BAR] < num_of_vehicles <= traffic_bars[HIGH_LEVEL]:
            traffic_level = MEDIUM_LEVEL
        else:
            traffic_level = HIGH_LEVEL

        return traffic_level
