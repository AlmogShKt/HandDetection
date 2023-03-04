from HandDetectionModule import HandDetector, calc_distance_between_fingers
from HandFunctions import Features
import cv2
import time


def drawMenu(img, draw):
    if draw:
        cv2.rectangle(img, (70, 10), (310, 100), (153, 153, 253), cv2.FILLED)
        cv2.rectangle(img, (70, 10), (310, 100), (0, 0, 255))
        cv2.putText(img, "Function 1", (100, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.rectangle(img, (70, 110), (310, 200), (153, 153, 253), cv2.FILLED)
        cv2.rectangle(img, (70, 110), (310, 200), (0, 0, 255))
        cv2.putText(img, "Function 2", (100, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.rectangle(img, (70, 210), (310, 300), (153, 153, 253), cv2.FILLED)
        cv2.rectangle(img, (70, 210), (310, 300), (0, 0, 255))
        cv2.putText(img, "Function 3", (100, 260), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.rectangle(img, (70, 310), (310, 400), (153, 153, 253), cv2.FILLED)
        cv2.rectangle(img, (70, 310), (310, 400), (0, 0, 255))
        cv2.putText(img, "Function 4", (100, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.rectangle(img, (70, 410), (310, 500), (153, 153, 253), cv2.FILLED)
        cv2.rectangle(img, (70, 410), (310, 500), (0, 0, 255))
        cv2.putText(img, "Function 5", (100, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

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

    detector.initialize_hand_size()
    print("Done init, starting app...")
    i = 0
    while True:
        success, img = cap.read()
        # Draw the functions menu
        img = drawMenu(cv2.flip(img, 1), False)
        # draw hands landmarks on the img
        img = detector.find_hands(img)
        # return the landmark_list
        landmark_list = detector.get_landmark_position(img)
        # Define the landmark_list in the class
        all_feature.set_variables(landmark_list, img)

        # Only if hand is detected:
        try:
            if landmark_list:
                if all_feature.hand_is_close():
                    cv2.rectangle(img, (590, 10), (830, 100), (194, 214, 214), cv2.FILLED)
                    cv2.putText(img, "Hand Is Close", (600, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                #img = all_feature.drag_rectangle()
                #all_feature.move_mouse()
                i += 1
                board = all_feature.free_draw(i,paint_color='pink', thickness='large')
                cv2.imshow('board',board)

            else:
                cv2.putText(img, "Hand is not detected", (600, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
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