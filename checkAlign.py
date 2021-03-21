# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 15:02:43 2021

@author: Administrator
"""

import numpy as np
import cv2
import os
import sys
import matplotlib.pyplot as plt

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#1
def find_location_crop(event, x, y, flags, param):
    f = open(resource_path('data/config/location_crop.txt'), 'a')
    if event == cv2.EVENT_LBUTTONDOWN:
        f.write(str(x) + "\n")
        f.write(str(y) + "\n")
    f.close()

#2
def crop_image(image):
    a = []
    f = open(resource_path('data/config/location_crop.txt'), 'r+')
    for i in range(4):
        x1 = int(f.readline())
        y1 = int(f.readline())
        x2 = int(f.readline())
        y2 = int(f.readline())
        crop = image[y1:y2, x1:x2, :]
        # cv2.imwrite(resource_path('data/img_check_crop/{}.jpg'.format(i)), crop)
        a.append(crop)
    f.close()
    return a

#3
def calc_mean(image):
    return np.mean(image, axis=(0, 1))

def calc_mean_all(image_list):
    a = []
    for i in range(4):
        # img = cv2.imread(resource_path('data/img_check_crop/{}.jpg'.format(i)))
        img = image_list[i]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        a.append(calc_mean(img))
    return a

def check(mean):
    mean_check = [245, 245, 235, 235]
    for i in range(4):
        if mean[i] < mean_check[i]:
            return 0
    return 1

# cap = cv2.VideoCapture(1)
# cap.set(3, 1280)
# cap.set(4, 720)

# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     cv2.imshow('frame', frame)
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break
#     if key == ord('s'):
#         cv2.imwrite('preview.jpg', frame)

# cap.release()
# cv2.destroyAllWindows()

# image = cv2.imread("preview.jpg")

# cv2.namedWindow("image")
# cv2.setMouseCallback("image", find_location_crop)
# while True:
#     cv2.imshow("image", image)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
# cv2.destroyAllWindows()

# crop_list = crop_image(image)

# mean = calc_mean_all(crop_list)
# print(mean)
# print(check(mean))
