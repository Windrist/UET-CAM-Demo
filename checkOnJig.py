import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class CheckOn(object):
    def __init__(self) -> None:
        super().__init__()

        self.image = []

    def calc_mean(self):
        x = self.image.shape
        sum = 0
        for i in range(x[0]):
            for j in range(x[1]):
                sum += self.image[i][j]
        return sum / (x[0]*x[1])

    def check(mean):
        if mean < 195:
            return 1
        return 0

# if __name__ == "__main__":
#     Test = CheckOn()

#     # image = cv2.imread(resource_path('data/demo/0.png'))
#     image = cv2.imread(resource_path('data/demo/Test/preview.jpg'))
#     # Test.image = cv2.cvtColor(image[140:266, 221:428], cv2.COLOR_BGR2GRAY)
#     Test.image = cv2.cvtColor(image[155:273, 250:445], cv2.COLOR_BGR2GRAY)

#     histr = cv2.calcHist([Test.image], [0], None, [256], [0, 256])
#     plt.subplot(121)
#     plt.imshow(Test.image)
#     plt.subplot(122)
#     plt.plot(histr)
#     plt.show()
#     print(Test.calc_mean())
