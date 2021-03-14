# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 15:02:43 2021

@author: Administrator
"""

import numpy as np
import cv2
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

#1
def find_location_crop(event, x, y, flags, param):
    f = open(resource_path('data/config/location_crop.txt'), 'a+')
    if event == cv2.EVENT_LBUTTONDOWN:
        f.write(str(x) + "\n")
        f.write(str(y) + "\n")

#2
def crop_image(image):
    f = open(resource_path('data/config/location_crop.txt'), 'r+')
    for i in range(4):
        x1 = int(f.readline())
        y1 = int(f.readline())
        x2 = int(f.readline())
        y2 = int(f.readline())
        crop = image[y1:y2, x1:x2, :]
        cv2.imwrite(resource_path('data/img_check_crop/{}.jpg'.format(i)), crop)
    f.close()

#3
def calc_mean(image):
    x = image.shape
    sum = 0
    for i in range(x[0]):
        for j in range(x[1]):
            sum += image[i][j]
    return sum / (x[0]*x[1])

def calc_mean_all():
    a = []
    for i in range(4):
        img = cv2.imread(resource_path('data/img_check_crop/{}.jpg'.format(i)))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        a.append(calc_mean(img))
    return a

def check(mean):
    mean_check = [180, 200, 200, 200]
    for i in range(4):
        if mean[i] < mean_check[i]:
            return 0
    return 1

# cap = cv2.VideoCapture(0)
# i = 0

##4
# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     # Our operations on the frame come here
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Display the resulting frame
#     cv2.imshow('frame',gray)
#     k = cv2.waitKey(1)
#     print(k)
#     if k==113:
#         break
#     if k==99:
#         cv2.imwrite('img\\{}.jpg'.format(i),frame)
#         image = frame
#         image = cv2.resize(image,(800,800))
#         crop_image(image)
#         mean = calc_mean_all()
#         print(check(mean))
#         i+=1
        
# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()


# image = cv2.imread("demo/Check/OK-2.jpg")
# # print(image.shape)
# image = cv2.resize(image,(800,800))


##1
# cv2.namedWindow("image")
# cv2.setMouseCallback("image",find_location_crop)
# while True:
#     cv2.imshow("image",image)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
# cv2.destroyAllWindows()

##2
# crop_image(image)

##3
# #calculator mean
# mean = calc_mean_all()
# print(check(mean))

