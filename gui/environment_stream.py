import tkinter as tk
import cv2
import gui.screen as screen

class EnvironmentStream(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        env_id = self.controller.data["ENV_ID"]
        self.env = self.database.get_environment(env_id)
        self.video_cap = CustomCapture(self.controller, self.env)

        self.canvas = tk.Canvas(self, )


class CustomCapture:
    def __init__(self, app, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        self.app = app
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        self.app.mainloop()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return False, None
