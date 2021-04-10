from utils import LOW_BAR, MEDIUM_BAR, HIGH_BAR, LOW_LEVEL, MEDIUM_LEVEL, HIGH_LEVEL
from datetime import datetime


class TrafficDetector:
    def __init__(self, database, env_id):
        self.boxes = None
        self.database = database
        self.env_id = env_id

    def detect_traffic_level(self, boxes, traffic_bars):
        self.boxes = boxes
        num_of_vehicles = len(self.boxes)
        print("cars:")
        print(num_of_vehicles)
        print(traffic_bars)

        if num_of_vehicles <= traffic_bars[LOW_BAR]:
            traffic_level = LOW_LEVEL
        elif traffic_bars[LOW_BAR] < num_of_vehicles <= traffic_bars[MEDIUM_BAR]:
            traffic_level = LOW_BAR
        elif traffic_bars[MEDIUM_BAR] < num_of_vehicles <= traffic_bars[HIGH_LEVEL]:
            traffic_level = MEDIUM_LEVEL
        else:
            traffic_level = HIGH_LEVEL
        day, hour = self.get_time_for_db()
        print(day, hour)
        self.database.set_traffic_data(self.env_id, day, hour, traffic_level)

    @staticmethod
    def get_time_for_db():
        curr_hour = str(datetime.now().time())[:2]
        curr_day = datetime.now().strftime("%A")
        return curr_day, curr_hour
