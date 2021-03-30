# import the necessary packages
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
from imutils.video import VideoStream
import cv2
import os


class GuiVideoStream:
    def __init__(self, controller, q, stopEvent):
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.decision = False
        self.traffic_indication = None
        self.q = q
        self.stopEvent = stopEvent

        # initialize the root window and image panel
        self.root = controller
        self.panel = None
        self.traffic_panel = None

        # Defining indications
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.resources = os.path.join(self.root_dir, 'resources')

        self.green_light = cv2.imread(os.path.join(self.resources, 'green.png'))
        self.red_light = cv2.imread(os.path.join(self.resources, 'red.png'))

        self.green_light = imutils.resize(self.green_light, width=50, height=300)
        self.red_light = imutils.resize(self.red_light, width=50, height=300)

        self.green_light = self.convert_image(self.green_light)
        self.red_light = self.convert_image(self.red_light)

        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        # set a callback to handle when the window is closed
        self.root.wm_title("PyImageSearch PhotoBooth")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)\

    @staticmethod
    def convert_image(image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        return image

    def videoLoop(self):
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                out = self.q.get()
                self.frame = out[0]
                self.decision = out[1]

                if self.decision:
                    self.traffic_indication = self.green_light
                else:
                    self.traffic_indication = self.red_light

                self.frame = imutils.resize(self.frame, width=500)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(anchor="w", side="bottom", padx=10, pady=10)
                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

                if self.traffic_panel is None:
                    self.traffic_panel = tki.Label(image=self.traffic_indication)
                    self.traffic_panel.image = self.traffic_indication
                    self.traffic_panel.pack(anchor="s", side="right", padx=10, pady=10)

                # otherwise, simply update the panel
                else:
                    self.traffic_panel.configure(image=self.traffic_indication)
                    self.traffic_panel.image = self.traffic_indication

        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        self.stopEvent.set()
        self.root.quit()
