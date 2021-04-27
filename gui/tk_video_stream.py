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
    def __init__(self, frame, root, q, stopEvent):
        self.curr_frame = None
        self.frame = frame
        self.thread = None
        self.stopEvent = stopEvent
        self.decision = False
        self.traffic_indication = None
        self.image_on_canvas = None
        self.q = q

        # initialize the root window and image panel
        self.root = root
        self.panel = None
        self.traffic_panel = None

        self.tkFrame = tki.Frame(frame, bd=2, relief=tki.SUNKEN, width=600, height=600)
        self.tkFrame.grid_rowconfigure(0, weight=1)
        self.tkFrame.grid_columnconfigure(0, weight=1)

        self.x_scroll = tki.Scrollbar(self.tkFrame, orient=tki.HORIZONTAL)
        self.x_scroll.grid(row=1, column=0, sticky=tki.E + tki.W)
        self.y_scroll = tki.Scrollbar(self.tkFrame)
        self.y_scroll.grid(row=0, column=1, sticky=tki.N + tki.S)
        self.canvas = None

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
        self.root.wm_title("Traffix Stream")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

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
                print("Grabbing")
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                out = self.q.get()
                self.curr_frame = out[0]
                self.decision = out[1]

                if self.decision:
                    self.traffic_indication = self.green_light
                else:
                    self.traffic_indication = self.red_light

                # self.frame = imutils.resize(self.frame, width=600)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.curr_frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if self.canvas is not None:
                    self.canvas.itemconfig(self.image_on_canvas, image=image)

                else:
                    self.canvas = tki.Canvas(self.tkFrame, bd=0,
                                             width=600, height=600,
                                             xscrollcommand=self.x_scroll.set, yscrollcommand=self.y_scroll.set)
                    self.canvas.grid(row=0, column=0, sticky=tki.N + tki.S + tki.E + tki.W)
                    self.x_scroll.config(command=self.canvas.xview)
                    self.y_scroll.config(command=self.canvas.yview)

                    self.tkFrame.pack(anchor="w", side="bottom")
                    self.image_on_canvas = self.canvas.create_image(0, 0, image=image, anchor="nw")
                    self.canvas.config(scrollregion=self.canvas.bbox(tki.ALL))

                if self.traffic_panel is None:
                    self.traffic_panel = tki.Label(self.frame, image=self.traffic_indication)
                    self.traffic_panel.image = self.traffic_indication
                    self.traffic_panel.pack(anchor="s", side="right", padx=10, pady=10)

                # otherwise, simply update the panel
                else:
                    try:
                        self.traffic_panel.configure(image=self.traffic_indication)
                        self.traffic_panel.image = self.traffic_indication
                    except Exception as e:
                        print(e)

                """
                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = tki.Label(self.tkFrame, image=image)
                    self.panel.image = image
                    self.panel.pack(anchor="w", side="bottom", padx=10, pady=10)
                # otherwise, simply update the panel
                else:
                    try:
                        self.panel.configure(image=image)
                        self.panel.image = image
                    except Exception as e:
                        print(e)
                """

        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        self.stopEvent.set()
        self.root.quit()
