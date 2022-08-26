import cv2
import mediapipe as mp

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
                print(f"ID:{id}, {cx, cy}")
                self.lmList.append([id, cx, cy])

                if draw:
                    # Only when there is at least 9 landmarks
                    if len(self.lmList) > 9:
                        # Calc the center of the hand
                        self.calcHCP()
                        # Draw the Circle on the center of the hand
                        cv2.circle(img, (self.handCenterPos), 10, (154, 239, 192), cv2.FILLED)
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
