import cv2
import mediapipe as mp
from time import sleep
import threading

capt = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

fingerX = []
fingerY = []
firstValAdded = False

def posFinder():
    while True:
        success, image = capt.read()
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(imageRGB)

    # checking whether a hand is detected
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks: # working with each hand
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # if id == 20 :
                    #     cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                    if id==8:
                        print(str(cx)+', '+str(cy))
                        fingerX.append(cx)
                        fingerY.append(cy)
                        firstValAdded = True



                mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
        cv2.imshow("Output", image)
        cv2.waitKey(1)
def posProc():
    while True:
        while not firstValAdded:
            pass
        sleep(0.25)
        currentX = fingerX[-1]
        for i in range(10):
            if currentX-fingerX[-i]>=250:
                print('Skipped!')
                break

t1=threading.Thread(None, posFinder)
t2=threading.Thread(None, posProc)
t1.start()
t2.start()