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

    def find_location_crop(self, event, x, y, flags, param):
        f = open(resource_path('data/config/location_crop_oj.txt'), 'a')
        if event == cv2.EVENT_LBUTTONDOWN:
            f.write(str(x) + "\n")
            f.write(str(y) + "\n")
        f.close()

    def crop_image(self):
        a = []
        f = open(resource_path('data/config/location_crop_oj.txt'), 'r+')
        for i in range(3):
            x1 = int(f.readline())
            y1 = int(f.readline())
            x2 = int(f.readline())
            y2 = int(f.readline())
            crop = self.image[y1:y2, x1:x2, :]
            a.append(crop)
        f.close()
        return a

    def check(self, crop):
        for i in range(3):
            gray = cv2.cvtColor(crop[i], cv2.COLOR_BGR2GRAY)
            histr = cv2.calcHist([gray], [0], None, [256], [0, 256])
            # plt.subplot(121)
            # plt.imshow(gray)
            # plt.subplot(122)
            # plt.plot(histr)
            # plt.show()
            for j in range(256):
                if max(histr) == histr[j]:
                    if j >= 250:
                        return 1
        return 0

# if __name__ == "__main__":
#     Test = CheckOn()

#     cap = cv2.VideoCapture(1)
#     cap.set(3, 1280)
#     cap.set(4, 720)

#     while(True):
#         # Capture frame-by-frame
#         ret, frame = cap.read()

#         # Display the resulting frame
#         cv2.imshow('frame', frame)
#         key = cv2.waitKey(1) & 0xFF
#         if key == ord('q'):
#             break
#         if key == ord('s'):
#             cv2.imwrite('preview.jpg', frame)
    
#     cap.release()
#     cv2.destroyAllWindows()

#     image = cv2.imread(resource_path('preview.jpg'))
#     Test.image = image

#     cv2.namedWindow("image")
#     cv2.setMouseCallback("image", Test.find_location_crop)
#     while True:
#         cv2.imshow("image", image)
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#     cv2.destroyAllWindows()

#     crop_list = Test.crop_image()

#     print(Test.check(crop_list))
