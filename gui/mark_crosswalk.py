import tkinter as tk
from PIL import Image, ImageTk
import cv2
import gui.screen as screen
from utils import CrosswalkDetails

event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))


class MarkCrosswalk(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.camera = self.controller.data["CAMERA"]
        self.clone = None
        self.image = None
        self.marked_image = None
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
        tk.Button(self, text="Reset", command=self.reset_crosswalk, font=(self.default_font, 20)).pack(padx=10, pady=10, side=tk.LEFT)
        tk.Button(self, text="OK", command=self.apply_crosswalk, font=(self.default_font, 20)).pack(padx=10, pady=10, side=tk.RIGHT)

        frame = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        x_scroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        x_scroll.grid(row=1, column=0, sticky=tk.E + tk.W)
        y_scroll = tk.Scrollbar(frame)
        y_scroll.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.canvas = tk.Canvas(frame, bd=0, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
        self.canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        x_scroll.config(command=self.canvas.xview)
        y_scroll.config(command=self.canvas.yview)

        frame.pack(fill=tk.BOTH, expand=1)

        # Adding the image
        cap = cv2.VideoCapture(self.camera.get_camera_index())
        is_read, frame = cap.read()
        cap.release()
        if is_read:
            self.clone = frame.copy()
            self.marked_image = frame.copy()
            self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the image to PIL format
            self.image = Image.fromarray(self.image)

            self.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.image, anchor="nw")
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
            self.canvas.bind("<Button 1>", self.capture_mouse_click)

    """ The following functions relate to capturing the points of the crosswalk """

    def get_vehicles_direction(self):
        return self.crosswalk[0][1] < self.crosswalk[3][1]

    def reset_crosswalk(self):
        self.image = self.clone.copy()
        self.marked_image = self.clone.copy()
        self.show_image(self.image)
        self.crosswalk = []

    def apply_crosswalk(self):
        is_above = self.get_vehicles_direction()
        width, length = self.controller.data["CROSSWALK_WIDTH"], self.controller.data["CROSSWALK_LENGTH"]
        crosswalk = CrosswalkDetails(self.crosswalk, width, length, is_above)
        self.controller.data["CROSSWALK"] = crosswalk
        self.destroy_screen()

    def show_image(self, img):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # convert the image to PIL format
        self.image = Image.fromarray(self.image)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")

    def capture_mouse_click(self, event):
        if len(self.crosswalk) < 4:
            cx, cy = event2canvas(event, self.canvas)
            cx = int(cx)
            cy = int(cy)
            self.marked_image = cv2.circle(self.marked_image.copy(), (cx, cy), radius=3, color=(0, 255, 0), thickness=2)
            self.image = self.marked_image.copy()
            self.show_image(self.image)
            self.crosswalk += [(cx, cy)]
        print(self.crosswalk)

    def get_crosswalk(self, frame):
        self.clone = frame.copy()
        self.image = frame
        cv2.namedWindow("Traffix - mark crosswalk")
        cv2.setMouseCallback("Traffix - mark crosswalk", self.capture_mouse_click)
        cv2.imshow('Traffix - mark crosswalk', self.image)
        cv2.waitKey(20) & 0xFF
