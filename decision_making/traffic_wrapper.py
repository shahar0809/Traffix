# TODO: ADD PROCESSION OF TRAFFIC HERE
import database.DB_Wrapper as DB
from utils import LOW_BAR, MEDIUM_BAR, HIGH_BAR, LOW_LEVEL, MEDIUM_LEVEL, HIGH_LEVEL
from datetime import datetime, timezone

class TrafficDetector:
    def __init__(self, boxes):
        self.boxes = boxes
        self.db_connection = DB.SqliteDatabase()
        self.traffic_bars = {}

    def init_traffic_bars(self, env_id):
        traffic_bars = self.db_connection.get_traffic_bars(env_id)

        for bar in [LOW_BAR, MEDIUM_BAR, HIGH_BAR]:
            self.traffic_bars[bar] = traffic_bars[bar]

    def detect_traffic_level(self, env_id):
        self.init_traffic_bars(env_id)
        traffic_level = self.classify_traffic(self.boxes)

        # Getting UTC current hour
        current_time = datetime.now(timezone.utc)
        # Updating traffic data in database
        self.db_connection.set_traffic_data(env_id, current_time.weekday(), current_time.hour, traffic_level)

    def classify_traffic(self, traffic):
        if len(traffic) <= self.traffic_bars[LOW_BAR]:
            return LOW_LEVEL

        elif self.traffic_bars[LOW_BAR] < len(traffic) <= self.traffic_bars[MEDIUM_BAR]:
            return MEDIUM_LEVEL

        else:
            return HIGH_LEVEL
