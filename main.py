import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os
from random import randrange
from PuzzlePiece import PuzzlePiece
import math

# Variables
cameraNo = 0
wCam = 1280
hCam = 720
path = "Cars/Mater"
#########################

# Methods
def placeImg(img):
    h, w, _ = img.shape
    x, y = randrange(1280 - w), randrange(720 - h)
    return x, y


def findStickingPoints(imgList):
    """"
    for 4 piece for now
    in format of((x1, y1), (x2, y2))
    since each piece has 2 sticking points
    """
    stickingPoints = []
    sizeList = []

    for img in imgList:
        sizeList.append(img.size)  # in form of (height, width)

    sp1 = (imgList[0].posOrigin[0] + sizeList[0][1], imgList[0].posOrigin[1] + sizeList[0][0] // 2), \
          (imgList[0].posOrigin[0] + sizeList[0][1] // 2, imgList[0].posOrigin[1] + sizeList[0][0])  # sticking point 1
    sp2 = (imgList[1].posOrigin[0], imgList[1].posOrigin[1] + sizeList[1][0] // 2), \
          (imgList[1].posOrigin[0] + sizeList[1][1] // 2, imgList[1].posOrigin[1] + sizeList[1][0])
    sp3 = (imgList[2].posOrigin[0] + sizeList[2][1], imgList[2].posOrigin[1] + sizeList[2][0] // 2), \
          (imgList[2].posOrigin[0] + sizeList[2][1] // 2, imgList[2].posOrigin[1])
    sp4 = (imgList[3].posOrigin[0], imgList[3].posOrigin[1] + sizeList[3][0] // 2), \
          (imgList[3].posOrigin[0] + sizeList[3][1] // 2, imgList[3].posOrigin[1])

    stickingPoints.append(sp1)
    stickingPoints.append(sp2)
    stickingPoints.append(sp3)
    stickingPoints.append(sp4)

    return stickingPoints


# Program Code
cap = cv2.VideoCapture(cameraNo)
cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector(detectionCon=0.75)

myList = os.listdir(path)
print(myList)
# Whole Image of the puzzle pieces
wholeImg = cv2.imread(f'{path}/{myList[0]}')
wholeImg = cv2.resize(wholeImg, (250, 150))
hWhole, wWhole, _ = wholeImg.shape

listImg = []
for i in range(1, len(myList)):
    pathImg = myList[i]
    # print([placeImg(cv2.imread(f'{path}/{pathImg}'))])
    if 'png' in pathImg:
        imgType = 'png'
    else:
        imgType = 'jpg'
    listImg.append(PuzzlePiece(f'{path}/{pathImg}', placeImg(cv2.imread(f'{path}/{pathImg}')), imgType, 0.5))

stickingPoints = findStickingPoints(listImg)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # flips the image
    hands, img = detector.findHands(img, flipType=False)
    img[0: hWhole, 0:wWhole] = wholeImg

    if hands:
        lmList = hands[0]['lmList']
        # Check if clicked
        length, info, img = detector.findDistance(lmList[8], lmList[12], img)
        # print(length)
        if length < 60:
            cursor = lmList[8]
            for imgObject in listImg:
                imgObject.update(cursor)
                stickingPoints = findStickingPoints(listImg)
                # print(math.dist(stickingPoints[0][0], stickingPoints[1][0]))

        # Stick the pieces if they are near enough
        if math.dist(stickingPoints[0][0], stickingPoints[1][0]) < 15:
            h, w = listImg[0].getSize()
            x = listImg[0].posOrigin[0] + w
            y = listImg[0].posOrigin[1]
            listImg[1].setPositionOrigin((x, y))
        if math.dist(stickingPoints[0][1], stickingPoints[2][1]) < 15:
            h, w = listImg[0].getSize()
            x = listImg[0].posOrigin[0]
            y = listImg[0].posOrigin[1] + h
            listImg[2].setPositionOrigin((x, y))
        if math.dist(stickingPoints[2][0], stickingPoints[3][0]) < 15:
            h, w = listImg[2].getSize()
            x = listImg[2].posOrigin[0] + w
            y = listImg[2].posOrigin[1]
            listImg[3].setPositionOrigin((x, y))
        if math.dist(stickingPoints[1][1], stickingPoints[3][1]) < 15:
            h, w = listImg[1].getSize()
            x = listImg[1].posOrigin[0]
            y = listImg[1].posOrigin[1] + h
            listImg[3].setPositionOrigin((x, y))

    try:
        for imgObject in listImg:
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                # Draw for PNG Images
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            else:
                # Draw for JPG image
                img[oy:oy + h, ox:ox + w] = imgObject.img
    except:
        pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
