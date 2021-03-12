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

class Detect(object):
    def __init__(self) -> None:
        super().__init__()

        self.image = []
        self.crop_tray_1 = []
        self.crop_tray_2 = []

        f = open(resource_path('data/config/location_crop_yn.txt'))
        self.t1_x_begin = int(f.readline())
        self.t1_y_begin = int(f.readline())
        self.t1_x_end = int(f.readline())
        self.t1_y_end = int(f.readline())
        self.t2_x_begin = int(f.readline())
        self.t2_y_begin = int(f.readline())
        self.t2_x_end = int(f.readline())
        self.t2_y_end = int(f.readline())

    def find_location_crop(self, event, x, y, flags, param):
        f = open(resource_path('data/config/location_crop_yn.txt'), 'w')
        if event == cv2.EVENT_LBUTTONDOWN:
            f.write(str(x) + "\n")
            f.write(str(y) + "\n")
    
    def get_coord(self):
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.find_location_crop)
        while True:
            cv2.imshow("image", self.image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cv2.destroyAllWindows()

    def grabCut(self):
        
        crop_tray_1 = self.image[self.t1_y_begin:self.t1_y_end, self.t1_x_begin:self.t1_x_end]
        crop_tray_2 = self.image[self.t2_y_begin:self.t2_y_end, self.t2_x_begin:self.t2_x_end]

        gray_tray_1 = cv2.cvtColor(crop_tray_1, cv2.COLOR_BGR2GRAY)
        gray_tray_2 = cv2.cvtColor(crop_tray_2, cv2.COLOR_BGR2GRAY)

        ret_tray_1, thresh_tray_1 = cv2.threshold(gray_tray_1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        ret_tray_2, thresh_tray_2 = cv2.threshold(gray_tray_2, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        mask_detect = np.zeros(crop_tray_1.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        mask_detect[thresh_tray_1 == 255] = 1
        mask_detect[thresh_tray_1 == 0] = 0
        cv2.grabCut(crop_tray_1, mask_detect, None, bgdModel, fgdModel, 1, cv2.GC_INIT_WITH_MASK)
        mask3 = np.where((mask_detect == 2) | (mask_detect == 0), 0, 1).astype('uint8')
        self.crop_tray_1 = crop_tray_1 * mask3[:, :, np.newaxis]

        mask_detect = np.zeros(crop_tray_2.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        mask_detect[thresh_tray_2 == 255] = 1
        mask_detect[thresh_tray_2 == 0] = 0
        cv2.grabCut(crop_tray_2, mask_detect, None, bgdModel, fgdModel, 1, cv2.GC_INIT_WITH_MASK)
        mask3 = np.where((mask_detect == 2) | (mask_detect == 0), 0, 1).astype('uint8')
        self.crop_tray_2 = crop_tray_2 * mask3[:, :, np.newaxis]

    def check(self, crop_img):
        crop_gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        height = crop_img.shape[0]
        width = crop_img.shape[1]
        mask = np.zeros(21)
        for i in range(21):
            k = int(i / 7)
            j = i % 7
            cut = crop_gray[int(height / 7 * (7 - j - 1)):int(height / 7 * (7 - j)), int(width / 3 * k):int(width / 3 *
                                                                                                            (k + 1))]
            histr = cv2.calcHist([cut], [0], None, [256], [0, 256])
            # plt.subplot(121)
            # plt.imshow(cut)
            # plt.subplot(122)
            # plt.plot(histr)
            # plt.show()
            for j in range(256):
                if max(histr) == histr[j]:
                    if j <= 10:
                        mask[i] = 1
        return mask

# if __name__ == "__main__":
#     detect = Detect()
#     detect.image = cv2.imread('data/demo/Detect/origin.jpg')
#     detect.image = cv2.resize(detect.image, (1920, 1080), interpolation=cv2.INTER_AREA)

#     # detect.get_coord()
#     detect.grabCut()
#     mask = detect.check(detect.crop_tray_1)
#     mask = np.append(mask, detect.check(detect.crop_tray_2))

#     print(mask.shape)
