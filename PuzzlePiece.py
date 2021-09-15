import cv2


class PuzzlePiece():
    def __init__(self, path, posOrigin, imgType, resizeRatio):
        self.path = path
        self.posOrigin = posOrigin
        self.imgType = imgType

        if self.imgType == "png":
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        self.img = cv2.resize(self.img, (0, 0), None, resizeRatio, resizeRatio)
        self.size = self.img.shape[:2]  # height, width

        self.stickingPoints = []  # [(x1, y1), (x2, y2)]

    # Methods
    def update(self, cursor):  # cursor represents the tip of the index finger in this project
        ox, oy = self.posOrigin
        h, w = self.size

        # Check if in region
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2
            # since cursor should overlay with the middle of the img

    def setPositionOrigin(self, newPosOrigin):
        self.posOrigin = newPosOrigin

    def getSize(self):
        return self.size
