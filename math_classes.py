import numpy as np


class Point:
    def __init__(self, init_x, init_y):
        self.x = init_x
        self.y = init_y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __str__(self):
        return 'x=' + str(self.x) + ', y=' + str(self.y)

    def distance(self, target):
        x_diff = target.x - self.x
        y_diff = target.y - self.y
        dist = numpy.math.sqrt(x_diff ** 2 + y_diff ** 2)
        return dist

    def slope_from_origin(self):
        if self.x == 0:
            return None
        else:
            return self.y / self.x

    def slope(self, target):
        if target.x == self.x:
            return None
        else:
            m = (target.y - self.y) / (target.x - self.x)
            return m

    def dist_from_line(self, line):
        res1 = abs(line.get_slope() * self.x -1 * self.get_y() + line.get_bias())
        return res1 / np.math.sqrt(line.get_slope() ** 2 + 1)


class LinearLine:
    def __init__(self, init_slope, init_bias):
        self.slope = init_slope
        self.bias = init_bias

    def get_slope(self):
        return self.slope

    def get_bias(self):
        return self.bias

    @staticmethod
    def gen_line_from_points(p1, p2):
        slope = p2.slope(p1)
        bias = p1.get_y() - slope * p1.get_x()
        line = LinearLine(slope, bias)
        return line

    def calc_y_value(self, x):
        return self.slope * x + self.bias

    def calc_x_value(self, y):
        return (y - self.bias) / self.slope

    def get_intersection(self, other):
        x_coordinate = (other.get_bias() - self.bias) / (self.slope - other.get_slope())
        y_coordinate = self.calc_y_value(x_coordinate)
        return Point(x_coordinate, y_coordinate)

    def greater_than(self, other, y_range):
        intersection = self.get_intersection(other)
        if y_range[1] > intersection.get_y() > y_range[0]:
            return None

        return self.calc_x_value(y_range[0]) > other.calc_x_value(y_range[0])





