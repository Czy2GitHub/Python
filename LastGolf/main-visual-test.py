#ecoding:utf-8
from Data import *
"""
some test codes for Nao golf visual part.
@author: Meringue
@date: 2018/1/15
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import numpy as np
import cv2
import time
import os
import sys
#sys.path.append("/home/meringue/Softwares/pynaoqi-sdk/") #naoqi directory
sys.path.append("./")
import time
from visualTask import *
from naoqi import ALProxy
import vision_definitions as vd
headAngle = {"standInit": 49.2 / 180 * np.pi, "standUp": 39.7 / 180 * np.pi}
IP = "192.168.43.32"
PORT = 9559
_searchBallTimes = 0
stop1 = 0
# 0代表正常,非零则没有识别
landmarkFlag = 0
redballFlag = 0
# 步态和击球姿式
maxstepx = 0.04    # 直走一次的最大距离
maxstepy = 0.14    # 左走最大距离
maxsteptheta = 0.3  # 转动最大角度
maxstepfrequency = 0.6  # 行走频率
stepheight = 0.02     # 抬脚高度
torsowx = 0.0
torsowy = 0.0
cameraH = 47.8 # 相机高度
# 初始姿态
shouganJoint = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"]
shouganSongshou = [1.0995575, -0.0069813, -1.4486233, -1.0314896, -1.6737708, 1.0]
shouganFangxia = [1.462586, 0.0820305, -1.4765486, -0.0349066, 0.0]
_stepStatue = [["MaxStepX", 0.04], ["MaxStepY", 0.14], ["MaxStepTheta", 0.3], ["MaxStepFrequency", 0.6],
               ["StepHeight", 0.02], ["TorsoWx", 0], ["TorsoWy", 0]]

_stepStatue2 = [["MaxStepX", 0.02], ["MaxStepY", 0.14], ["MaxStepTheta", 0.3], ["MaxStepFrequency", 0.6],
               ["StepHeight", 0.02], ["TorsoWx", 0], ["TorsoWy", 0]]
# 右部关节  肩部横轴 肩部竖轴 肘部横轴 肘部竖轴 手腕横轴 手指
PositionJointNamesR = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
# 左部关节  肩部横轴 肩部竖轴 肘部横轴 肘部竖轴 手腕横轴 手指
PositionJointNamesL = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"]
# 预设关节角度 弧度制
golfPositionJointAnglesR1 = [1.4172073526193958, 0.061086523819801536, 1.6022122533307945, 1.4835298641951802,
                             0.038397243543875255, 0.12]
golfPositionJointAnglesR2 = [1.4172073526193958, 0.061086523819801536, 1.6022122533307945, 1.4835298641951802,
                             -0.538397243543875255, 0.12]
golfPositionJointAnglesR31 = [1.35787, 0.05760, 1.50098, 1.50971, 0.667945, 0.12]
golfPositionJointAnglesR101 = [1.3, 0.05760, 1.50098, 1.35, 0.767945, 0.12]
golfPositionJointAnglesR111 = [1.35787, 0.05760, 1.50098, 1.50971, -0.738397, 0.12]
golfPositionJointAnglesR11 = [1.35787, 0.05760, 1.50098, 1.50971, -0.538397, 0.12]
golfPositionJointAnglesR32 = [1.35787, 0.05760, 1.50098, 1.50971, -0.767944870877505, 0.12]
golfPositionJointAnglesR12 = [1.35787, 0.05760, 1.50098, 1.50971, 0.767944870877505, 0.12]
golfPositionJointAnglesR42 = [1.02974, 0.24958, 1.61094, 1.10828, -0.43633, 0.12]
# golfPositionJointAnglesR5 = [1.35787, 0.05760, 1.50098, 1.50971, 0.0, 0.6]  # 原始数据 握杆前
golfPositionJointAnglesR5 = [1.319469, -0.5131268, 1.6615535, 1.3578662, 0.2076942, 1.0]
# golfPositionJointAnglesR6 = [1.35787, 0.05760, 1.50098, 1.50971, 0.0, 0.12]   # 原始数据 握杆后
golfPositionJointAnglesR6 = [1.319469, -0.5131268, 1.6615535, 1.3578662, 0.2076942, 0.0]
golfPositionJointAnglesR61 = [1.319469, -0.5131268, 1.6615535, 1.3578662, -0.7976155, 0.0]#加蓄力动作
golfPositionJointAnglesR7 = [1.02629, 0.314159, 1.62907, 1.48342, 0.230058, 0.12]  # 原数据
# golfPositionJointAnglesR7 = [1.1868239, 0.0698132, 1.6144296, 0.12514011, 0.3804818, 0.0]
golfPositionJointAnglesR8 = [1.18857, -0.67719, 1.17635, 1.52193, 0.666716, 0.50]
golfPositionJointAnglesR9 = [1.47480, -0.17453, 1.18159, 0.41190, 0.10996, 0.12]
golfPositionJointAnglesR10 = [1.46084, 0.26005, -1.37008, -0.08901, -0.02792, 0.12]
golfPositionJointAnglesR101 = [1.1868239, 0.0698132, 1.6144296, 1.2514011, 1.565897, 0.0]
# 肘部竖轴 肩部轴承 肩部横轴 肘部横轴 手腕横轴 手指
GPositionJointNamesR = ["RElbowRoll", "RShoulderRoll", "RShoulderPitch", "RElbowYaw", "RWristYaw", "RHand"]
GgolfPositionJointAnglesR1 = [1.4835298641951802, 0.061086523819801536, 1.4172073526193958, 1.6022122533307945,
                              0.038397243543875255, 0.12]
GgolfPositionJointAnglesR11 = [1.4835298641951802, 0.061086523819801536, 1.4172073526193958, 1.6022122533307945,
                               -0.538397243543875255, 0.12]
GgolfPositionJointAnglesR2 = [1.4835298641951802, 0.061086523819801536, 1.1, 1.6022122533307945, 0.038397243543875255,
                              0.12]
GgolfPositionJointAnglesR3 = [1.4835298641951802, 0.061086523819801536, 1.4172073526193958, 1.6022122533307945,
                              0.767944870877505, 0.12]
GgolfPositionJointAnglesR4 = [1.03549, 0.314159, 1.66742, 0.971064, -0.980268, 0.12]
GgolfPositionJointAnglesR5 = [1.4835298641951802, 0.061086523819801536, 1.4172073526193958, 1.6022122533307945,
                              0.038397243543875255, 0.6]  # 松杆参数
GgolfPositionJointAnglesR6 = [1.4835298641951802, 0.061086523819801536, 1.4172073526193958, 1.6022122533307945,
                              0.038397243543875255, 0.04]  # 抓杆参数

visualBasis = VisualBasis(IP,cameraId=0, resolution=vd.kVGA)
ballDetect = BallDetect(IP, resolution=vd.kVGA, writeFrame=True)
stickDetect = StickDetect(IP, cameraId=0, resolution=vd.kVGA, writeFrame=True)
landMarkDetect = LandMarkDetect(IP)
#visualBasis.motionProxy.wakeUp()
#visualBasis.postureProxy.goToPosture("StandInit", 0.5)
motionPrx = ALProxy("ALMotion", IP, 9559)
tts = ALProxy("ALTextToSpeech", IP, 9559)
memoryProxy = ALProxy("ALMemory", IP, 9559)
# #红球检测
# while 1:
# 	time1 = time.time()
angle = -60
reallyAngle = [ angle / 180  * math.pi]


# 红球识别及定位信息的获得
# ,angleInterpolationWithSpeed(第一个参数为关节名，第二个为目标角度，第三个为最大速度)
# motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR0,0.2)

# 准备动作
motionPrx.angleInterpolationWithSpeed(GPositionJointNamesR, GgolfPositionJointAnglesR1, 0.2)
# 睡眠一秒
time.sleep(1)
motionPrx.angleInterpolationWithSpeed(GPositionJointNamesR, GgolfPositionJointAnglesR2, 0.2)
time.sleep(0.5)
motionPrx.angleInterpolationWithSpeed(GPositionJointNamesR, GgolfPositionJointAnglesR3, 0.2)
time.sleep(1)
motionPrx.angleInterpolationWithSpeed(GPositionJointNamesR, GgolfPositionJointAnglesR11, 0.6)
motionPrx.stiffnessInterpolation("Body", 1, 1)
print("stiff_set finished")

# 握杆
def zhuagan():
    while True:
        # 从memory中获得数据，得到人触摸中部传感器的数据
        # RighthandTouchedFlag = memoryProxy.getData("HandRightRightTouched")
        headTouchedmidlleFlag = memoryProxy.getData("MiddleTactilTouched")
        if headTouchedmidlleFlag == 1.0:
            print("right hand touched")
            tts.say("give me!")
            motionPrx.angleInterpolationWithSpeed(PositionJointNamesR, golfPositionJointAnglesR5, 0.4)
            time.sleep(5)            # 单位 秒
            motionPrx.angleInterpolationWithSpeed(PositionJointNamesR, golfPositionJointAnglesR6, 0.1)
            time.sleep(3)
            # motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR2,0.4)
            """  
            motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR2,0.4)
            motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR1,0.4)
            """
            break
# 击球
def kaiBall():
    motionPrx.angleInterpolationWithSpeed(PositionJointNamesR, golfPositionJointAnglesR61, 0.2)
    # motionPrx.angleInterpolationWithSpeed(PositionJointNamesR, golfPositionJointAnglesR7, 0.2)
    # time.sleep(1)
    # # motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR2,0.2)
    # time.sleep(0.5)
    # motionPrx.angleInterpolationWithSpeed(PositionJointNamesR, golfPositionJointAnglesR31, 0.1)
    # time.sleep(1)
    # # motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR11,0.15)
    #
    # # 添加程序
    # effectornamelist = ["RWristYaw"]  # 修改过 effectornamelist = ["RWristYaw"]
    # timelist = [0.7]
    # targetlist = [-65 * math.pi / 180.0]
    # motionPrx.angleInterpolation(effectornamelist, targetlist, timelist, True)
    time.sleep(0)
    motionPrx.angleInterpolationWithSpeed(PositionJointNamesR, golfPositionJointAnglesR101, 1.0)
    time.sleep(1)
def shougang(): # 收杆
    # 声明三个空列表
    names = list()      # 关节名
    times = list()      # 关节移动所用时间
    keys = list()       # 关节坐标
    # 添加头部横轴 关节动作
    names.append("HeadPitch")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("HeadYaw")  # Z轴动
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])
    # ankle 脚踝
    names.append("LAnklePitch")  # 脚踝Z轴
    times.append([1, 2, 3, 4])
    keys.append([-0.349794, -0.349794, -0.349794, -0.349794])

    names.append("LAnkleRoll")  # 脚踝X轴
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])
    # elbow 肘部
    names.append("LElbowRoll")  # 肘Z轴
    times.append([1, 2, 3, 4])
    keys.append([-0.321141, -0.321141, -1.1, -1.1])

    names.append("LElbowYaw")  # X轴
    times.append([1, 2, 3, 4])
    keys.append([-1.37757, -1.37757, -1.466076, -1.466076])

    names.append("LHand")  # 左掌
    times.append([1, 2, 3, 4, 5.2])
    keys.append([0.9800, 0.9800, 0.9800, 0.9800, 0.1800])
    # hip 臀部
    names.append("LHipPitch")  # 腿Y轴
    times.append([1, 2, 3, 4])
    keys.append([-0.450955, -0.450955, -0.450955, -0.450955])

    names.append("LHipRoll")  # 腿X轴
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("LHipYawPitch")  # 啥关节
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("LKneePitch")  # 膝盖Y轴
    times.append([1, 2, 3, 4])
    keys.append([0.699462, 0.699462, 0.699462, 0.699462])

    names.append("LShoulderPitch")  # 左肩轴
    times.append([1, 2, 3, 4, 5.2])
    ##------------------------------------------------------------
    keys.append([1.53885, 1.43885, 1.3, 1.3, 1.3])

    names.append("LShoulderRoll")  # 肩Z轴
    times.append([1, 2, 3, 4, 5.2])
    keys.append([0.268407, 0.268407, -0.04014, -0.04014, -0.04014])

    names.append("LWristYaw")  # 手腕X轴
    times.append([1, 2, 3, 4])
    keys.append([-0.016916, -0.016916, -1.632374, -1.632374])

    names.append("RAnklePitch")  # 脚踝Y轴
    times.append([1, 2, 3, 4])
    keys.append([-0.354312, -0.354312, -0.354312, -0.354312])

    names.append("RAnkleRoll")  # 脚踝X轴
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("RElbowRoll")  # 肘Z轴
    times.append([1, 2, 3, 4])
    keys.append([0.958791, 0.958791, 0.958791, 0.958791])

    names.append("RElbowYaw")  # 肘X轴
    times.append([1, 2, 3, 4])
    keys.append([1.466076, 1.466076, 1.466076, 1.466076])

    names.append("RHand")
    times.append([1, 2, 3, 4])
    keys.append([0.0900, 0.0900, 0.0900, 0.0900])

    names.append("RHipPitch")  # 腿Y轴
    times.append([1, 2, 3, 4])
    keys.append([-0.451038, -0.451038, -0.451038, -0.451038])

    names.append("RHipRoll")  # 腿X轴
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("RHipYawPitch")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("RKneePitch")  # 膝盖Y轴
    times.append([1, 2, 3, 4])
    keys.append([0.699545, 0.699545, 0.699545, 0.699545])

    names.append("RShoulderPitch")  # 肩Y轴
    times.append([0.5,1, 2, 3, 4, 5.2])
    # keys.append([1.03856, 1.03856, 1.03856, 1.03856, 1.03856])
    keys.append([0.9, 1.03856, 1.03856,1.03856, 1.03856, 1.03856])

    names.append("RShoulderRoll")  # 肩Z轴
    times.append([1, 2, 3, 4, 5.2])
    keys.append([0.04014, 0.04014, 0.04014, 0.04014, 0.04014])

    names.append("RWristYaw")  # 腕X轴
    times.append([1, 2, 3, 4])
    keys.append([1.632374, 1.632374, 1.632374, 1.632374])
    motionPrx.setMoveArmsEnabled(False, False)  # 设置移动时候左右手不动
    motionPrx.angleInterpolation(names, keys, times, True)  # 如果为true，则以绝对角度描述运动，否则角度相对于当前角度why？

def LShoulderpitchAmend():
    names = list()
    keys = list()
    times = list()
    names.append("LShoulderPitch")  #
    times.append([1])
    keys.append([1.03856])
    names.append("LHand")
    times.append([1, 2, 3, 4])
    keys.append([0.0200, 0.0200, 0.0200, 0.0200])
    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.angleInterpolation(names, keys, times, True)

def ShoulderpitchAmend2():
    names = list()
    keys = list()
    times = list()
    names.append("LShoulderPitch")  #
    times.append([0.5, 1])
    keys.append([1.43856, 1.88495559])
    names.append("RShoulderPitch")  #
    times.append([0.5, 1])
    keys.append([1.43856, 1.88495559])
    names.append("LElbowRoll")  #
    times.append([0.5, 1])
    keys.append([-1.23490659, -1.51843645])
    names.append("RElbowRoll")  #
    times.append([0.5, 1])
    keys.append([1.23490659, 1.51843645])
    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.angleInterpolation(names, keys, times, True)






# 开始找球
while 1:
    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.moveTo(0.2, 0.0, 0.0, _stepStatue)
    time.sleep(1)
    ballDetect.updateBallData(client="xxxx", colorSpace="HSV", fitting=True)
    motionPrx.moveTo(0.0, 0.0, redballFlag)
    if redballFlag == 0 :
        break
while 1:
    stickDetect.updateStickData(client="xxx")
    motionPrx.moveTo(0.0, 0.0, reallyAngle)
    time.sleep(1)
    if redballFlag == 0 :
        break

# 找到黄杆
motionPrx.moveTo(0.0, 0.0, stickDetect.stickAngle)
motionPrx.angleInterpolationWithSpeed("HeadYaw", headAngle["standInit"], 0.2)
# 更新mark数据
landMarkDetect.updateLandMarkData(client="xxx")

# 更新红球数据
ballDetect.updateBallData(client="xxxx", colorSpace="HSV", fitting=True)


# 计算距离
if redballFlag == 0 and landmarkFlag == 0:
    x1 = ballDetect.ballPosition["disX"]
    y1 = ballDetect.ballPosition["disY"]
    x2 = landMarkDetect.disX            # (x2, 0) 为与x轴交点
    y2 = (-y1)*x2 / (x1 - x2)           # (0, y2) 为与y轴交点
    alpha = math.atan(x2 / y2)          # 通过atan的函数算出角度
    beta = math.pi - alpha

# 调整角度
motionPrx.setMoveArmsEnabled(False, False)
motionPrx.moveTo(x1 - 0.05, ballDetect.ballPosition["disY"], 0.0, _stepStatue)
motionPrx.moveTo(0, 0.08, 0, _stepStatue)
motionPrx.moveTo(0.12, 0, 0, _stepStatue)
motionPrx.moveTo(0, 0, beta, _stepStatue)
ballDetect.updateBallData(client="xxxx", colorSpace="HSV", fitting=True)
if ballDetect.ballPosition["disX"] <= 5 and ballDetect.ballPosition["disY"] <=0.02 and ballDetect.ballPosition["disY"] >=0:
    # 此处加入松杆代码
    motionPrx.angleInterpolationWithSpeed(shouganJoint, shouganSongshou, 0.2)
    motionPrx.angleInterpolationWithSpeed(shouganJoint, shouganFangxia, 0.2)
    # 击球然后收杆
    kaiBall()
    shougang()
    LShoulderpitchAmend()
    ShoulderpitchAmend2()

# 黄杆检测
# stickDetect.updateStickData(client="xxx")
# 	stickDetect.showStickPosition()
# 	cv2.waitKey(1000)

# mark检测
#
# while 1:

# 	landMarkDetect.showLandMarkData()
# 	time.sleep(1)

#
# print("start collecting...")
# for i in range(10):
# 	imgName = "stick_" + str(i+127) + ".jpg"
# 	imgDir = os.path.join("stick_images", imgName)
# 	visualBasis.updateFrame()
# 	visualBasis.showFrame(timeMs=1000)
# 	visualBasis.saveFrame(imgDir)
# 	print ("saved in ", imgDir)
# 	time.sleep(5)


"""
visualBasis._tts.say("hello world")
"""

"""
visualBasis._motionProxy.wakeUp()
"""


# dataList = visualBasis._memoryProxy.getDataList("camera")
# print (dataList)


"""
visualBasis._motionProxy.setStiffnesses("Body", 1.0)
visualBasis._motionProxy.moveInit()
"""

#motionProxy = ALProxy("ALMotion", IP, 9559)
#postureProxy = ALProxy("ALRobotPosture", IP, 9559)

#motionProxy.wakeUp()
#postureProxy.goToPosture("StandInit", 0.5)


#motionProxy.wakeUp()
#motionProxy.goToPosture("StandInit", 0.5)
#motionProxy.moveToward(0.1, 0.1, 0, [["Frequency", 1.0]])
#motionProxy.moveTo(0.3, 0.2, 0)
"""
"""


def headtouch(): # 摸头
    while True:
        # 从memory中获得数据， 得到人触摸前头传感器的数据 tactil 触觉的
        headTouchedButtonFlag = memoryProxy.getData("FrontTactilTouched")
        if headTouchedButtonFlag == 1.0:
            print("front head touched")
            tts.say("I am ready to hit")
            break
    print("Head select information successfully")

def zhuagan(): # 抓杆
    while True:
        # 从memory中获得数据，得到人触摸中部传感器的数据
        # RighthandTouchedFlag = memoryProxy.getData("HandRightRightTouched")
        headTouchedmidlleFlag = memoryProxy.getData("MiddleTactilTouched")
        if headTouchedmidlleFlag == 1.0:
            print("right hand touched")
            tts.say("give me!")
            motionPrx.angleInterpolationWithSpeed(PositionJointNamesR, golfPositionJointAnglesR5, 0.4)
            time.sleep(5)            # 单位 秒
            motionPrx.angleInterpolationWithSpeed(PositionJointNamesR, golfPositionJointAnglesR6, 0.1)
            time.sleep(3)
            # motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR2,0.4)
            """  
            motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR2,0.4)
            motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR1,0.4)
            """
            break
            print("finnished")  # 待修改

def shougang(): # 收杆
    # 声明三个空列表
    names = list()      # 关节名
    times = list()      # 关节移动所用时间
    keys = list()       # 关节坐标
    # 添加头部横轴 关节动作
    names.append("HeadPitch")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("HeadYaw")  # Z轴动
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])
    # ankle 脚踝
    names.append("LAnklePitch")  # 脚踝Z轴
    times.append([1, 2, 3, 4])
    keys.append([-0.349794, -0.349794, -0.349794, -0.349794])

    names.append("LAnkleRoll")  # 脚踝X轴
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])
    # elbow 肘部
    names.append("LElbowRoll")  # 肘Z轴
    times.append([1, 2, 3, 4])
    keys.append([-0.321141, -0.321141, -1.1, -1.1])

    names.append("LElbowYaw")  # X轴
    times.append([1, 2, 3, 4])
    keys.append([-1.37757, -1.37757, -1.466076, -1.466076])

    names.append("LHand")  # 左掌
    times.append([1, 2, 3, 4, 5.2])
    keys.append([0.9800, 0.9800, 0.9800, 0.9800, 0.1800])
    # hip 臀部
    names.append("LHipPitch")  # 腿Y轴
    times.append([1, 2, 3, 4])
    keys.append([-0.450955, -0.450955, -0.450955, -0.450955])

    names.append("LHipRoll")  # 腿X轴
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("LHipYawPitch")  # 啥关节
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("LKneePitch")  # 膝盖Y轴
    times.append([1, 2, 3, 4])
    keys.append([0.699462, 0.699462, 0.699462, 0.699462])

    names.append("LShoulderPitch")  # 左肩轴
    times.append([1, 2, 3, 4, 5.2])
    ##------------------------------------------------------------
    keys.append([1.53885, 1.43885, 1.3, 1.3, 1.3])

    names.append("LShoulderRoll")  # 肩Z轴
    times.append([1, 2, 3, 4, 5.2])
    keys.append([0.268407, 0.268407, -0.04014, -0.04014, -0.04014])

    names.append("LWristYaw")  # 手腕X轴
    times.append([1, 2, 3, 4])
    keys.append([-0.016916, -0.016916, -1.632374, -1.632374])

    names.append("RAnklePitch")  # 脚踝Y轴
    times.append([1, 2, 3, 4])
    keys.append([-0.354312, -0.354312, -0.354312, -0.354312])

    names.append("RAnkleRoll")  # 脚踝X轴
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("RElbowRoll")  # 肘Z轴
    times.append([1, 2, 3, 4])
    keys.append([0.958791, 0.958791, 0.958791, 0.958791])

    names.append("RElbowYaw")  # 肘X轴
    times.append([1, 2, 3, 4])
    keys.append([1.466076, 1.466076, 1.466076, 1.466076])

    names.append("RHand")
    times.append([1, 2, 3, 4])
    keys.append([0.0900, 0.0900, 0.0900, 0.0900])

    names.append("RHipPitch")  # 腿Y轴
    times.append([1, 2, 3, 4])
    keys.append([-0.451038, -0.451038, -0.451038, -0.451038])

    names.append("RHipRoll")  # 腿X轴
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("RHipYawPitch")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("RKneePitch")  # 膝盖Y轴
    times.append([1, 2, 3, 4])
    keys.append([0.699545, 0.699545, 0.699545, 0.699545])

    names.append("RShoulderPitch")  # 肩Y轴
    times.append([0.5,1, 2, 3, 4, 5.2])
    # keys.append([1.03856, 1.03856, 1.03856, 1.03856, 1.03856])
    keys.append([0.9, 1.03856, 1.03856,1.03856, 1.03856, 1.03856])

    names.append("RShoulderRoll")  # 肩Z轴
    times.append([1, 2, 3, 4, 5.2])
    keys.append([0.04014, 0.04014, 0.04014, 0.04014, 0.04014])

    names.append("RWristYaw")  # 腕X轴
    times.append([1, 2, 3, 4])
    keys.append([1.632374, 1.632374, 1.632374, 1.632374])
    motionPrx.setMoveArmsEnabled(False, False)  # 设置移动时候左右手不动
    motionPrx.angleInterpolation(names, keys, times, True)  # 如果为true，则以绝对角度描述运动，否则角度相对于当前角度why？
