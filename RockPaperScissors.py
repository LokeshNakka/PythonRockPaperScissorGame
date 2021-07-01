import random
import os
import cv2
import HandTrackingModule as htm


def LoadImages(percent):
    imgFolderPath = r'D:\PythonProj\PythonAdvancedComputerVision\RockPaperSciccorsGame'
    imagesPath = os.listdir(imgFolderPath)
    loadedImgs = []
    for a in imagesPath:
        img = cv2.imread(f'{imgFolderPath}/{a}')
        scale_percent = percent  # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        loadedImgs.append(resized)
    return loadedImgs


def IsHandClosedOrOpened(hand=[]):
    length = len(hand)
    if length == 0:
        return []
    initial = hand[0]
    result = []
    for id in range(6, length, 4):
        lDiff = abs(initial[1] - hand[id][1]) + abs(initial[2] - hand[id][2])
        uDiff = abs(initial[1] - hand[id + 2][1]) + abs(initial[2] - hand[id + 2][2])
        result.append(1 if lDiff <= uDiff else 0)

    tlDiff = abs(initial[1] - hand[3][1]) + abs(initial[2] - hand[3][2])
    tuDiff = abs(initial[1] - hand[4][1]) + abs(initial[2] - hand[4][2])
    result.insert(0, 1 if tlDiff <= tuDiff else 0)

    return result


if __name__ == '__main__':
    instance = htm.HandTrackingUtils(max_hands=1, min_detection_con=.9, min_tracking_con=.9)
    overlays = LoadImages(130)
    gameStarted = False
    countDown = 1
    frame = 0
    userScore = 0
    computerScore = 0

    while True:
        if not gameStarted:
            instance.OnlyCapture()
            instance.ShowText(str('user {0}'.format(userScore)), 'tl')
            instance.ShowText(str('com {0}'.format(computerScore)), 'tr')
            instance.ShowText(str(countDown), 'c', 3)
            instance.ShowImg()
            frame = frame + 1
            if frame >= 20:
                frame = 0
                countDown = countDown + 1
                if countDown > 3:
                    gameStarted = True

            cv2.waitKey(1)

        else:
            hands = instance.GetDetectedPoinsAsList()
            instance.HighlightThis(landMarkIndexs=[0, 4, 8, 12, 16, 20])
            hand1 = hands[0] if len(hands) > 0 else []
            status = IsHandClosedOrOpened(hand1)
            userchoosen = None

            if status in [[1, 1, 1, 1, 1], [0, 1, 1, 1, 1]]:
                instance.insertImage(overlays[0], 'cl')
                userchoosen = 0

            elif status in [[0, 0, 0, 0, 0], [1, 0, 0, 0, 0]]:
                instance.insertImage(overlays[1], 'cl')
                userchoosen = 1

            elif status in [[0, 1, 1, 0, 0], [1, 1, 1, 0, 0]]:
                instance.insertImage(overlays[2], 'cl')
                userchoosen = 2

            if len(hand1) > 0 and not userchoosen is None:
                # Game Logic
                computerChoose = random.randint(0, len(overlays) - 1)
                instance.insertImage(overlays[computerChoose], 'cr')

                if computerChoose == userchoosen:
                    instance.ShowText('Draw', 'c', 1)

                elif computerChoose + 1 == userchoosen or computerChoose + 1 == 3:
                    computerScore = computerScore + 1
                    instance.ShowText('Com Win', 'c', 1)

                elif computerChoose - 1 == userchoosen or computerChoose - 1 < 0:
                    userScore = userScore + 1
                    instance.ShowText('U Win', 'c', 1)

                instance.ShowText(str('user {0}'.format(userScore)), 'tl')
                instance.ShowText(str('com {0}'.format(computerScore)), 'tr')

                instance.ShowImg()
                cv2.waitKey(1500)
                countDown = 1
                frame = 0
                gameStarted = not gameStarted
                instance.GetDetectedPoinsAsList().clear()
            else:
                instance.ShowText('User Not Detect or Undefine', 'c', 1)
                instance.ShowImg()
                cv2.waitKey(1500)
                countDown = 1
                frame = 0
                gameStarted = not gameStarted
