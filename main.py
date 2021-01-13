import yolo_detection as yolo
import capture_video as cap
import cv2 as cv
import kinematics_calculation as kinematics
crosswalk = []
image = None


def capture_point(event, x, y, flags, param):
    global crosswalk, image

    if event == cv.EVENT_LBUTTONDOWN:
        image = cv.circle(image, (x, y), radius=3, color=(255, 0, 0), thickness=-2)
        crosswalk += [(x, y)]


def get_crosswalk(frame):
    clone = frame.copy()
    cv.namedWindow("Traffix")
    cv.setMouseCallback("Traffix", capture_point)

    # Keep looping until the 'q' key is pressed
    while True:
        # Display the image and wait for a keypress
        cv.imshow("Traffix", frame)
        key = cv.waitKey(1) & 0xFF
        # If the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            frame = clone.copy()
        # If the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break

    if len(crosswalk) == 4:
        return


def main():
    global crosswalk, image
    detector = yolo.YoloDetector(0.5, 0.3)

    # Detect objects in image
    capture = cv.VideoCapture('traffic.mp4')
    for i in range(20):
        ret, frame1 = capture.read()
    ret, frame2 = capture.read()
    ret, frame3 = capture.read()

    image = frame1
    get_crosswalk(frame1)
    cv.destroyAllWindows()
    print(crosswalk)
    m = kinematics.KinematicsCalculation(None, crosswalk)
    boxes, frame = detector.detect_objects(frame1)

    for box_index in boxes.flatten():
        dist = m.calc_distance(detector.boxes[box_index])

        # Drawing the crosswalk
        frame = cv.line(frame, crosswalk[0], crosswalk[1], [255, 0, 0], 1)
        frame = cv.line(frame, crosswalk[1], crosswalk[2], [255, 0, 0], 1)
        frame = cv.line(frame, crosswalk[2], crosswalk[3], [255, 0, 0], 1)
        frame = cv.line(frame, crosswalk[3], crosswalk[0], [255, 0, 0], 1)

        frame = detector.put_bounding_box(box_index, frame, dist)
        # Saving image
        cv.imwrite("result.jpg", frame)
        # Showing image
        cv.imshow('Traffix', frame)
        cv.waitKey(0)


if __name__ == '__main__':
    main()
