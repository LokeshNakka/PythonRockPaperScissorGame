import cv2
import mediapipe as mp
import time


class HandTrackingUtils:
    def __init__(self, mode=False, max_hands=2, min_detection_con=0.5, min_tracking_con=0.5, color='#00000'):
        self.color = color
        self.static_image_mode = mode,
        self.max_num_hands = max_hands,
        self.min_detection_confidence = min_detection_con,
        self.min_tracking_confidence = min_tracking_con,
        self.vCapture = cv2.VideoCapture(0)
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.sTime = time.time()
        self.detectedList = []

    def OnlyCapture(self):
        self.sTime = time.time()
        self.success, self.image = self.vCapture.read()
        h, w, c = self.image.shape
        self.height = h
        self.width = w
        self.eTime = time.time()

    def GetDetectedPoinsAsList(self):
        self.sTime = time.time()
        self.success, self.image = self.vCapture.read()
        imageRGB = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imageRGB)
        h, w, c = self.image.shape
        self.height = h
        self.width = w
        if results.multi_hand_landmarks:
            self.detectedList.clear()
            for indx, handLandMarks in enumerate(results.multi_hand_landmarks):
                self.mpDraw.draw_landmarks(self.image, handLandMarks, self.mpHands.HAND_CONNECTIONS)

                hand = [[id, int(w * landMark.x), int(h * landMark.y)] for id, landMark in
                        enumerate(handLandMarks.landmark)]
                # hand.insert(0, indx)
                self.detectedList.append(hand)
        self.eTime = time.time()
        return self.detectedList;

    def HighlightThis(self, handIndx=0, radius=5, landMarkIndexs=[]):
        for landMarkIndex in landMarkIndexs:
            if len(self.detectedList) > handIndx and len(self.detectedList[handIndx]) > landMarkIndex:
                point = self.detectedList[handIndx][landMarkIndex]
                cv2.circle(self.image, (point[1], point[2]), radius, (100, 0, 125), cv2.FILLED)

    def ShowFPS(self, location='tr'):
        timePerFrame = self.eTime - self.sTime
        fps = 1 / timePerFrame
        self.ShowText('FPS {0} '.format(str(int(fps))), location, 1)

    def ShowText(self, text='', location='c', textSize=1):
        x = 0
        y = 0
        for char in location:
            if char == 't':
                y = int(self.height * .05)
            if char == 'b':
                y = int(self.height * .98)

            if char == 'c':
                x = int(self.width * .5 - len(text) * 10)
                y = int(self.height * .5)

            if char == 'l':
                x = int(self.width * .01)
            if char == 'r':
                x = int(self.width - len(text) * 20)

        cv2.putText(self.image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, textSize, (155, 1, 255), 3)

    def insertImage(self, imge, location='tl'):

        width = imge.shape[1]
        height = imge.shape[0]

        x = 0
        y = 0

        for char in location:
            if char == 't':
                y = 0
            if char == 'b':
                y = int(self.height - height)

            if char == 'c':
                x = int(self.width * .5) - int(width * 0.5)
                y = int(self.height * .5) - int(height * 0.5)

            if char == 'l':
                x = 0
            if char == 'r':
                x = int(self.width - width)

        self.image[y:imge.shape[0] + y, x:imge.shape[1] + x] = imge

    def ShowImg(self):
        cv2.imshow('Image', self.image)
        cv2.waitKey(1)

    def GetImageSize(self):
        return self.image.shape
