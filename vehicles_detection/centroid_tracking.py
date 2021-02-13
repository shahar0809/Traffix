import cv2
import numpy as np
from collections import OrderedDict
from scipy.spatial import distance as dist
import measurements_calculations.math_classes as math

class CentroidTracker:
    def __init__(self, crosswalk):
        self.max_disappeared = 50
        self.crosswalk = crosswalk
        self.next_id = 0
        self.amount_of_vehicles = [0, 0, 0]
        self.objects = OrderedDict()
        self.disappeared_objects = OrderedDict()
        crosswalk_points = self.crosswalk.get_points()
        self.line = math.LinearLine(crosswalk_points[0], crosswalk_points[1])

    @staticmethod
    def calculate_centroid(box):
        x, y, w, h = box[0], box[1], box[2], box[3]
        centroid_x = (x + x + w) / 2
        centroid_y = (y + y + h) / 2
        return centroid_x, centroid_y

    def register_object(self, box, centroid):
        centroids = [Detection(box, centroid), None, None]
        self.objects[self.next_id] = centroids
        self.disappeared_objects[self.next_id] = 0
        self.next_id += 1

    def remove_object(self, object_id):
        del self.objects[object_id]
        del self.disappeared_objects[object_id]

    def update_objects(self, boxes):
        # No objects detected in the frame
        if len(boxes) == 0:
            for id in range(self.next_id):
                self.disappeared_objects[id] += 1

                # Remove an object from the list if it has disappeared above MAX
                if self.disappeared_objects[id] > self.max_disappeared:
                    self.remove_object(id)
            return self.objects

        # Objects were detected
        self.update_new_detections(boxes)

        # Removing objects that crossed the crosswalk
        for id in self.objects.keys():
            if self.is_object_beyond_crosswalk(id):
                self.remove_object(id)

        # Update amount of object
        self.amount_of_vehicles[2] = self.amount_of_vehicles[1]
        self.amount_of_vehicles[1] = self.amount_of_vehicles[0]
        self.amount_of_vehicles[0] = self.next_id
        
    def update_new_detections(self, boxes):
        input_centroids = np.zeros((len(boxes), 2), dtype="int")

        # Assign centroids to each bounding box
        for i in range(len(boxes)):
            input_centroids[i] = self.calculate_centroid(boxes[i])
        
        # Each detection is assigned to a new id
        if len(self.objects) == 0:
            for i in range(len(boxes)):
                self.register_object(boxes[i], input_centroids[i])

        # Update based on distances between centroids
        self.update_centroids_dist(input_centroids, boxes)
    
    def update_centroids_dist(self, input_centroids, input_boxes):
        # Getting the data about the existing objects
        object_ids = list(self.objects.keys())
        object_centroids = []
        for centroids in self.objects.values():
            object_centroids.append(centroids[0])

        # Calculate the distance between each pair of existing and input centroids
        """
        The output is a 2d array, so that the [i,j] cell holds the distance
        between the input centroid in the i-th cell and the object centroid in the j-th cell
        """
        distances = dist.cdist(np.array(object_centroids), input_centroids)

        """
        Our goal is to match an input centroid to an existing object centroid.
        So we need to find the minimal distance in each row of the distances matrix.
        """
        rows = distances.min(axis=1).argsort()
        cols = distances.argmin(axis=1)[rows]

        usedRows = set()
        usedCols = set()
        # loop over the combination of the (row, column) index tuples
        for (row, col) in zip(rows, cols):
            # Ignore the tuple if the row or column was already examined
            if row in usedRows or col in usedCols:
                continue
            # Otherwise, grab the object ID for the current row
            object_ID = object_ids[row]
            # Set the new centroid
            self.update_centroids(object_ID, input_centroids[col], input_boxes[col])
            # Reset the disappeared counter
            self.disappeared_objects[object_ID] = 0

            usedRows.add(row)
            usedCols.add(col)

        # Compute the row and column indexes we haven't examined yet
        unusedRows = set(range(0, distances.shape[0])).difference(usedRows)
        unusedCols = set(range(0, distances.shape[1])).difference(usedCols)

        """
        If the number of object centroids is not smaller than the number of input centroids,
        we need to check and see if some objects have disappeared.
        """
        if distances.shape[0] >= distances.shape[1]:
            for row in unusedRows:
                object_ID = object_ids[row]
                # Increase disappearance counter
                self.disappeared_objects[object_ID] += 1
                # Check if the object needs to be removed
                if self.disappeared_objects[object_ID] > self.max_disappeared:
                    self.remove_object(object_ID)
        else:
            for col in unusedCols:
                self.register_object(input_centroids[col], input_boxes[col])

    def get_objects(self):
        return self.objects

    def update_centroids(self, object_id, new_centroid, box):
        self.objects[object_id][2] = self.objects[object_id][1]
        self.objects[object_id][1] = self.objects[object_id][0]
        self.objects[object_id][0] = Detection(box, new_centroid)

    def is_object_beyond_crosswalk(self, object_id):
        centroid = self.objects[object_id][0]
        # Checking if the vehicle has crossed the crosswalk
        if self.crosswalk.get_is_above():
            return self.line.is_point_above(math.Point(centroid[0], centroid[1]))
        else:
            return not self.line.is_point_above(math.Point(centroid[0], centroid[1]))

    def get_amount_of_objects(self):
        return self.amount_of_vehicles

    def get_disappearances(self, object_id):
        return self.disappeared_objects[object_id]

class Detection:
    def __init__(self, box, centroid=None):
        if centroid is None:
            centroid = CentroidTracker.calculate_centroid(box)
        self.centroid = centroid
        self.box = box

    def get_box(self):
        return self.box

    def get_centroid(self):
        return self.centroid
