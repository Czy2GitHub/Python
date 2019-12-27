# coding:utf-8
import math
import time
import vision_definitions as vd
from circleDetect import findBall
import numpy as np
from naoqi import ALProxy
from Text import *
id = "192.168.31.32"
port = 9559
cameraProxy = ALProxy("ALVideoDevice", id, port)
motionProxy = ALProxy("ALMotion", id, port)
def getRedBall():
    # 球的数据
    ballData = []
    # 角度
    angle = -60
    reallyAngle = [angle / 180 * math.pi]
    # 循环找球
    while True:
        time.sleep(1)
        motionProxy.setMoveArmsEnabled(False, False)
        motionProxy.moveTo(0.2, 0, 0)
        imgList = getImage(1)
        ballData = findBall(imgList)            # ballData: 圆心x, y, 半径r
        if ballData != [] or angle == 120:
            return ballData
        else:
            motionProxy.setMoveArmsEnabled(False, False)
            motionProxy.moveTo(0.2, 0, 0)
            time.sleep(1)
            motionProxy.angleInterpolationWithSpeed("HeadYaw", reallyAngle, 0.2)
            time.sleep(2)
            angle += 60
    return []
def ToTheRedBall(ballPosition):
    motionProxy.setMoveArmsEnabled(False, False)
    motionProxy.moveTo(ballPosition["disX"] - 0.10, ballPosition["disY"], ballPosition["angle"])

def getImage(cameraId):
    cameraProxy.setActiveCamera(cameraId)
    videoClient = cameraProxy.subscribe("Recognize", vd.kVGA,  vd.kBGRColorSpace, 20)
    videoFrame = cameraProxy.getImageRemote(videoClient)
    cameraProxy.unsubscribe(videoClient)
    frameWidth = videoFrame[0]
    frameHeight = videoFrame[1]
    frameChannels = videoFrame[2]
    frameArrays = np.frombuffer(videoFrame[6], dtype=np.uint8).reshape(frameHeight, frameWidth, frameChannels)
    return frameArrays
if __name__ == "__main__":
    ballData = getRedBall()
    frameArray = getImage(1)
    if ballData != None:
        ballPosition = redBallLocation("standInit", frameArray, ballData)
        ToTheRedBall(ballPosition)