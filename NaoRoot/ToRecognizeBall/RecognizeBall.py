# coding:utf-8

import cv2
import numpy as np
from naoqi import ALProxy
from NaoVision import VisionBasic
# 识别红球
class Recognize(VisionBasic):
    def __init__(self):
        VisionBasic.__init__(self)
    def searchBall(self):
        # 转换为HSV
        hue_image = cv2.cvtColor(self.frameArray, cv2.COLOR_BGR2HSV)
        
        # 用颜色分割图像
        low_range = np.array([160, 83, 100])
        high_range = np.array([180, 255, 255])
        th = cv2.inRange(hue_image, low_range, high_range)

        # 平滑处理
        gaus = cv2.GaussianBlur(th, (7, 7), 1.5)
        
        # 腐蚀
        eroded = cv2.erode(gaus, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)), iterations=2)

        # 膨胀
        dilated = cv2.dilate(eroded, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)

        # Hough Circle
        circles = cv2.HoughCircles(dilated, cv2.HOUGH_GRADIENT, 1, 100, param1=15, param2=7, minRadius=15, maxRadius=100)
        
        # 绘制
        if circles is not None:
            x, y, radius = circles[0][0]
            center = (x, y)
            cv2.circle(self.frameArray, center, radius, (0, 255, 0), 2)