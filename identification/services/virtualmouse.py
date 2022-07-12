from cv2 import VideoCapture, destroyAllWindows, CAP_V4L2, flip, FILLED, circle, imshow
import numpy as np
from autopy import screen, mouse as Amouse
from services import handTrackingModule as htm
import os
from datetime import datetime, timedelta
import sys

class Mouse:

    def __init__(self):
        self.cap = VideoCapture(0)
        self.wScr, self.hScr = screen.size()
        self.wCam = 640
        self.hCam = 480
        self.frameR = 150
        self.smootheing = 5
        self.plocX = 0
        self.plocY = 0
        self.clocX = 0
        self.clocY = 0
        self.detector = htm.HandDetector()

    def Mouse(self, img):
        
        # finding hands
        self.detector.findhands(img)
        lmlist, bbox = self.detector.findPosition(img)

        # 2. get the tip of index and midel finger
        if len(lmlist) != 0:
            Xindex, Yindex = lmlist[8][1], lmlist[8][2]
            Xmidel, Ymidel = lmlist[12][1], lmlist[12][2]
            # 3. check which one is up?
            fingers = self.detector.fingersUp()
            # 4. index: moving mode
            if fingers[1] == 1 and fingers[2] == 0:
                # 5. cordinates the position (cam :640*480) to (screen :2560 × 1600)
                xMOUSE = np.interp(Xindex, [self.frameR, self.wCam - self.frameR], [0, self.wScr])
                yMOUSE = np.interp(Yindex, (self.frameR, self.hCam - self.frameR), (0, self.hScr))
                
                # 6. smoothen value
                self.clocX = self.plocX + (xMOUSE - self.plocX) / self.smootheing
                self.clocY = self.plocY + (yMOUSE - self.plocY) / self.smootheing
                # 7. move mouse
                Amouse.move(self.clocX, self.clocY)

                circle(img, (Xindex, Yindex), 15, (20, 180, 90), FILLED)
                self.plocY, self.plocX = self.clocY, self.clocX
            # 8. both are up : cliking mode
            if fingers[1] == 1 and fingers[2] == 1:
                # 9. finding distance
                length, bbox = self.detector.findDistance(8, 12, img)
                # 10. click if distance was short
                if length < 40:
                    Amouse.click()
        return img


    def main(self):
        if self.cap.isOpened():
            self.cap.set(3, self.wCam)
            self.cap.set(4, self.hCam)
            while True:
                sucess, img = self.cap.read()
                img = flip(img, 1)
                img = self.Mouse(img)
        else:
            return "Pas de cam"

    def stop(self):
        self.cap.release()
        self.cap = None
        destroyAllWindows()

    def __del__(self):
        print("vm killed")
        
