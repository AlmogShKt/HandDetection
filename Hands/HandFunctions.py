import time
import cv2
from HandDetectionModule import handDetector, calcDistanceBetweenFingers
from pynput.mouse import Button, Controller
from screeninfo import get_monitors

class Features:
    """

    """
    def __init__(self, detector):
        """

        """
        self.detector = detector

        # The distance between the top of each finger
        # place 0: dis between lm4-lm8
        # place 1: dis between lm8-lm12
        # place 2: dis between lm12-l16
        # place 3: dis between lm16-lm20
        # place 4: dis between lm20-lm4
        self.relativeScaleForCloseHand = [0, 0, 0, 0, 0]

        for m in get_monitors():
            if m.is_primary:
                self.screenInfo = m

    def setFingers(self, ):
        try:


            self.f0 = self.lmList[0][1:3]
            self.f2 = self.lmList[2][1:3]
            self.f4 = self.lmList[4][1:3]
            self.f3 = self.lmList[3][1:3]
            self.f5 = self.lmList[5][1:3]
            self.f6 = self.lmList[6][1:3]
            self.f8 = self.lmList[8][1:3]
            self.f9 = self.lmList[9][1:3]
            self.f10 = self.lmList[10][1:3]
            self.f12 = self.lmList[12][1:3]
            self.f13 = self.lmList[13][1:3]
            self.f14 = self.lmList[14][1:3]
            self.f16 = self.lmList[16][1:3]
            self.f17 = self.lmList[17][1:3]
            self.f18 = self.lmList[18][1:3]
            self.f20 = self.lmList[20][1:3]
            self.relativeScaleForCloseHand = [
                self.detector.getdistanceBetweenFingersOpenHand()[0] * 0.5,
                self.detector.getdistanceBetweenFingersOpenHand()[1] * 0.5,
                self.detector.getdistanceBetweenFingersOpenHand()[2] * 0.5,
                self.detector.getdistanceBetweenFingersOpenHand()[3] * 0.5,
                self.detector.getdistanceBetweenFingersOpenHand()[4] * 0.5
            ]
        except:
            print("No lmList")
    def setLmList(self,lmList):
        self.lmList = lmList
    def handIsClose(self):
        self.setFingers()
        """
        Detect if the hands is close 
        :return: True if the hand is close
        """
        if self.lmList:
            if self.f8[1] > self.f5[1] and self.f12[1] > self.f9[1] and self.f16[1] > self.f13[1] and self.f20[1] > \
                    self.f17[1]:
                return True
            else:
                return False

            # Another but less reliable way to check if the hand is close
            # if calcDistanceBetweenFingers(self.f4, self.f8) < self.relativeScaleForCloseHand[0]+20 \
            #         and calcDistanceBetweenFingers(self.f8,self.f12) < self.relativeScaleForCloseHand[1] \
            #         and calcDistanceBetweenFingers(self.f12, self.f16) < self.relativeScaleForCloseHand[2] \
            #         and calcDistanceBetweenFingers(self.f16,self.f20) < self.relativeScaleForCloseHand[3] \
            #         and calcDistanceBetweenFingers(self.f4, self.f20) < self.relativeScaleForCloseHand[4]:
            #     return True

    def printDisForTest(self, lmList):
        self.setFingers(lmList)
        print(self.detector.distanceBetweenFingers(self.f4, self.f8))

    def getScreenInfo(self):
        return self.screenInfo

    def moveMouse(self):
        mouseX = (self.f8[0] / 1920) * self.screenInfo.width
        mouseY = (self.f8[1] / 1080) * self.screenInfo.height

        mouse = Controller()
        mouse.move(mouseX, mouseY)
        mouse.position = (mouseX, mouseY)

        dis = calcDistanceBetweenFingers(self.f8,self.f12)
        if dis < self.relativeScaleForCloseHand[1] and not self.handIsClose():
            mouse.press(Button.left)
        else:
            mouse.release(Button.left)
            print(self.relativeScaleForCloseHand[1])

