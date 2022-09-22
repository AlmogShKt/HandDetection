import cv2
from HandDetectionModule import handDetector, calcDistanceBetweenFingers


class Features:
    """

    """
    def __init__(self,detector):
        """

        """
        self.detector = detector
        self.relativeScaleForCloseHand = [0,0,0,0,0]

        #self.lmList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def setFingers(self,lmList):
        try:
            self.lmList = lmList

            self.f0 = self.lmList[0][1:3]
            self.f2 = self.lmList[2][1:3]
            self.f4 = self.lmList[4][1:3]
            self.f3 = self.lmList[3][1:3]
            self.f5 = self.lmList[5][1:3]
            self.f8 = self.lmList[8][1:3]
            self.f9 = self.lmList[9][1:3]
            self.f12 = self.lmList[12][1:3]
            self.f13 = self.lmList[13][1:3]
            self.f16 = self.lmList[16][1:3]
            self.f17 = self.lmList[17][1:3]
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

    def handIsClose(self,lmList):
        self.setFingers(lmList)
        """

        :param lmList:
        :return:
        """

        if self.lmList:
            if calcDistanceBetweenFingers(self.f4, self.f8) < self.relativeScaleForCloseHand[0] \
                    and calcDistanceBetweenFingers(self.f8,self.f12) < self.relativeScaleForCloseHand[1] \
                    and calcDistanceBetweenFingers(self.f12, self.f16) < self.relativeScaleForCloseHand[2] \
                    and calcDistanceBetweenFingers(self.f16,self.f20) < self.relativeScaleForCloseHand[3] \
                    and calcDistanceBetweenFingers(self.f4, self.f20) < self.relativeScaleForCloseHand[4]:
                return True


    def printDisForTest(self, lmList):
        self.setFingers(lmList)
        print(self.detector.distanceBetweenFingers(self.f4, self.f8))
