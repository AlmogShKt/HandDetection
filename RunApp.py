from HandDetectionModule import handDetector
import cv2
import time

def main():
    # previous an current time
    pre_time = 0
    cur_time = 0

    # Receive video from camera 0
    cap = cv2.VideoCapture(0)

    detector = handDetector()

    while True:
        success, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.getLendmarkPosition(img)
        #fliping the img
        img = cv2.flip(img,1)

        # Calc the fps
        cur_time = time.time()
        fps = 1 / (cur_time - pre_time)
        pre_time = cur_time

        # Show FPS on video
        cv2.putText(img, f"FPS: {str(int(fps))}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 3)

        # Show window with img
        cv2.imshow("Hey ;)", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()