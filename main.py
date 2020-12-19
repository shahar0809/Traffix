import yolo_detection as yolo
import capture_video as cap
import cv2 as cv


def main():
    detector = yolo.YoloDetector(0.5, 0.3)

    # Detect objects in image
    image = cv.imread('a.jpeg')
    result = detector.detect_objects(image)
    # Create window with freedom of dimensions
    cv.imshow("Traffix", result)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
