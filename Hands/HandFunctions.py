import cv2
from pynput.mouse import Button, Controller
from screeninfo import get_monitors

from HandDetectionModule import calcDistanceBetweenFingers


# Static function:
def pointInRect(lm, rectLU, rectRD):
    """
    Check if point is within a rectangle
    :param lm: the point (landmark)
    :param rectLU: Left Up point of the rectangle
    :param rectRD:  Right Down point of the rectangle
    :return: True if the point is within the rectangle otherwise False
    """
    x1, y1 = rectLU[0], rectLU[1]
    w = abs(rectRD[0] - rectLU[0])
    h = abs(rectRD[1] - rectLU[1])

    x2, y2 = x1 + w, y1 + h
    x, y = lm[0], lm[1]

    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False


class Features:
    """

    """

    def __init__(self, detector, img=0):
        """

        """
        self.detector = detector

        self.board = Board()

        # The distance between the top of each finger
        # place 0: dis between lm4-lm8
        # place 1: dis between lm8-lm12
        # place 2: dis between lm12-l16
        # place 3: dis between lm16-lm20
        # place 4: dis between lm20-lm4
        self.relativeScaleForCloseHand = [0, 0, 0, 0, 0]
        self.img = img

        # Varibles for dedicated functions:
        # For frag rectangles:
        # First Values:
        self.rectX = 750
        self.rectY = 500

        for m in get_monitors():
            if m.is_primary:
                self.screenInfo = m

    def setVars(self, lmList, img):
        """
        Sets all the class variables
        :param lmList:
        :param img:
        :return:
        """
        self.setLmList(lmList)
        self.setImg(img)

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

            if not self.detector.getdistanceBetweenFingersOpenHand()[0] == 0:
                self.relativeScaleForCloseHand = [
                    self.detector.getdistanceBetweenFingersOpenHand()[0] * 0.5,
                    self.detector.getdistanceBetweenFingersOpenHand()[1] * 0.5,
                    self.detector.getdistanceBetweenFingersOpenHand()[2] * 0.5,
                    self.detector.getdistanceBetweenFingersOpenHand()[3] * 0.5,
                    self.detector.getdistanceBetweenFingersOpenHand()[4] * 0.5
                ]
            else:
                # for tests..
                self.relativeScaleForCloseHand = [298.2, 101.4, 83.6, 121.0, 441.4]
        except:
            print("Failed on setFinger")

    def setImg(self, img):
        self.img = img
        return

    def setLmList(self, lmList):
        self.lmList = lmList
        return

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
        # print(self.detector.distanceBetweenFingers(self.f4, self.f8))

    def getScreenInfo(self):
        return self.screenInfo

    def fingersAreClose(self):
        """
        Check if lm8 and lm12 are close -> the finger are "close"
        :return: True if the finger are close otherwise False
        """
        dis = calcDistanceBetweenFingers(self.f8, self.f12)
        # Only if the hand is NOT close AND the distance is smaller the the relative size
        return dis < self.relativeScaleForCloseHand[1] and not self.handIsClose()

    def dragRectangles(self):
        """
        Function 1
        Drag a rectangle with your fingers, Create the "Peace" sign with your fingers,
        place your hand within the circle and "close" the 2 fingers when you want to drag the rectangle
        Open the finger to stop dragging the rectangle
        :return: the img with the rectangle
        """
        # Draw the rectangle
        cv2.rectangle(self.img, (self.rectX, self.rectY), (self.rectX + 250, self.rectY + 250), (194, 0, 214), 2)

        # Check if the lm is within the rectangle
        inRect = pointInRect((int(self.f8[0]), int(self.f8[1])), (self.rectX, self.rectY),
                             (self.rectX + 250, self.rectY + 250))

        # only if the 'finger are close' and the lm is within the rectangle - change the positing of the rectangle
        # The lm is the center of the rectangle new position
        if self.fingersAreClose() and inRect:
            # Original equation :
            # Xcenter(lm8[0]) = (x1 + x2(x1+250))/2
            # Ycenter(lm8[1]) = (y1 + y2(x1+250))/2

            # Set the right up corner of the rectangle (lm 8 is the center of the rectangle)
            self.rectX = int((2 * (int(self.f8[0])) - 250) / 2)
            self.rectY = int((2 * (int(self.f8[1])) - 250) / 2)

        return self.img

    def moveMouse(self):
        mouseX = (self.f8[0] / 1920) * self.screenInfo.width
        mouseY = (self.f8[1] / 1080) * self.screenInfo.height
        mouseX = int(mouseX)
        mouseY = int(mouseY)

        mouse = Controller()
        mouse.move(mouseX, mouseY)
        mouse.position = (mouseX, mouseY)

        if self.fingersAreClose():
            mouse.press(Button.left)
            # print((mouseX, mouseY))
            return (mouseX, mouseY)
        else:

            mouse.release(Button.left)
            # return (mouseX,mouseY)

    def freeDraw(self,i, paint_color='black', thickness='small'):
        mouseX = self.f8[0]
        mouseY = self.f8[1]

        self.board.set_drawing_color(paint_color)
        self.board.set_cursor_thickness(thickness)
        self.board.draw(i,mouseX,mouseY)
        return self.board.getBoard()


class Board:
    def __init__(self):
        self.board = cv2.imread("/Users/almogshtaigmann/PycharmProjects/HandDetection/photos/CleanBoard.png")
        print(self.board.shape)
        self.drawing_colors = {
            'black': (0, 0, 0),
            'green': (0, 255, 0),
            'red': (0, 0, 255),
            'blue': (255, 0, 0),
            'pink': (213, 86, 245)
        }

        self.cursors_thickness = {
            'small': 30,
            'medium': 50,
            'large': 75
        }
        self.cur_cursor_thickness = self.cursors_thickness['small']
        self.cur_drawing_color = (0, 0, 0)  # by def its black

    def set_cursor_thickness(self, thickness):
        thickness = thickness.lower()
        try:
            self.cur_cursor_thickness = self.cursors_thickness['aa']
        except KeyError:
            self.cur_cursor_thickness = self.cursors_thickness['small']

    def set_drawing_color(self, color):
        color = color.lower()
        try:
            self.cur_drawing_color = self.drawing_colors[color]
        except KeyError:
            # in case that the user insret worng color name - def value
            self.cur_drawing_color = self.drawing_colors['black']

    def loadBoard(self):
        self.board = cv2.imread('/Users/almogshtaigmann/PycharmProjects/HandDetection/Hands/runningBoard.png')

    def draw(self,i, x, y):

        map_X, map_Y = self.setCursorPosotion(x,y)

        self.board[map_Y:map_Y + self.cur_cursor_thickness,
        map_X:map_X + self.cur_cursor_thickness] = self.cur_drawing_color

    def getBoard(self):
        return self.board

    def setCursorPosotion(self, x=0, y=0, mouse_mode=False):
        if mouse_mode:
            mos = Controller()

            x = mos.position[0]
            y = mos.position[1]

        map_X = (x / 1500) * 3630
        if map_X > 3630:
            map_X = 3630

        map_Y = (y / 920) * 2484
        if map_Y > 2484:
            map_Y = 2484

        cursor_position = (int(map_X), int(map_Y))

        return cursor_position



def main():
    pass
    # img size (2484, 3630, 3)
    # left screen size 1500 #916


if __name__ == "__main__":
    main()
