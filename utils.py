import math_classes as geo


class CameraDetails:
    def __init__(self, fps):
        self.fps = fps

    def set_fps(self, fps):
        self.fps = fps

    def get_fps(self):
        return self.fps


class CrosswalkDetails:
    def __init__(self, points, width, length, bars, crosswalk_id=None, camera_id=None):
        self.crosswalk_id = crosswalk_id
        self.camera_id = camera_id

        # Setting bars for heavy traffic
        self.low_bar = bars[0]
        self.med_bar = bars[1]
        self.high_bar = bars[2]

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
