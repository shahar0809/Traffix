import tkinter as tk
import cv2
import gui.screen as screen
from utils import CrosswalkDetails

class MarkCrosswalk(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.camera = self.controller.data["CAMERA"]
        self.clone = None
        self.image = None
        self.crosswalk = []

        # Title
        tk.Label(self, text="Mark crosswalk", font=(self.default_font, 45)).pack()

        # Instructions
        tk.Label(self, text="Mark the crosswalk in the frame by choosing its 4 corners",
                 font=(self.default_font, 16)).pack(pady=10)
        tk.Label(self, text="Choose the point consecutively", font=(self.default_font, 16)).pack(pady=10)
        tk.Label(self, text="Choose the line closest to the vehicles' direction first",
                 font=(self.default_font, 16)).pack(pady=10)

        # A button that opens an OpenCV window to show frame
        tk.Button(self, text="Start marking", font=(self.default_font, 25), command=self.mark_crosswalk).pack(pady=30)

    def mark_crosswalk(self):
        # Create buttons to control capturing
        tk.Button(self, text="Reset", command=self.reset_crosswalk, font=(self.default_font, 20)).pack(pady=30)
        tk.Button(self, text="OK", command=self.apply_crosswalk, font=(self.default_font, 20)).pack(pady=10)

        cap = cv2.VideoCapture(self.camera.get_camera_index())
        is_read, frame = cap.read()
        
        if is_read:
            self.get_crosswalk(frame)

    """ The following functions relate to capturing the points of the crosswalk """

    def get_vehicles_direction(self):
        return self.crosswalk[0][1] < self.crosswalk[3][1]

    def reset_crosswalk(self):
        self.image = self.clone.copy()
        self.crosswalk = []

    def apply_crosswalk(self):
        cv2.destroyAllWindows()
        is_above = self.get_vehicles_direction()
        width, length = self.controller.data["CROSSWALK_WIDTH"], self.controller.data["CROSSWALK_LENGTH"]
        crosswalk = CrosswalkDetails(self.crosswalk, width, length, is_above)
        self.controller.data["CROSSWALK"] = crosswalk
        self.destroy_screen()

    def capture_mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(self.crosswalk) < 4:
            self.image = cv2.circle(self.image, (x, y), radius=3, color=(255, 0, 0), thickness=2)
            cv2.imshow('Traffix - mark crosswalk', self.image)
            k = cv2.waitKey(20) & 0xFF
            self.crosswalk += [(x, y)]
            print(self.crosswalk)

    def get_crosswalk(self, frame):
        self.clone = frame.copy()
        self.image = frame
        cv2.namedWindow("Traffix - mark crosswalk")
        cv2.setMouseCallback("Traffix - mark crosswalk", self.capture_mouse_click)

        cv2.imshow('Traffix - mark crosswalk', self.image)
        k = cv2.waitKey(20) & 0xFF
