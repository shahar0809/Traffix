import database.DB_Wrapper as DB
from utils import LOW_BAR, MEDIUM_BAR, HIGH_BAR, LOW_LEVEL, MEDIUM_LEVEL, HIGH_LEVEL

class TrafficDetector:
    def __init__(self, boxes):
        self.boxes = boxes
        self.db_connection = DB.SqliteDatabase()

    def detect_traffic_level(self, env_id):
        traffic_bars = self.db_connection.get_traffic_bars(env_id)
        traffic_level = None

        if len(self.boxes) <= traffic_bars[LOW_BAR]:
            traffic_level = LOW_LEVEL

        else:
