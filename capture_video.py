import cv2


class Capture:
    """
    The Capture class manages the frames captured from the video source.
    ___________
    Attributes:
    @:param frames: List that contains groups of frames in the size of 3.
    @:param iteration: The current iteration number.
    @:cvar GROUP_SIZE: The size of each groups of frames
    @:cvar TIME_GAP: A frame gets stored each TIME_GAP iterations
    """

    def __init__(self, frames_queue, result_queue):
        self.frames_queue = frames_queue
        self.results_queue = result_queue
        self.width = 0
        self.height = 0
        self.GROUP_SIZE = 3
        self.TIME_GAP = 30
        self._iteration = 0
        self._curr_frames = []
        self.video_cap = None

    def capture_frames(self):
        """
        Gets the frames from the video source (Pure virtual function).
        @:param self: Instance of the Capture class
        @:return: None
        """
        print("capture frame")
        while True:
            # Capture frame-by-frame
            ret, frame = self.video_cap.read()
            if ret is False: break

            cv2.imshow('Traffix', frame)
            self.add_frame(frame, self.frames_queue)

            # Exiting program if the 'q' key was pressed
            if self.handle_keys(self.frames_queue) is True: break
            self._iteration += 1

        # When everything is done, release the capture
        self.video_cap.release()
        cv2.destroyAllWindows()

    def add_frame(self, frame):
        """
        Adds a frame to the list containing groups of frames.
        :param frame: The frame to be added
        :param frames_queue: The queue containing the groups of frames
        :return: None
        """

        if len(self._curr_frames) < self.GROUP_SIZE:
            self._curr_frames += [frame]

        if len(self._curr_frames) == self.GROUP_SIZE:
            self.frames_queue.put(self._curr_frames)
            self._curr_frames = [self._curr_frames[1], self._curr_frames[2]]

    def get_frames(self):
        """
        Retrieves the current group of frames in the list.
        :return: Current group of frames
        @:rtype: List containing 3 frames
        """
        print("get frame")
        if self.frames_queue.qsize() == 0:
            raise Exception("Not enough frames!")

        else:
            return self.frames_queue.get()

    def handle_keys(self, frames_queue):
        """
        Handles events of keys being pressed.
        @:keyword: If 'g' is pressed: The function 'get_frames' gets called.
        @:keyword: If 'q' is pressed: The window showing the frames gets closed.
        @:return: Indication to either close the window or not.
        @:rtype: boolean
        """
        # Getting the key pressed
        pressed_key = cv2.waitKey(1) & 0xFF

        # Getting the current group of frames
        if pressed_key == ord('g'):
            try:
                print(len(self.get_frames(frames_queue)))

            except Exception as e:
                print(e), print()

        return pressed_key == ord('q')

    def assign_dimensions(self):
        if self.video_cap.isOpened():
            self.width = int(self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_dimensions(self):
        return self.width, self.height

class LiveCapture(Capture):
    def __init__(self, frames_queue, result_queue, camera_index):
        super().__init__(frames_queue, result_queue)
        self.camera_index = camera_index
        self.video_cap = cv2.VideoCapture(self.camera_index)
        self.assign_dimensions()


class StaticCapture(Capture):
    def __init__(self, frames_queue, result_queue, video_path):
        super().__init__(frames_queue, result_queue)
        self.video_path = video_path
        self.video_cap = cv2.VideoCapture(self.video_path)
        self.assign_dimensions()

