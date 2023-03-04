import time
import cv2
import mediapipe as mp


# Static function:
def calc_distance_between_fingers(lm1, lm2):
    """
    Calc the distance between 2 given landmarks
    :param lm1:
    :param lm2:
    :return: the distance(in pixels)
    """
    res = (((lm2[0] - lm1[0]) ** 2) + ((lm2[1] - lm1[1]) ** 2)) ** 0.5
    return res


class HandDetector:
    """
    Hand detector class
    """

    def __init__(self, mode=False, max_hands=2, min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        """ç a Hand Hand object.
               Args:
                 static_image_mode: Whether to treat the input images as a batch of static
                   and possibly unrelated images, or a video stream. See details in
                 max_num_hands: Maximum number of hands to detect. See details in
                 min_detection_confidence: Minimum confidence value ([0.0, 1.0]) for hand
                   detection to be considered successful. See details in
                 min_tracking_confidence: Minimum confidence value ([0.0, 1.0]) for the
                   hand landmarks to be considered tracked successfully. See details in
               """
        self.distance_between_fingers_open_hand = [0, 0, 0, 0, 0]
        self.mode = mode
        self.max_hands = max_hands
        self.min_detection = min_detection_confidence
        self.min_tracking = min_tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=self.mode, max_num_hands=self.max_hands,
                                         min_detection_confidence=self.min_detection,
                                         min_tracking_confidence=self.min_tracking, model_complexity=0)

        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
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
                    self.mpDraw.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_landmark_position(self, img, hand_number=0, draw=True):
        """
        Getting the landmarks location on array.
        Can draw on the center of the hand a circle
        :param img: the captured img
        :param hand_number: Amount of hand to get
        :param draw: True by default, will add a circle on HCP
        :return: the array with all the 20 landmarks
        """
        # the list with all the landmarks
        self.landmark_list = []

        # Only if there is detection
        if self.result.multi_hand_landmarks:
            # Take only 1 hand (Hand number 0)
            detected_hand = self.result.multi_hand_landmarks[hand_number]
            for lm_id, lm in enumerate(detected_hand.landmark):
                # get x,y landmarks positions
                lmX = lm.x
                lmY = lm.y

                # Convert lmX, lmY tp pixel location
                h, w, c = img.shape
                cx, cy = int(lmX * w), int(lmY * h)

                self.landmark_list.append([lm_id, cx, cy])

                if draw and len(self.landmark_list) > 9:
                    # Only when there is at least 9 landmarks
                    # Calc the center of the hand
                    self.calculate_hand_center_position()
                    # Draw the Circle on the center of the hand
                    cv2.circle(img, self.hand_center_position, 10, (154, 239, 192), cv2.FILLED)
            self.set_fingers()
            return self.landmark_list

    def calculate_hand_center_position(self):
        """
        calculate the hand center position
        Taking the middle of the line between lm 0 to ln 9
        """
        hand_center_x = int((self.landmark_list[9][1] + self.landmark_list[0][1]) / 2)
        hand_center_y = int((self.landmark_list[9][2] + self.landmark_list[0][2]) / 2)
        self.hand_center_position = (hand_center_x, hand_center_y)

    def get_hand_center_position(self):
        """
        :return: the Hand Center Position
        """
        return self.hand_center_position

    def get_landmark_list(self):
        """
        :return: landmarks list
        """
        return self.landmark_list

    def set_fingers(self):
        """
        Set all relevant landmarks as class variables
        :return:
        """
        self.lm0 = self.landmark_list[0][1:3]
        self.lm2 = self.landmark_list[2][1:3]
        self.lm4 = self.landmark_list[4][1:3]
        self.lm3 = self.landmark_list[3][1:3]
        self.lm5 = self.landmark_list[5][1:3]
        self.lm8 = self.landmark_list[8][1:3]
        self.lm9 = self.landmark_list[9][1:3]
        self.lm12 = self.landmark_list[12][1:3]
        self.lm13 = self.landmark_list[13][1:3]
        self.lm16 = self.landmark_list[16][1:3]
        self.lm17 = self.landmark_list[17][1:3]
        self.lm20 = self.landmark_list[20][1:3]

    def add_avg_distance(self, count):
        """
        Create avg of the distance between top of each finger
        :param count: the current count of sum
        :return:
        """
        self.distance_between_fingers_open_hand[0] = (int(self.distance_between_fingers_open_hand[0]
                                                          + calc_distance_between_fingers(self.lm4, self.lm8)))
        self.distance_between_fingers_open_hand[1] = (int(self.distance_between_fingers_open_hand[1]
                                                          + calc_distance_between_fingers(self.lm8, self.lm12)))
        self.distance_between_fingers_open_hand[2] = (int(self.distance_between_fingers_open_hand[2]
                                                          + calc_distance_between_fingers(self.lm12, self.lm16)))
        self.distance_between_fingers_open_hand[3] = (int(self.distance_between_fingers_open_hand[3]
                                                          + calc_distance_between_fingers(self.lm16, self.lm20)))
        self.distance_between_fingers_open_hand[4] = (int(self.distance_between_fingers_open_hand[4]
                                                          + calc_distance_between_fingers(self.lm20, self.lm4)))

        if count == 5:
            for i in range(len(self.distance_between_fingers_open_hand)):
                self.distance_between_fingers_open_hand[i] = self.distance_between_fingers_open_hand[i] / count

    def initialize_hand_size(self, start_state=0):
        """
        Initializes the hand size in order to get a relative size for future calculations
        The user needs to place his hand in the middle of the screen for 5 seconds, after that the system will calc the
        avg distance between his finger, and save it.
        :param start_state: Option to start the rin form specific state for test, def should be 0!
        :return: True when done the process
        """

        def is_point_in_circle(center_x, center_y, R, p_x, p_y):
            """
            Check if given point is in given circle
            :param center_x: X center of the circle
            :param center_y: Y center of the circle
            :param R: Radius of the circle
            :param p_x: X center of the point
            :param p_y: Y center of the point
            :return: True if the point is in the circle
            """
            return (p_x - center_x) ** 2 + (p_y - center_y) ** 2 < R ** 2

        wait_key = 1

        # All the sates in the process:
        # Waiting for user to place and hold the hand in the middle of the screen for 5 second
        init_states = {0: "Waiting",
                       # Taking 5 samples of the distance of the tip of each finger, and calc the avg of that
                       1: "Taking Samples",
                       # Finish initialize - ready to start the program
                       2: "Done"}

        # The current state, start with 0
        current_state = start_state

        # The distance between the top of each finger
        # place 0: dis between lm4-lm8
        # place 1: dis between lm8-lm12
        # place 2: dis between lm12-l16
        # place 3: dis between lm16-lm20
        # place 4: dis between lm20-lm4

        # Hold the hand for 5 sec before start taking samples
        seconds_for_init = 5
        # the amount of samples to take fot the avg
        amount_of_samples_left = 5
        # Wait 5 sec before end the proses
        hold_for_seconds = 5

        start_time = time.time()
        cap = cv2.VideoCapture(0)
        flag = True
        while flag:
            success, img = cap.read()
            img = self.find_hands(img)
            self.landmark_list = self.get_landmark_position(img)
            # flip the img
            img = cv2.flip(img, 1)

            if current_state == 0:
                # instruction for user
                cv2.rectangle(img, (10, 10), (1350, 100), (194, 214, 214), cv2.FILLED)
                cv2.putText(img, f"Lets Start the initialization! Open and place your hand in the middle of the screen",
                            (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                # Only when hand is detect
                if self.landmark_list:
                    cv2.putText(img, f"Place your hand in the middle of the screen", (300, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
                    cv2.putText(img, f"Hold for more {seconds_for_init} second ", (550, 300), cv2.FONT_HERSHEY_SIMPLEX,
                                2,
                                (255, 0, 0), 2)
                    # Only if the HCP in in the middle of the screen and 1 sec passed - count down
                    if (is_point_in_circle(1100, 650, 100, self.get_hand_center_position()[0] + 220,
                                           self.get_hand_center_position()[1]) and (
                            time.time() - start_time >= 1)):
                        seconds_for_init -= 1
                        # Update the start time
                        start_time = time.time()
                    # When 5 sec passed - move to the next step
                    if seconds_for_init == 0:
                        current_state += 1
            # Start taking samples of the hand, and update the avg
            elif current_state == 1:
                cv2.putText(img, f"Taking {6 - amount_of_samples_left} sampling of 5", (750, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
                # Only if the HCP in in the middle of the screen and 1 sec passed - count down
                if self.landmark_list and (time.time() - start_time) >= 1:
                    # up==Update the avg
                    self.add_avg_distance(6 - amount_of_samples_left)
                    start_time = time.time()
                    amount_of_samples_left -= 1
                # After taking 5 samples move to the next step
                elif amount_of_samples_left == 0:
                    current_state += 1
            # Done!
            elif current_state == 2:
                wait_key = 0
                print(hold_for_seconds)
                img = cv2.imread("photos/All_Set_img.png")
                # Show the image for 5 sec the end the init' process
            elif current_state == 9:
                return
            try:
                cv2.imshow(init_states[current_state], img)
                cv2.waitKey(wait_key)
                if wait_key == 0:
                    cv2.destroyAllWindows()
                    break
            except Exception as err:
                print(init_states[current_state])
                print(f"Failed on initHands - {err}")

    def get_distance_between_fingers_open_hand(self):
        return self.distance_between_fingers_open_hand


# test!
def main():
    D = HandDetector()
    D.initialize_hand_size()


if __name__ == "__main__":
    main()
