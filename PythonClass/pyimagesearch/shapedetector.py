# coding:utf-8
# import the necessary packages
import cv2

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unfentified"  # shape是形状的名称
        # 计算图形的周长
        peri = cv2.arcLength(c, True)
        # 计算图形一共有多少个点集，存在一个数组里
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        # 根据点集的个数，判断为几边形
        if len(approx) == 3:
            shape = "triangle"
        # 当点集为四时，判断为正方形还是长方形
        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # 根据得到的比值来判断正方形与长方形
            shape = "square" if ar >=0.95  and  ar <= 1.05 else "rectangle"

        elif len(approx) == 5:
            shape = "pentagon"

        else:
            shape = "circle"
        # 返回shape
        return shape

