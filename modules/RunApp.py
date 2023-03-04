import select
import sys
import time

import cv2

from HandDetectionModule import HandDetector
from HandFunctions import Features

last_click = [(0, 0)]
global feature_to_play, back_to_menu_flag, EXIT

back_to_menu_flag = False
feature_to_play = -1
EXIT = False


def detect_double_click(event, x, y, flags, param):
    global last_click
    if event == cv2.EVENT_LBUTTONDOWN:
        last_click.append((x, y))
        print(last_click[-1])


def timeout_input(timeout, prompt="", timeout_value=None):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n')
    else:
        sys.stdout.write('\n')
        sys.stdout.flush()
        return timeout_value


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


def drawMenu(img, draw_menu, draw_back_to_menu):
    global feature_to_play, back_to_menu_flag, EXIT
    up_left_rec_pos = (100, 100)
    right_down_rec_pos = (450, 200)
    backround_color = (187, 240, 201)
    border_color = (43, 237, 95)

    cv2.setMouseCallback('Hey', detect_double_click, img)
    last_click_point = last_click[-1]

    if draw_menu:

        cv2.putText(img, "Enter in the terminal your selection", (120, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.rectangle(img, up_left_rec_pos, right_down_rec_pos, backround_color, cv2.FILLED)
        cv2.rectangle(img, up_left_rec_pos, right_down_rec_pos, border_color, thickness=2)
        cv2.putText(img, "Drag rectangle - 1", (120, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        if point_in_rectangle(last_click_point, up_left_rec_pos, right_down_rec_pos):
            feature_to_play = 1

        up_left_rec_pos = (up_left_rec_pos[0], up_left_rec_pos[1] + 100)
        right_down_rec_pos = (right_down_rec_pos[0], right_down_rec_pos[1] + 100)

        cv2.rectangle(img, up_left_rec_pos, right_down_rec_pos, backround_color, cv2.FILLED)
        cv2.rectangle(img, up_left_rec_pos, right_down_rec_pos, border_color, thickness=2)
        cv2.putText(img, "Control mouse - 2", (120, 260), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        if point_in_rectangle(last_click_point, up_left_rec_pos, right_down_rec_pos):
            feature_to_play = 2

        up_left_rec_pos = (up_left_rec_pos[0], up_left_rec_pos[1] + 100)
        right_down_rec_pos = (right_down_rec_pos[0], right_down_rec_pos[1] + 100)

        cv2.rectangle(img, up_left_rec_pos, right_down_rec_pos, backround_color, cv2.FILLED)
        cv2.rectangle(img, up_left_rec_pos, right_down_rec_pos, border_color, thickness=2)
        cv2.putText(img, "Free Draw - 3", (120, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        if point_in_rectangle(last_click_point, up_left_rec_pos, right_down_rec_pos):
            feature_to_play = 3

    if draw_back_to_menu:
        cv2.rectangle(img, (1600, 100), (1850, 200), border_color, thickness=2)
        cv2.putText(img, "Back to menu", (1625, 175), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        if point_in_rectangle(last_click_point, (1400, 100), (1850, 200)):
            back_to_menu_flag = True
            feature_to_play = -1

    if point_in_rectangle(last_click_point, (1600, 250), (1850, 350)):
        EXIT = True

        return img
    return img


def main():
    # previous an current time
    pre_time = 0
    cur_time = 0

    # Receive video from camera 0
    cap = cv2.VideoCapture(0)

    detector = HandDetector()
    all_feature = Features(detector)

    # detector.initialize_hand_size(2)
    print("Done init, starting app...")
    i = 0

    draw_menu = True
    back_to_menu = False

    while not EXIT:
        success, img = cap.read()
        # Draw the functions menu
        img = drawMenu(cv2.flip(img, 1), draw_menu, back_to_menu)
        # draw hands landmarks on the img
        img = detector.find_hands(img)
        # return the landmark_list
        landmark_list = detector.get_landmark_position(img)
        # Define the landmark_list in the class
        all_feature.set_variables(landmark_list, img)

        cv2.rectangle(img, (1600, 250), (1850, 350), (200, 120, 0), thickness=2)
        cv2.putText(img, "EXIT", (1625, 325), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4)

        # Only if hand is detected:
        try:
            if landmark_list:

                if all_feature.hand_is_close():
                    cv2.rectangle(img, (830, 60), (1090, 130), (194, 214, 214), cv2.FILLED)
                    cv2.putText(img, "Hand Is Close", (850, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)


                if feature_to_play == -1:
                    draw_menu = True
                    back_to_menu = False
                    print("in 0")


                elif feature_to_play == 1:
                    img = all_feature.drag_rectangle()
                    cv2.putText(img, "running - drag rectangle ", (850, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    print("in 1")


                elif feature_to_play == 2:
                    all_feature.move_mouse()
                    cv2.putText(img, "running - move mouse", (850, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    print("in 2")


                elif feature_to_play == 3:
                    board = all_feature.free_draw(i, paint_color='pink', thickness='large')
                    cv2.putText(img, "running - free draw", (850, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    cv2.imshow('board', board)
                    print("in 3")

                else:
                    print("els")

                if feature_to_play != -1:
                    draw_menu = False
                    back_to_menu = True

            else:
                cv2.putText(img, "Hand is not detected", (850, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        except Exception as e:  # work on python 3.x
            print('Failed app ' + str(e))

        # Calc the fps
        cur_time = time.time()
        fps = 1 / (cur_time - pre_time)
        pre_time = cur_time

        # Show FPS on video
        cv2.putText(img, f"FPS: {str(int(fps))}", (1750, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

        # Show window with img
        cv2.imshow("Hey", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
