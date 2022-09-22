from HandDetectionModule import handDetector, calcDistanceBetweenFingers
from HandFunctions import Features
import cv2
import time

def main():
    # previous an current time
    pre_time = 0
    cur_time = 0

    # Receive video from camera 0
    cap = cv2.VideoCapture(0)

    detector = handDetector()
    allFeature = Features(detector)

    detector.initHandSize()
    print("Done init, starting app...")
    while True:
        success, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.getLendmarkPos(img)
        #fliping the img
        img = cv2.flip(img,1)

        if lmList:
            if allFeature.handIsClose(lmList):
                cv2.rectangle(img, (10, 10), (1350, 100), (194, 214, 214), cv2.FILLED)
            # lm1 = detector.getlmList()[4][1:3]
            # lm2 = detector.getlmList()[8][1:3]
            # print(f"\n/n{calcDistanceBetweenFingers(lm1,lm2)} , {detector.getdistanceBetweenFingersOpenHand()[0]}")
            #
            # lm1 = detector.getlmList()[8][1:3]
            # lm2 = detector.getlmList()[12][1:3]
            # print(f"{calcDistanceBetweenFingers(lm1,lm2)} , {detector.getdistanceBetweenFingersOpenHand()[1]}")
            #
            # lm1 = detector.getlmList()[12][1:3]
            # lm2 = detector.getlmList()[16][1:3]
            # print(f"{calcDistanceBetweenFingers(lm1,lm2)} , {detector.getdistanceBetweenFingersOpenHand()[2]}")
            #
            # lm1 = detector.getlmList()[20][1:3]
            # lm2 = detector.getlmList()[4][1:3]
            # print(f"{calcDistanceBetweenFingers(lm1,lm2)} , {detector.getdistanceBetweenFingersOpenHand()[4]}")
            # time.sleep(1.5)
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