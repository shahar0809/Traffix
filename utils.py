import math_classes as geo

LOW = 0
MED = 1
HIGH = 2


class CameraDetails:
    def __init__(self, camera_id, fps):
        self.fps = fps
        self.camera_id = camera_id

    def set_fps(self, fps):
        self.fps = fps

    def get_fps(self):
        return self.fps

    def get_id(self):
        return self.camera_id


class CrosswalkDetails:
    def __init__(self, points, width, length, crosswalk_id=None):
        self.crosswalk_id = crosswalk_id

        self.points = []
        for point in points:
            self.points += geo.Point(point[0], point[1])
        self.width = width
        self.length = length

    def set_width(self, width):
        self.width = width

    def get_width(self):
        return self.width

    def set_length(self, length):
        self.length = length

    def get_length(self):
        return self.length


class Environment:
    def __init__(self, env_id, crosswalk_id, camera_id, bars):
        self.crosswalk_id = crosswalk_id
        self.camera_id = camera_id
        self.bars = bars
        self.environment_id = env_id

    def get_environment_id(self):
        return self.environment_id

    def get_camera_id(self):
        return self.camera_id

    def get_crosswalk_id(self):
        return self.crosswalk_id

    def get_low_bar(self):
        return self.bars[LOW]

    def get_med_bar(self):
        return self.bars[MED]

    def get_high_bar(self):
        return self.bars[HIGH]

    def set_low_bar(self, bar):
        self.bars[LOW] = bar

    def set_med_bar(self, bar):
        self.bars[MED] = bar

    def set_high_bar(self, bar):
        self.bars[HIGH] = bar
