import cv2
import mediapipe as mp
import time

class handDetector():
    """
    Hand detector class
    """
    def __init__(self, mode=False, max_hands=2, min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        """Initializes a Hand Hand object.
               Args:
                 static_image_mode: Whether to treat the input images as a batch of static
                   and possibly unrelated images, or a video stream. See details in
                 max_num_hands: Maximum number of hands to detect. See details in
                 min_detection_confidence: Minimum confidence value ([0.0, 1.0]) for hand
                   detection to be considered successful. See details in
                 min_tracking_confidence: Minimum confidence value ([0.0, 1.0]) for the
                   hand landmarks to be considered tracked successfully. See details in
               """
        self.mode = mode
        self.maxHands = max_hands
        self.minDetection = min_detection_confidence
        self.minTracking = min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.minDetection,
                                        min_tracking_confidence=self.minTracking, model_complexity=0)

        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        """
        Finding the hands
        :param img:
        :param draw: will the connection between the landmarks
        :return: the img after drawing if requested
        """

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        # Only if there is detection
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def getLendmarkPosition(self, img, handNo=0, draw=True):
        """
        Getting the landmarks location on array.
        Can draw on the center of the hand a circle
        :param img: the captured img
        :param handNo: Amount of hand to get
        :param draw: True by default, will add a circle on HCP
        :return: the array with all the 20 landmarks
        """

        # the list with all the landmarks
        self.lmList = []
        # Only if there is detection
        if self.result.multi_hand_landmarks:
            # Take only 1 hand (Hand number 0)
            detectedHand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(detectedHand.landmark):
                # get x,y landmarks positions
                lmX = lm.x
                lmY = lm.y

                # Convert lmX, lmY tp pixel location
                h, w, c = img.shape
                cx, cy = int(lmX * w), int(lmY * h)
                #print(f"ID:{id}, {cx, cy}")
                self.lmList.append([id, cx, cy])

                if draw:
                    # Only when there is at least 9 landmarks
                    if len(self.lmList) > 9:
                        # Calc the center of the hand
                        self.calcHCP()
                        # Draw the Circle on the center of the hand
                        cv2.circle(img, (self.handCenterPos), 10, (154, 239, 192), cv2.FILLED)
            self.setFingers()
            return self.lmList

    def calcHCP(self):
        """
        Calc the hand center position
        Taking the middle of the line between lm 0 to ln 9
        """
        xHandCenter = int((self.lmList[9][1] + self.lmList[0][1]) / 2)
        yHandCenter = int((self.lmList[9][2] + self.lmList[0][2]) / 2)
        self.handCenterPos = (xHandCenter, yHandCenter)

    def getHCP(self):
        """
        :return: the Hand Center Position
        """
        return self.handCenterPos

    def getlmList(self):
        return  self.lmList

    def setFingers(self):  # setting finger lendmarks
        self.lm0 = self.lmList[0][1:3]
        self.lm2 = self.lmList[2][1:3]
        self.lm4 = self.lmList[4][1:3]
        self.lm3 = self.lmList[3][1:3]
        self.lm5 = self.lmList[5][1:3]
        self.lm8 = self.lmList[8][1:3]
        self.lm9 = self.lmList[9][1:3]
        self.lm12 = self.lmList[12][1:3]
        self.lm13 = self.lmList[13][1:3]
        self.lm16 = self.lmList[16][1:3]
        self.lm17 = self.lmList[17][1:3]
        self.lm20 = self.lmList[20][1:3]

    def calcDistanceBetweenFingers(self, f1, f2):
        return ((((f2[0] - f1[0]) ** 2) + ((f2[1] - f1[1]) ** 2)) ** 0.5)

    def addAvgDistance(self, count):
        self.distanceBetweenFingersOpenHand[0] = (int(self.distanceBetweenFingersOpenHand[0]
                                                      + self.calcDistanceBetweenFingers(self.lm4, self.lm8)) / count)
        self.distanceBetweenFingersOpenHand[1] = (int(self.distanceBetweenFingersOpenHand[1]
                                                      + self.calcDistanceBetweenFingers(self.lm8, self.lm12)) / count)
        self.distanceBetweenFingersOpenHand[2] = (int(self.distanceBetweenFingersOpenHand[2]
                                                      + self.calcDistanceBetweenFingers(self.lm12,self.lm16)) / count)
        self.distanceBetweenFingersOpenHand[3] = (int(self.distanceBetweenFingersOpenHand[3]
                                                      + self.calcDistanceBetweenFingers(self.lm16,self.lm20)) / count)
        self.distanceBetweenFingersOpenHand[4] = (int(self.distanceBetweenFingersOpenHand[4]
                                                      + self.calcDistanceBetweenFingers(self.lm20, self.lm4)) / count)
    def initHandSize(self):
        def pointIsInCircle(center_x,center_y,R,p_x,p_y):
            return (p_x-center_x) **2 + (p_y-center_y)**2 < R**2

        initStates = [
            {0 : "Waiting"},
            {1 : "Ready To Start"},
            {2 : "Taking Samples"},
            {3: "Done"},
        ]
        currentState = 0
        self.distanceBetweenFingersOpenHand = [0,0,0,0,0]
        # place 0: dis between lm4-lm8
        # place 1: dis between lm8-lm12
        # place 2: dis between lm12-l16
        # place 3: dis between lm16-lm20
        # place 4: dis between lm20-lm4
        countInitTimes = 5
        secForInit = 5
        startTime = time.time()

        cap = cv2.VideoCapture(0)

        while True > 0:

            success, img = cap.read()
            img = self.findHands(img)
            self.LmList = self.getLendmarkPosition(img)
            img = cv2.flip(img, 1)

            # Start init
            if (currentState == 0):
                cv2.putText(img, f"Lest Start the initialization! Open and place your hand in the middle of the screen", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                if(self.lmList):
                    sec = 5
                    cv2.putText(img,f"Place your hand above the circle ",(450, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
                    cv2.circle(img, (1100,650), 70, (154, 239, 192), cv2.FILLED)
                    cv2.putText(img, f"Hold for more {secForInit} second ", (550, 350), cv2.FONT_HERSHEY_SIMPLEX, 2,
                                (255, 0, 0), 2)
                    if(pointIsInCircle(1100,650,70,self.getHCP()[0]+220,self.getHCP()[1]) and (time.time() - startTime >= 1)):
                        secForInit -= 1
                        startTime = time.time()
                    if(secForInit == 0):
                        currentState += 1



            elif(currentState == 1):
                cv2.putText(img, (f"Taking {6 - countInitTimes} sampling of 5"), (750, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
                if(self.lmList and (time.time() - startTime) >= 1):
                    self.addAvgDistance(6-countInitTimes)
                    startTime = time.time()
                    countInitTimes -= 1
                elif (countInitTimes == 0):
                    currentState += 1
            elif(currentState == 2):
                img = cv2.imread("green-check-mark-.jpeg")





            cv2.imshow("Initialize Hand Size", img)
            cv2.waitKey(1)
        print(self.distanceBetweenFingersOpenHand)


def main():
    D = handDetector()

    D.initHandSize()



if __name__ == "__main__":
    main()