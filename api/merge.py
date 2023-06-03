import os

import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

img = cv2.imread("Resources/Image/p1.jpeg")
detector = PoseDetector()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
print(listShirts)

fixesRatio = 280/190 # widthOfShirt / widthOfPoint11to12
shirtRatioHeightWidth = 581 / 440

img = detector.findPose(img, draw=False)

while True:
    # img = detector.findPose(img)
    # img = cv2.flip(img, 1)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        # center = bboxInfo["center"]
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[2]), cv2.IMREAD_UNCHANGED)

        widthOfShirt = int((lm11[0] - lm12[0]) * fixesRatio)
        # imgShirt = cv2.resize(imgShirt,(0,0),None,0.5,0.5)
        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
        currentScale = (lm11[0] - lm12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)
        # print(widthOfShirt)
        try:
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
        except:
            pass





    cv2.imshow("Image",img)
    cv2.waitKey(1)



    