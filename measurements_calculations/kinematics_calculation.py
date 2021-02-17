import measurements_calculations.calc_measurements as measurements
import measurements_calculations.math_classes as geo


class KinematicsCalculation(measurements.VehicleMeasure):
    """
    Calculates the measurements based on kinematics.
    """

    def __init__(self, camera, crosswalk):
        super().__init__(camera, crosswalk)

    def calc_velocity(self, box1, box2, duration):
        dist_diff = self.calc_distance(box2) - self.calc_distance(box1)
        return dist_diff / (1 / self.camera_details.get_fps())

    def calc_acceleration(self, box1, box2, box3, duration):
        velocity_diff = self.calc_velocity(box2, box3, duration) - self.calc_velocity(box1, box2, duration)
        return velocity_diff / (1 / self.camera_details.get_fps())

    def calc_distance(self, box):
        crosswalk_points = self.crosswalk.get_points()

        line1 = geo.LinearLine.gen_line_from_points(crosswalk_points[0], crosswalk_points[1])
        line2 = geo.LinearLine.gen_line_from_points(crosswalk_points[2], crosswalk_points[3])

        dist = []
        x_start, y_start, width, length = box[0], box[1], box[2], box[3]
        box_points = [(x_start, y_start), (x_start + width, y_start),
                      (x_start, y_start + length), (x_start + width, y_start + length)]

        for point in box_points:
            point_obj = geo.Point(point[0], point[1])
            has_passed_line1 = (line1.is_point_above(point_obj) and self.crosswalk.get_is_above()) \
                               or (not line1.is_point_above(point_obj) and not self.crosswalk.get_is_above())

            has_passed_line2 = (line2.is_point_above(point_obj) and self.crosswalk.get_is_above()) \
                               or (not line2.is_point_above(point_obj) and not self.crosswalk.get_is_above())

            # Is the vehicle on the crosswalk
            if has_passed_line1 and not has_passed_line2:
                dist.append(0)

            if has_passed_line1 and has_passed_line2:
                dist.append(-1)

            else:
                dist.append(point_obj.dist_from_line(line1))

        return min(dist) / self.pixels_ratio
