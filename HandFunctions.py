import cv2
from HandDetectionModule import handDetector



class Features():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = handDetector()



    def setFingers(self,lmList):  # setting finger lendmarks
        self.f0 = lmList[0][1:3]
        self.f2 = lmList[2][1:3]
        self.f4 = lmList[4][1:3]
        self.f3 = lmList[3][1:3]
        self.f5 = lmList[5][1:3]
        self.f8 = lmList[8][1:3]
        self.f9 = lmList[9][1:3]
        self.f12 = lmList[12][1:3]
        self.f13 = lmList[13][1:3]
        self.f16 = lmList[16][1:3]
        self.f17 = lmList[17][1:3]
        self.f20 = lmList[20][1:3]

    def handIsClose(self, lmList):
        self.setFingers(lmList)

        if self.detector.calcDistanceBetweenFingers(self.f4, self.f8) < 50 and self.detector.calcDistanceBetweenFingers(self.f8,
                                                                                                                self.f12) < 30 and self.detector.calcDistanceBetweenFingers(
                self.f12, self.f16) < 25 and self.detector.calcDistanceBetweenFingers(self.f16,
                                                                                  self.f20) < 25 and self.detector.calcDistanceBetweenFingers(
                self.f4, self.f20) < 83:

            return True

        else:  # In case the hand is open
            return False

    def printDisForTest(self, lmList):
        self.setFingers(lmList)
        print(self.detector.distanceBetweenFingers(self.f4, self.f8))
