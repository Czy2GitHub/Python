# -*- coding: UTF-8 -*-
import cv2
import numpy as np
from naoqi import ALProxy
import vision_definitions
import math

port = 9559  # crf 机器人端口
robot_ip = "192.168.31.150"  # crf 机器人IP
cameraProxy = ALProxy("ALVideoDevice", robot_ip, port)

# 基本参数
resolution = vision_definitions.kVGA
colorSpace = vision_definitions.kRGBColorSpace
fps = 20
frameHeight = 0
frameWidth = 0
frameChannels = 0
frameArray = None
cameraPitchRange = 47.64/180*math.pi
cameraYawRange = 60.97/180*math.pi

# 获取图片
cameraProxy.setActiveCamera(1)
videoClient = cameraProxy.subscribe("python_GVM", resolution, colorSpace, fps)
frame = cameraProxy.getImageRemote(videoClient)
cameraProxy.unsubscribe(videoClient)

# 读取图片
frameWidth = frame[0]
frameHeight = frame[1]
frameChannels = frame[2]
frameArray = np.frombuffer(frame[6], dtype=np.uint8).reshape([frameHeight, frameWidth, frameChannels])
# 转换为HSV
hue_image = cv2.cvtColor(frameArray, cv2.COLOR_BGR2HSV)

# 用颜色分割图像
low_range = np.array([160, 83, 100])
high_range = np.array([180, 255, 255])
th = cv2.inRange(hue_image, low_range, high_range)
cv2.imshow('result', th)
cv2.waitKey(0)

# 平滑处理
gaus=cv2.GaussianBlur(th,(7,7),1.5)
cv2.imshow('result', gaus)
cv2.waitKey(0)

# 腐蚀
eroded = cv2.erode(gaus, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)), iterations=2)
cv2.imshow('result', eroded)
cv2.waitKey(0)

# 膨胀
dilated = cv2.dilate(eroded, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
cv2.imshow('result', dilated)
cv2.waitKey(0)

# Hough Circle
circles = cv2.HoughCircles(dilated, cv2.HOUGH_GRADIENT, 1, 100, param1=15, param2=7, minRadius=15, maxRadius=100)

# 绘制
if circles is not None:
    x, y, radius = circles[0][0]
    center = (x, y)
    cv2.circle(frameArray, center, radius, (0, 255, 0), 2)
cv2.imshow('result', frameArray)
print(frameArray)
cv2.waitKey(0)
cv2.destroyAllWindows()