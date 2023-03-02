import cv2
import mediapipe as mp
import os
import time
import hand_tracking_module as htm
import numpy as np

path = 'templates'
dirlist = os.listdir(path)
overlay = []

strip_height = 50
strip_width = 960

top = 0
bottom = strip_height
left = 0
right = strip_width

detector = htm.hand_tracking(confidence_detection=0.80)

defaultcolor = (173, 216, 230)
thickness = 10
eraserthickness = 35

canvas = np.zeros((720, 1200, 3), np.uint8)

xp, yp = 0, 0

for img in dirlist:
    image = cv2.imread(f'{path}/{img}')
    overlay.append(image)

template = overlay[0]
template = cv2.resize(template, (960, 50))


cap = cv2.VideoCapture(0)
cap.set(3, 1200)
cap.set(4, 720)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # getting landmarks
    frame = detector.hands_tracking(frame)
    lmList = detector.position_find(frame, draw = False)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:] # tip of index finger
        x2, y2 = lmList[12][1:] # tip of middle finger




        # check how many fingers are up

        fingers = detector.finger_up()
    # If two fingers are up- selection mode only no drawing
        if fingers[1] and fingers[2]:
            print('MAKE A SELECTION')
            if y1 < 50:
                if 75<x1<130:
                    template = overlay[0]
                    defaultcolor = (173, 216, 230)
                elif 150<x1<360:
                    template = overlay[1]
                    defaultcolor = (124, 252, 0)
                elif 400<x1<600:
                    template = overlay[2]
                    defaultcolor = (255, 160, 122)
                elif 660<x1<800:
                    template = overlay[3]
                    defaultcolor = (0, 0, 0)

    # If one finger is up- drawing mode
        if fingers[1] and fingers[2] == False:
            cv2.circle(frame, (x1, y1), 15, (0, 255, 255), cv2.FILLED)

            if xp == 0 and  yp == 0:
                xp, yp = x1, y1
            
            if defaultcolor == (0, 0, 0):
                cv2.line(frame, (xp, yp), (x1, y1), defaultcolor, eraserthickness)
                cv2.line(canvas, (xp, yp), (x1, y1), defaultcolor, eraserthickness)
                xp, yp = x1, y1
            else:
                cv2.line(frame, (xp, yp), (x1, y1), defaultcolor, thickness)
                cv2.line(canvas, (xp, yp), (x1, y1), defaultcolor, thickness)
                xp, yp = x1, y1
            print('DRAW')


    frame[top:bottom, left:right] = template
    cv2.imshow('Webcam', frame)
    cv2.imshow('Canvas', canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()