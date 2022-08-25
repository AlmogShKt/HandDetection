import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, max_hands=2, min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
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
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self.hands.process(imgRGB)

        # Only if there is detection
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def getLendmarkPosition(self,handLms, img):
        for id, lm in enumerate(handLms.landmark):
            #get x,y landmarks positions
            lmX = lm.x
            lmY = lm.y

            #Convert lmX, lmY tp pixel location
            h, w, c = img.shape
            cx, cy = int(lmX * w), int(lmY * h)

            #Set circle on each landmark
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            print(f"ID:{id}, {cx, cy}")

