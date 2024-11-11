import sys
sys.path.append("d:/Coding Stuff/Music Gestures/Lib/site-packages")
import cv2
import mediapipe as mp
from time import sleep
from pynput.keyboard import Key, Controller
keyboard = Controller()

capt = cv2.VideoCapture(1)
capt.set(cv2.CAP_PROP_FPS, 30)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

fingerX = [0,0,0,0,0,0,0,0,0,0,0]
palmDetect = [0,0,0,0,0,0,0,0,0,0]
fingerY = [0,0,0,0,0,0,0,0,0,0,0]
firstValAdded = False
palmDetectToler = 150
fingerYToler = 65
gracePeriod = 3
prevRewind = False

def clearArrays():
    global fingerX, palmDetect, fingerY
    fingerX = [0,0,0,0,0,0,0,0,0,0,0]
    palmDetect = [0,0,0,0,0,0,0,0,0,0]
    fingerY = [0,0,0,0,0,0,0,0,0,0,0]


def posFinder():
    global firstValAdded, fingerX, palmDetect, palmDetectToler, fingerY, fingerYToler
    loopCount=0
    while True:
        success, image = capt.read()
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(imageRGB)

    # checking whether a hand is detected
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks: # working with each hand
                lmList=[]
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                    # if id == 20 :
                    #     cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                indexX = 0
                indexY = 0
                indexMid = 0
                handBottomX = 0
                handBottomY = 0
                for pos in lmList:
                    if pos[0] == 7:
                        indexX, indexY = pos[1], pos[2]
                        # cv2.circle(handsFrame, (pos[1], pos[2]), 15, (255, 0, 255), cv2.FILLED)
                    elif pos[0] == 5:
                        indexMid = pos[2]
                    # elif pos[0] == 11:
                        # middleY = pos[2]
                        # cv2.circle(handsFrame, (pos[1], pos[2]), 15, (255, 0, 255), cv2.FILLED)
                    # elif pos[0] == 15:
                        # ringY = pos[2]
                        # cv2.circle(handsFrame, (pos[1], pos[2]), 15, (255, 0, 255), cv2.FILLED)
                    elif pos[0] == 0:
                        handBottomX, handBottomY = pos[1], pos[2]
                    if pos[0]==4:
                        palmDetect.append(pos[1])
                    if pos[0]==20:
                        palmDetect.append(pos[1])
                        if abs(palmDetect[-2]-palmDetect[-1])>palmDetectToler and abs(palmDetect[-4]-palmDetect[-3])>palmDetectToler and abs(palmDetect[-6]-palmDetect[-5])>palmDetectToler and abs(palmDetect[-8]-palmDetect[-7])>palmDetectToler and abs(palmDetect[-10]-palmDetect[-9])>palmDetectToler:
                            keyboard.press(Key.media_play_pause)
                            print('Paused!')
                            clearArrays()
                            sleep(gracePeriod)
                    if pos[0]==8:
                        print(str(pos[1])+', '+str(pos[2]))
                        fingerX.append(pos[1])
                        fingerY.append(pos[2])
                        currentX = fingerX[-1]
                        currentY = fingerY[-1]
                        for i in range(2,8):
                            if currentX-fingerX[-i]<-150:
                                keyboard.press(Key.media_next)
                                print('Skipped!')
                                clearArrays()
                                sleep(gracePeriod)
                                break
                            if currentX-fingerX[-i]>150:
                                if fingerX[-i]==0:
                                    break
                                keyboard.press(Key.media_previous)
                                print(fingerX)
                                print('Rewinded!')
                                if (prevRewind) :
                                    keyboard.press(Key.media_previous)
                                    prevRewind = False
                                else:
                                    prevRewind = True
                                clearArrays()
                                sleep(gracePeriod)
                                break
                if (indexY < handBottomY) and (indexY > indexMid):
                    clearArrays()
                    print("Cleared!")
                    sleep(gracePeriod-1)

                    


        #         mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)  # NOTE:UNCOMMENT THESE TO SHOW CAMERA
        # cv2.imshow("Output", image)
        # cv2.waitKey(1)

# def posProc():
#     global fingerX
#     prevArrayLen=len(fingerX)
#     print('t2 started')
#     while True:
#         while not len(fingerX)>prevArrayLen:
#             pass
#         currentX = fingerX[-1]
#         for i in range(2,4):
#             if currentX-fingerX[-i]<-150:
#                 keyboard.press(Key.media_next)
#                 print('Skipped!')
#                 fingerX=[0,0,0,0]
#                 prevArrayLen=len(fingerX)
#                 break

# t1=threading.Thread(None, posFinder)
# t2=threading.Thread(None, posProc)
# t1.start()
# t2.start()

posFinder()