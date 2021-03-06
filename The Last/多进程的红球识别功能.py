# encoding: GBK
# 此功能因为时间原因，没有加入到最终的程序中
from multiprocessing import Process, Pool, Queue
import os
import time
from naoqi import ALProxy
import sys
import cv2
import numpy as np
import almath
import time
import math

robotIP = "192.168.31.120"
PORT = 9559
motionPrx = ALProxy("ALMotion", robotIP, PORT)
_stepStatue = [["MaxStepX", 0.04], ["MaxStepY", 0.14], ["MaxStepTheta", 0.3], ["MaxStepFrequency", 3],
                   ["StepHeight", 0.02], ["TorsoWx", 0], ["TorsoWy", 0]]

def findball(angle):
    motionPrx.angleInterpolationWithSpeed("HeadYaw", angle * math.pi / 180, 0.3)
    motionPrx.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.3)
    redballProxy.subscribe("redBallDetected")
    memoryProxy.insertData("redBallDetected", [])
    time.sleep(0.5)
    ballData = memoryProxy.getData("redBallDetected")
    redballProxy.unsubscribe("redBallDetected")

    if (ballData != []):
        # headangle 为机器人水平方向相对x轴的转角
        headangle = motionPrx.getAngles("HeadYaw", True)
        allData = [headangle, ballData]
        return allData
    else:
        return []

def searchredball():
    camProxy.setActiveCamera(1)
    angle = -60
    while angle <= 60:
        allData = findball(angle)
        if allData != []:
            return allData
        else:
            angle += 60
    return []

def straightMove():
    while True:
        motionPrx.moveTo(0.1, 0.0, 0.0, _stepStatue)

def CalculateRobotToRedball(allballData):
    # 原 h = 0.478
    h = 0.578
    # 机器人行走参数
    maxstepx = 0.04
    maxstepy = 0.14
    maxsteptheta = 0.3
    maxstepfrequency = 0.6
    stepheight = 0.02
    torsowx = 0.0
    torsowy = 0.0

    headangle = allballData[0]  # 头偏转角
    wzCamera = allballData[1][1][0]  # alpha角
    wyCamera = allballData[1][1][1]  # beta角
    isenabled = False
    x = 0.0
    y = 0.0
    if (headangle[0] + wzCamera < 0.0):
        theta = headangle[0] + wzCamera + 0.2  # 修改一
    else:
        theta = headangle[0] + wzCamera

    motionPrx.setMoveArmsEnabled(False, False)
    # 接下来，第一次，机器人转到正对红球的方向
    motionPrx.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.5)
    motionPrx.moveTo(x, y, theta,
                     [["MaxStepX", maxstepx],
                      ["MaxStepY", maxstepy],
                      ["MaxStepTheta", maxsteptheta],
                      ["MaxStepFrequency", maxstepfrequency],
                      ["StepHeight", stepheight],
                      ["TorsoWx", torsowx],
                      ["TorsoWy", torsowy]])  # x=y=0

    time.sleep(1.5)
    val = memoryProxy.getData("redBallDetected")
    # info 信息
    ballinfo = val[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1] + (39.7 * math.pi / 180.0)
    x = h / (math.tan(thetav)) - 0.5  # 最少为40厘米
    if (x >= 0):
        theta = 0.0
        motionPrx.setMoveArmsEnabled(False, False)
        print("正对红球方向完成")
        # 接下来，第二次，机器人走到距离红球20厘米的位置,程序为40厘米，因为机器人在实际行走过程中误差过大，会踢到球
        motionPrx.moveTo(x, y, theta,
                         [["MaxStepX", maxstepx],
                          ["MaxStepY", maxstepy],
                          ["MaxStepTheta", maxsteptheta],
                          ["MaxStepFrequency", maxstepfrequency],
                          ["StepHeight", stepheight],
                          ["TorsoWx", torsowx],
                          ["TorsoWy", torsowy]])

        motionPrx.waitUntilMoveIsFinished()
    # 向下低头30度
    effectornamelist = ["HeadPitch"]
    timelist = [0.5]
    # targetlist = [30 * math.pi / 180.0]
    targetlist = [30 * math.pi / 180.0]
    motionPrx.angleInterpolation(effectornamelist, targetlist, timelist, isenabled)
    time.sleep(1.5)
    val = memoryProxy.getData("redBallDetected")
    ballinfo = val[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1] + (69.7 * math.pi / 180.0)
    x = 0.0
    y = 0.0
    theta = thetah
    motionPrx.setMoveArmsEnabled(False, False)
    print("走到距离红球20cm处")
    # 接下来，第三次，机器人修正角度对准红球
    motionPrx.moveTo(x, y, theta,
                     [["MaxStepX", maxstepx],
                      ["MaxStepY", maxstepy],
                      ["MaxStepTheta", maxsteptheta],
                      ["MaxStepFrequency", maxstepfrequency],
                      ["StepHeight", stepheight],
                      ["TorsoWx", torsowx],
                      ["TorsoWy", torsowy]])
    time.sleep(1.5)

    maxstepx = 0.02
    maxstepy = 0.14
    maxsteptheta = 0.15
    maxstepfrequency = 0.6
    stepheight = 0.02
    torsowx = 0.0
    torsowy = 0.0

    val = memoryProxy.getData("redBallDetected")
    ballinfo = val[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1] + (69.7 * math.pi / 180.0)
    x = (h - 0.03) / (math.tan(thetav)) - 0.1  # 三点一线最终修改关键点
    theta = thetah
    motionPrx.setMoveArmsEnabled(False, False)
    print("角度修正完成")
    # 接下来，第四次，机器人走到距离红球10厘米的位置
    motionPrx.moveTo(x, y, theta,
                     [["MaxStepX", maxstepx],
                      ["MaxStepY", maxstepy],
                      ["MaxStepTheta", maxsteptheta],
                      ["MaxStepFrequency", maxstepfrequency],
                      ["StepHeight", stepheight],
                      ["TorsoWx", torsowx],
                      ["TorsoWy", torsowy]])
    time.sleep(1.5)
    print("到达10cm处")
    val = memoryProxy.getData("redBallDetected")
    ballinfo = val[1]
    thetah = ballinfo[0]
    print(thetah)
    thetav = ballinfo[1] + (69.7 * math.pi / 180.0)
    x = 0.0
    y = 0.0
    theta = thetah
    motionPrx.setMoveArmsEnabled(False, False)
    print("走到距离红球20cm处")
    # 接下来，第五次，机器人最后修正角度对准红球
    motionPrx.moveTo(x, y, theta,
                     [["MaxStepX", maxstepx],
                      ["MaxStepY", maxstepy],
                      ["MaxStepTheta", maxsteptheta],
                      ["MaxStepFrequency", maxstepfrequency],
                      ["StepHeight", stepheight],
                      ["TorsoWx", torsowx],
                      ["TorsoWy", torsowy]])
    time.sleep(1.5)
    # 接下来，第六次，最后一次检测球和机器人的距离dx
    val = memoryProxy.getData("redBallDetected")
    ballinfo = val[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1] + (69.7 * math.pi / 180.0)
    emsl = val[3][0]
    dx = (h - 0.03) / (math.tan(thetav))  # dx作为了三角形的一条边
    dx += emsl
    print dx
    return dx

if __name__ == "__main__":
    searchBallTimes = 0
    memoryProxy = ALProxy("ALMemory", robotIP, PORT)  # memory  object
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    postureProxy.goToPosture("StandInit", 1.0)
    # memoryProxy = ALProxy("ALMemory", robotIP , PORT)
    Lifestop = ALProxy("ALAutonomousLife", robotIP, PORT)
    redballProxy = ALProxy("ALRedBallDetection", robotIP, PORT)
    camProxy = ALProxy("ALVideoDevice", robotIP, PORT)
    landmarkProxy = ALProxy("ALLandMarkDetection", robotIP, PORT)
    
    p = Process(target=straightMove)
    p.start()
    tts.say("我开始了")
    allData = searchredball()
    while allData == []:
        allData = searchredball()
    p.terminate()
    CalculateRobotToRedball(allData)

# postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
# postureProxy.goToPosture("StandInit", 1.0)
# Lifestop = ALProxy("ALAutonomousLife", robotIP, PORT)
# Lifestop.setState("disabled")
# motionPrx.wakeUp()
# motionPrx.moveTo(0.3, 0, 0)


