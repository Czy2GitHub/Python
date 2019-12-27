# coding:utf-8

import cv2
import imutils
from NaoVision import VisionBasic
from ShapeDetector import ShapeDetector
class NaoShape(VisionBasic):
    # 图片预处理
    def __init__(self):
        VisionBasic.__init__(self)
        self.resized = None
        self.ratio = None

    # 获取形状
    def detect(self, thresh):
        # 图像大小处理
        self.resized = imutils.resize(thresh, width=300)  # 将图片的宽度设为300px
        self.ratio = self.resized.shape[0] / float(self.resized.shape[0])

        self.cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cnts = imutils.grab_contours(self.cnts)
        sd = ShapeDetector()
        for c in self.cnts:
        # 获得图形的矩
            M = cv2.moments(c)
            cX = int((M["m10"] / M["m00"]) * self.ratio)
            cY = int((M["m01"] / M["m00"]) * self.ratio)
        # 根据多边形点集个数，获得图形的名称
            shape = sd.detect(c)
        # 画出图形的形状并且打印名称
            c = c.astype("float")
            c *= self.ratio
            c = c.astype("int")
        # 画出轮廓 -1为画出所有的轮廓，0为只划出一个，1，2，3以此类推，(0,255,0)为划线的颜色，2为固定参数
            cv2.drawContours(self.frameArray, [c], -1, (0, 255, 0), 2)
        # 写出名称
            cv2.putText(self.frameArray, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.imshow("Image", self.frameArray)
            cv2.waitKey(0)


