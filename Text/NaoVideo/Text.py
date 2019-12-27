# coding:utf-8
from naoqi import ALProxy
import vision_definitions
import cv2
import numpy as np

resolution = vision_definitions.kVGA
colorSpace = vision_definitions.kBGRColorSpace
FPS = 20
robotIP = "192.168.31.132"
port = 9559
carema = ALProxy("ALVideoDevice", robotIP, port)
tracker = ALProxy("ALTracker", robotIP, port)
carema.setActiveCamera(1)
videoVideo = carema.subscribe("Recognize", resolution, colorSpace, FPS)
frame = carema.getImageRemote(videoVideo)
carema.unsubscribe(videoVideo)

# 获取图片
frameWidth = frame[0]
frameHeight = frame[1]
frameChannels = frame[2]
frameArray = np.frombuffer(frame[6], dtype=np.uint8).reshape(frameHeight, frameWidth, frameChannels)
cv2.imshow("result", frameArray)
cv2.waitKey(0)
