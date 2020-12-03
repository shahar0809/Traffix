import yolo_detection as yolo
import capture_video as cv
import time

# Checking capture file module
def capture_video_main():
    capture = cv.user_interaction()

    print("Press 'q' to quit")
    print("Press 'g' to get frames")
    time.sleep(2)

    capture.capture_frames()


# Checking detections module
def detector_main():
    video_path = input("Enter the path of the input video:\n")
    video_name = input("Enter the path of the output video:\n")
    detector = yolo.YoloDetector(video_path, video_name, 0.5, 0.3)

    detector.run_detections()


if __name__ == '__main__':
    detector_main()
