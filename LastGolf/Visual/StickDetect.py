# coding:utf-8

import cv2
import numpy as np
import vision_definitions as vd
import VisualBasis
class StickDetect(VisualBasis):
    def __init__(self, IP, cameraId=vd.kTopCamera, resolution=vd.kVGA):
        super(StickDetect, self).__init__(IP, cameraId, resolution)
        self._boundRect = []
        self._cropKeep = 1
        self._stickAngle = None  # rad

    def _findStick(self, frameBin, minPerimeter, minArea):
        """
        find the yellow stick in the preprocessed frame.
        Args:
            frameBin: preprocessed frame.
            minPerimeter: minimum perimeter of detected stick.最小周长
            minArea: minimum area of detected stick.最小面积
        Return: detected stick marked with rectangle or [].
        """

        rects = []  # 矩形，观测到的黄杆形状是矩形
        _, contours, _ = cv2.findContours(frameBin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # contour 外形，轮廓

        if len(contours) == 0:
            return rects

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            area = cv2.contourArea(contour)
            if perimeter > minPerimeter and area > minArea:
                x, y, w, h = cv2.boundingRect(contour)
                rects.append([x, y, w, h])

        if len(rects) == 0:
            return rects

        rects = [rect for rect in rects if (1.0 * rect[3] / rect[2]) > 0.8]

        # if len(rects) == 0:
        #     return rects

        rects = np.array(rects)
        print(rects)
        rect = rects[np.argmax(1.0 * (rects[:, -1]) / rects[:, -2]),]
        rect[1] += int(self._frameHeight * (1 - self._cropKeep))
        return rect

    def _preprocess(self, minHSV, maxHSV, cropKeep, morphology):  # 图形预处理函数
        """
        preprocess the current frame for stick detection.(binalization, crop etc.)
        Arguments:
            minHSV: the lower limit for binalization.  黄色的HSV阈值
            maxHSV: the upper limit for binalization.
            cropKeep: crop ratio (>=0.5).
            morphology: erosion and dilation.腐蚀和膨胀
        Return:
            preprocessed image for stick detection.
        """
        self._cropKeep = cropKeep
        frameArray = self._frameArray
        height = self._frameHeight
        width = self._frameWidth
        try:
            frameArray = frameArray[int((1 - cropKeep) * height):, :]
        except IndexError:
            raise
        frameHSV = cv2.cvtColor(frameArray, cv2.COLOR_BGR2HSV)
        frameBin = cv2.inRange(frameHSV, minHSV, maxHSV)

        kernelErosion = np.ones((5, 5), np.uint8)  # 腐蚀
        kernelDilation = np.ones((5, 5), np.uint8)  # 膨胀
        frameBin = cv2.erode(frameBin, kernelErosion, iterations=1)  # 腐蚀图二值化
        frameBin = cv2.dilate(frameBin, kernelDilation, iterations=1)  # 膨胀二值化
        frameBin = cv2.GaussianBlur(frameBin, (9, 9), 0)  # 高斯滤波
        return frameBin