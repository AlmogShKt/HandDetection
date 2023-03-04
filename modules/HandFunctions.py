import cv2
from pynput.mouse import Button, Controller
from screeninfo import get_monitors

from HandDetectionModule import calc_distance_between_fingers
from BoardFunctions import Board


# Static function:
def get_primary_screen_info():
    primary_screen_info = ""
    for monitor in get_monitors():
        if monitor.is_primary:
            primary_screen_info = monitor
    return primary_screen_info


def point_in_rectangle(lm, rect_left_up_point, rect_right_down_point):
    """
    Check if point is within a rectangle
    :param lm: the point (landmark)
    :param rect_left_up_point: Left Up point of the rectangle
    :param rect_right_down_point:  Right Down point of the rectangle
    :return: True if the point is within the rectangle otherwise False
    """
    x1, y1 = rect_left_up_point[0], rect_left_up_point[1]
    w = abs(rect_right_down_point[0] - rect_left_up_point[0])
    h = abs(rect_right_down_point[1] - rect_left_up_point[1])

    x2, y2 = x1 + w, y1 + h
    x, y = lm[0], lm[1]

    if x1 < x < x2:
        if y1 < y < y2:
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
        self.relative_scale_for_close_hand = [0, 0, 0, 0, 0]
        self.img = img

        # Variables for dedicated functions:
        # For frag rectangles:
        # First Values:
        self.rectangle_x_position = 750
        self.rectangle_y_position = 500

        self.screen_info = get_primary_screen_info()

    def set_variables(self, landmark_list, img):
        """
        Sets all the class variables
        :param landmark_list:
        :param img:
        :return:
        """
        self.set_landmark_list(landmark_list)
        self.set_img(img)

    def set_fingers(self, ):
        try:
            self.f0 = self.landmark_list[0][1:3]
            self.f2 = self.landmark_list[2][1:3]
            self.f4 = self.landmark_list[4][1:3]
            self.f3 = self.landmark_list[3][1:3]
            self.f5 = self.landmark_list[5][1:3]
            self.f6 = self.landmark_list[6][1:3]
            self.f8 = self.landmark_list[8][1:3]
            self.f9 = self.landmark_list[9][1:3]
            self.f10 = self.landmark_list[10][1:3]
            self.f12 = self.landmark_list[12][1:3]
            self.f13 = self.landmark_list[13][1:3]
            self.f14 = self.landmark_list[14][1:3]
            self.f16 = self.landmark_list[16][1:3]
            self.f17 = self.landmark_list[17][1:3]
            self.f18 = self.landmark_list[18][1:3]
            self.f20 = self.landmark_list[20][1:3]

            if not self.detector.get_distance_between_fingers_open_hand()[0] == 0:
                self.relative_scale_for_close_hand = [
                    self.detector.get_distance_between_fingers_open_hand()[0] * 0.5,
                    self.detector.get_distance_between_fingers_open_hand()[1] * 0.5,
                    self.detector.get_distance_between_fingers_open_hand()[2] * 0.5,
                    self.detector.get_distance_between_fingers_open_hand()[3] * 0.5,
                    self.detector.get_distance_between_fingers_open_hand()[4] * 0.5
                ]
            else:
                # for tests..
                self.relative_scale_for_close_hand = [298.2, 101.4, 83.6, 121.0, 441.4]
        except Exception as err:
            print(f"Failed on setFinger - {err}")

    def set_img(self, img):
        self.img = img
        return

    def set_landmark_list(self, landmark_list):
        self.landmark_list = landmark_list
        return

    def hand_is_close(self):
        """
                Detect if the hands is close 
                :return: True if the hand is close
                """
        self.set_fingers()

        if self.landmark_list:
            if self.f8[1] > self.f5[1] and self.f12[1] > self.f9[1] and self.f16[1] > self.f13[1] and self.f20[1] > \
                    self.f17[1]:
                return True
            else:
                return False

            # Another but less reliable way to check if the hand is close
            # if calc_distance_between_fingers(self.f4, self.f8) < self.relative_scale_for_close_hand[0]+20 \
            #         and calc_distance_between_fingers(self.f8,self.f12) < self.relative_scale_for_close_hand[1] \
            #         and calc_distance_between_fingers(self.f12, self.f16) < self.relative_scale_for_close_hand[2] \
            #         and calc_distance_between_fingers(self.f16,self.f20) < self.relative_scale_for_close_hand[3] \
            #         and calc_distance_between_fingers(self.f4, self.f20) < self.relative_scale_for_close_hand[4]:
            #     return True

    def print_dis_for_test(self):
        self.set_fingers()
        # print(self.detector.distanceBetweenFingers(self.f4, self.f8))

    def get_screen_info(self):
        return self.screen_info

    def fingers_are_close(self):
        """
        Check if lm8 and lm12 are close -> the finger are "close"
        :return: True if the finger are close otherwise False
        """
        dis = calc_distance_between_fingers(self.f8, self.f12)
        # Only if the hand is NOT close AND the distance is smaller the the relative size
        return dis < self.relative_scale_for_close_hand[1] and not self.hand_is_close()

    def drag_rectangle(self):
        """
        Function 1
        Drag a rectangle with your fingers, Create the "Peace" sign with your fingers,
        place your hand within the circle and "close" the 2 fingers when you want to drag the rectangle
        Open the finger to stop dragging the rectangle
        :return: the img with the rectangle
        """
        # Draw the rectangle
        cv2.rectangle(self.img, (self.rectangle_x_position, self.rectangle_y_position),
                      (self.rectangle_x_position + 250, self.rectangle_y_position + 250), (194, 0, 214), 2)

        # Check if the lm is within the rectangle
        is_point_in_rectangle = point_in_rectangle((int(self.f8[0]), int(self.f8[1])),
                                                   (self.rectangle_x_position, self.rectangle_y_position),
                                                   (self.rectangle_x_position + 250, self.rectangle_y_position + 250))

        # only if the 'finger are close' and the lm is within the rectangle - change the positing of the rectangle
        # The lm is the center of the rectangle new position
        if self.fingers_are_close() and is_point_in_rectangle:
            # Original equation :
            # Xcenter(lm8[0]) = (x1 + x2(x1+250))/2
            # Ycenter(lm8[1]) = (y1 + y2(x1+250))/2

            # Set the right up corner of the rectangle (lm 8 is the center of the rectangle)
            self.rectangle_x_position = int((2 * (int(self.f8[0])) - 250) / 2)
            self.rectangle_y_position = int((2 * (int(self.f8[1])) - 250) / 2)

        return self.img

    def move_mouse(self):
        mouse_x_position = (self.f8[0] / 1920) * self.screen_info.width
        mouse_y_position = (self.f8[1] / 1080) * self.screen_info.height
        mouse_x_position = int(mouse_x_position)
        mouse_y_position = int(mouse_y_position)

        mouse = Controller()
        mouse.move(mouse_x_position, mouse_y_position)
        mouse.position = (mouse_x_position, mouse_y_position)

        if self.fingers_are_close():
            mouse.press(Button.left)
            # print((mouse_x_position, mouse_y_position))
            return (mouse_x_position, mouse_y_position)
        else:
            mouse.release(Button.left)
            # return (mouse_x_position,mouse_y_position)

    def free_draw(self, i, paint_color='black', thickness='small'):
        mouse_x_position = self.f8[0]
        mouse_y_position = self.f8[1]

        self.board.set_drawing_color(paint_color)
        self.board.set_cursor_thickness(thickness)
        self.board.draw(i, mouse_x_position, mouse_y_position)
        return self.board.get_board()


def main():
    b = Board()
    b.draw(mouse_mode=True)
    # img size (2484, 3630, 3)
    # left screen size 1500 #916


if __name__ == "__main__":
    main()