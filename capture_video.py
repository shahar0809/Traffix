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

    GROUP_SIZE = 3
    TIME_GAP = 30
    _iteration = 0
    _curr_frames = []

    def video_capture(self):
        raise NotImplementedError

    def capture_frames(self, frames_queue):
        """
        Gets the frames from the video source (Pure virtual function).
        @:param self: Instance of the Capture class
        @:return: None
        """
        print("capture frame")
        cap = self.video_capture()

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret is False: break

            cv2.imshow('Traffix', frame)
            self.add_frame(frame, frames_queue)

            # Exiting program if the 'q' key was pressed
            if self.handle_keys(frames_queue) is True: break
            self._iteration += 1

        # When everything is done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def add_frame(self, frame, frames_queue):
        """
        Adds a frame to the list containing groups of frames.
        :param frame: The frame to be added
        :param frames_queue: The queue containing the groups of frames
        :return: None
        """

        if len(self._curr_frames) < self.GROUP_SIZE:
            self._curr_frames += [frame]

        if len(self._curr_frames) == self.GROUP_SIZE:
            frames_queue.put(self._curr_frames)
            self._curr_frames = [self._curr_frames[1], self._curr_frames[2]]

    def get_frames(self, frames_queue):
        """
        Retrieves the current group of frames in the list.
        :return: Current group of frames
        @:rtype: List containing 3 frames
        """
        print("get frame")
        if frames_queue.qsize() == 0:
            raise Exception("Not enough frames!")

        else:
            return frames_queue.get()

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


class LiveCapture(Capture):
    def video_capture(self):
        return cv2.VideoCapture(0)


class StaticCapture(Capture):
    def __init__(self, video_path):
        self.video_path = video_path

    def video_capture(self):
        return cv2.VideoCapture(self.video_path)


def user_interaction(video_path=None):
    STORED_VIDEO = 1
    LIVE_FOOTAGE = 2

    if video_path is not None:
        return StaticCapture(video_path)

    print("Choose an option")
    print(str(STORED_VIDEO) + " - To play a specific video")
    print(str(LIVE_FOOTAGE) + " - To capture live footage from webcam")
    choice = int(input("\n"))

    if choice == LIVE_FOOTAGE:
        return LiveCapture()
    else:
        video_path = input("Enter the path of the video:\n").replace('"', '')
        return StaticCapture(video_path)
