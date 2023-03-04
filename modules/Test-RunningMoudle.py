import cv2
import mediapipe as mp
import time

#Recive video from camera 0
cap = cv2.VideoCapture(0)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mpPose = mp.solutions.pose
mpPose.Pose(model_complexity=0)

mpDraw = mp.solutions.drawing_utils

#previus time
pTime = 0
#Current time
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)

    fingerL = []
    #Only if there is detection
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #get x,y landmarks positions
                lmX = lm.x
                lmY = lm.y

                #Convert lmX, lmY tp pixel location
                h, w, c = img.shape
                cx, cy = int(lmX * w), int(lmY * h)

                #Set circle on each landmark
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                fingerL.append((id, (cx, cy)))
                print(f"ID:{id}, {cx, cy}")

            mpDraw.draw_landmarks(img, handLms,mp_hands.HAND_CONNECTIONS)



    #Calc the fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f"FPS: {str(int(fps))}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 3)

    cv2.imshow("Hey ;)",img)
    cv2.waitKey(1)