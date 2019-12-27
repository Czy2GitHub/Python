# coding:utf-8
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2

# 设定执行函数文件的格式
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
args = vars(ap.parse_args())

# 对图像进行预处理
image = cv2.imread((args["image"]))
resized = imutils.resize(image, width=300)   # 将图片的宽度设为300px
ratio = image.shape[0] / float(resized.shape[0])

#
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)      # 转化为RGB图像
blurred = cv2.GaussianBlur(gray, (5, 5), 0)           # 霍夫处理 降噪 平滑

thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]      # 取得二值图
cv2.imshow("1", thresh)
# 获取形状
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()

# 获取圆心
for c in cnts:
    # 获得图形的矩
    M = cv2.moments(c)
    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)
    # 根据多边形点集个数，获得图形的名称
    shape = sd.detect(c)
    # 画出图形的形状并且打印名称
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    # 画出轮廓 -1为画出所有的轮廓，0为只划出一个，1，2，3以此类推，(0,255,0)为划线的颜色，2为固定参数
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    # 写出名称
    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow("Image", image)
    cv2.waitKey(0)