# coding:utf-8

from naoqi import ALProxy
import numpy as np
import cv2
import vision_definitions
IP = "192.168.31.120"
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

# 初始姿态
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
golfPositionJointAnglesR7 = [1.02629, 0.314159, 1.62907, 1.48342, 0.230058, 0.12]  # 原数据
# golfPositionJointAnglesR7 = [1.1868239, 0.0698132, 1.6144296, 0.12514011, 0.3804818, 0.0]
golfPositionJointAnglesR8 = [1.18857, -0.67719, 1.17635, 1.52193, 0.666716, 0.50]
golfPositionJointAnglesR9 = [1.47480, -0.17453, 1.18159, 0.41190, 0.10996, 0.12]
golfPositionJointAnglesR10 = [1.46084, 0.26005, -1.37008, -0.08901, -0.02792, 0.12]
golfPositionJointAnglesR101 = [1.1868239, 0.0698132, 1.6144296, 1.2514011, 0.3804818, 0.0]
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
motionProxy = ALProxy("ALMotion", IP, port = 9559)
cameraProxy = ALProxy("ALVideoDevice", IP, port = 9559)
memoryProxy = ALProxy("ALMemory", IP, port = 9559)
