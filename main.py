import cv2 
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector

from snake import SnakeGame

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon = 0.8, maxHands=1)

game = SnakeGame("img.png")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]["lmList"] #Landmark Lists
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)



    cv2.imshow("Image",img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        game.gameOver = False