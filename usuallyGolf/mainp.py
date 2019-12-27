import math
import almath
import time
import argparse
import redball000
import time
import landmark1
from naoqi import ALProxy


#申请所需要的各种服务

#本机IP 127.0.0.1
robotIP = "127.0.0.1"
IP = robotIP
#默认端口号 9559
PORT = 9559
# ********************motion init
motionProxy = ALProxy("ALMotion", robotIP, PORT)
# *******************posture init
postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
# ***********************Memory init
memoryProxy = ALProxy("ALMemory", robotIP, PORT)
camProxy = ALProxy("ALVideoDevice", IP, PORT)
landMarkProxy = ALProxy("ALLandMarkDetection", IP, PORT)
memoryProxy = ALProxy("ALMemory", IP, PORT)


#函数功能：站立拿球棒，手指张开为20秒，并且拿住球棒之后，将手臂放下
#参数： 无
def StandToGetstick():
	#初始化站立姿势
    postureProxy.goToPosture("Stand", 0.4)

    names = ['RShoulderRoll', 'RElbowRoll']
    angleLists = [-20.0 * almath.TO_RAD, 2.0 * almath.TO_RAD]
    timeLists = [1.0, 1.5]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(1.0)

    names = ['RShoulderRoll', 'RElbowYaw', 'RShoulderPitch']
    angleLists = [-45.0 * almath.TO_RAD, -4.0 * almath.TO_RAD, 4.0 * almath.TO_RAD]
    timeLists = [1.0, 1.5, 2.0]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(1.0)

    motionProxy.openHand('RHand')
	
	#设置手指张开的时间
    time.sleep(20.0)
	
    motionProxy.closeHand('RHand')
    motionProxy.setStiffnesses('RHand', 1.0)

    names = ['RShoulderPitch', 'RElbowYaw', 'RShoulderRoll']
    angleLists = [84.0 * almath.TO_RAD, 68.0 * almath.TO_RAD, -25.0 * almath.TO_RAD]
    timeLists = [1.0, 1.5, 2.0]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(1.0)

#函数功能：开始击球
#参数： power-击球力度，power越小，击球力度越大
def HitBall(power):
    postureProxy.goToPosture("Stand", 0.4)
    names = ['RShoulderRoll', 'RElbowRoll']
    angleLists = [-25.0 * almath.TO_RAD, 2.0 * almath.TO_RAD]
    timeLists = [1.0, 1.5]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(1.0)

    names = ['RShoulderRoll', 'RElbowYaw', 'RShoulderPitch']
    angleLists = [-45.0 * almath.TO_RAD, -4.0 * almath.TO_RAD, 4.0 * almath.TO_RAD]
    timeLists = [1.0, 1.5, 2.0]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(1.0)

    names = ['RWristYaw', 'RElbowYaw', 'RShoulderRoll', 'RElbowRoll', 'RShoulderPitch']
    angleLists = [-100.0 * almath.TO_RAD, 100.0 * almath.TO_RAD, 0.0 * almath.TO_RAD, 9.0 * almath.TO_RAD,
                  9.0 * almath.TO_RAD]
    timeLists = [1.0, 1.5, 2.0, 2.5, 3]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(2.0)

    names = 'RWristYaw'
	#手腕转动的幅度
    angleLists = 60.0 * almath.TO_RAD
	#power
    timeLists = power
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(1.0)
    time.sleep(1.0)

    names = ['RShoulderRoll', 'RElbowRoll', 'RShoulderPitch']
    angleLists = [0.0 * almath.TO_RAD, -20.0 * almath.TO_RAD, -20.0 * almath.TO_RAD]
    timeLists = [1.0, 1.5, 2.0, 2.5, 3]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(2.0)

    names = 'RWristYaw'
    angleLists = -100.0 * almath.TO_RAD
    timeLists = 1.0
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(1.0)

    names = ['RShoulderPitch', 'RElbowRoll', 'RShoulderRoll', 'RElbowYaw', 'RWristYaw']
    angleLists = [4 * almath.TO_RAD, -45.0 * almath.TO_RAD, -45.0 * almath.TO_RAD, -4.0 * almath.TO_RAD,
                  4.0 * almath.TO_RAD]
    timeLists = [1.0, 1.5, 2.0, 2.5, 3]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(2.0)

    names = ['RShoulderPitch', 'RElbowYaw', 'RShoulderRoll']
    angleLists = [84.0 * almath.TO_RAD, 68.0 * almath.TO_RAD, -25.0 * almath.TO_RAD]
    timeLists = [1.0, 1.5, 2.0]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(1.0)

#函数功能：缓慢向前走，即走一会，停一会。为了防止走路过快，摔倒所用
#参数： d-行走距离  正为前走  负为后走
#额外说明：由于代码编写人员测试场地比较平坦，因此没有使用。如需使用：删除未注释的代码，并且注释的代码恢复即可。 
def Movex(d):
    x = d
    y = 0.0
    theta = 0.0
    motionProxy.moveTo(x, y, theta)
	# #此参数为停顿时间
    # sleep_time=0.7
	# #此参数为每次行走的距离
    # mdistance=0.15
    # if(d>0):
    #     while(1):
    #         if (d<=mdistance):
    #             x = d
    #             y = 0.0
    #             theta = 0.0
    #             motionProxy.moveTo(x, y, theta)
    #             #time.sleep(sleep_time)
    #             break
    #         else:
    #             x =mdistance
    #             y = 0.0
    #             theta = 0.0
    #             motionProxy.moveTo(x, y, theta)
    #             #time.sleep(sleep_time)
    #             d=d-mdistance
    # else:
    #     d=-d
    #     while(1):
    #         if (d<=mdistance):
    #             x = -d
    #             y = 0.0
    #             theta = 0.0
    #             motionProxy.moveTo(x, y, theta)
    #             #time.sleep(sleep_time)
    #             break
    #         else:
    #             x = -mdistance
    #             y = 0.0
    #             theta = 0.0
    #             motionProxy.moveTo(x, y, theta)
    #             #time.sleep(sleep_time)
    #             d=d-mdistance

#函数功能：缓慢横向走，即走一会，停一会。为了防止走路过快，摔倒所用
#参数： d-行走距离  正为前走  负为后走
def Movey(d):
    sleep_time = 0.5
    mdistance = 0.15
    if (d > 0):
        while (1):
            if (d <= mdistance):
                x = 0
                y = d
                theta = 0.0
                motionProxy.moveTo(x, y, theta)
                time.sleep(sleep_time)
                break
            else:
                x = 0.0
                y = mdistance
                theta = 0.0
                motionProxy.moveTo(x, y, theta)
                time.sleep(sleep_time)
                d = d - mdistance
    else:
        d = -d
        while (1):
            if (d <= mdistance):
                x = 0
                y = -d
                theta = 0.0
                motionProxy.moveTo(x, y, theta)
                time.sleep(sleep_time)
                break
            else:
                x = 0.0
                y = -mdistance
                theta = 0.0
                motionProxy.moveTo(x, y, theta)
                time.sleep(sleep_time)
                d = d - mdistance

#函数功能：缓慢转向，即走一会，停一会。为了防止走路过快，摔倒所用
#参数： d-行走距离 
#额外说明：由于代码编写人员测试场地比较平坦，因此没有使用。如需使用：删除未注释的代码，并且注释的代码恢复即可。 
def Movet(t):
    x = 0.0
    y = 0.0
    theta = t
    motionProxy.moveTo(x, y, theta)
    # sleep_time = 0.7
    # mdistance = math.pi/10
    # if(t>0):
    #     while(1):
    #         if (t<=( mdistance)):
    #             x = 0
    #             y = 0
    #             theta = t
    #             motionProxy.moveTo(x, y, theta)
    #             #time.sleep(sleep_time)
    #             break
    #         else:
    #             x = 0.0
    #             y = 0.0
    #             theta = mdistance
    #             motionProxy.moveTo(x, y, theta)
    #             #time.sleep(sleep_time)
    #             t=t-( mdistance)
    # else:
    #     t=-t
    #     while(1):
    #         if (t<=( mdistance)):
    #             x = 0
    #             y = 0
    #             theta = -t
    #             motionProxy.moveTo(x, y, theta)
    #             #time.sleep(mdistance)
    #             break
    #         else:
    #             x = 0.0
    #             y = 0.0
    #             theta = -math.pi/24
    #             motionProxy.moveTo(x, y, theta)
    #             #time.sleep(sleep_time)
    #             t=t-( mdistance)


#函数功能：检测landmark
#返回参数：五个，分别为 1、是否检测到landmark，检测到为1，未检测到为0。
#						2、landmark离摄像头的x轴距离，即横向距离
#						3、landmark离摄像头的y轴距离，即纵向距离
#						4、landmark离摄像头的z轴距离，即垂直距离
#						5、landmark离摄像头的距离 即2，3，4各自平方的和的开根号。 
def DetecteLandmark():
	#调用上摄像头
    camProxy.setParam(18, 0)
	#landmark的实际大小：10cm
    landmarkTheoreticalSize = 0.1
    currentCamera = "CameraTop"
    ip = robotIP
    period = 500
    landMarkProxy.subscribe("Test_LandMark", period, 0.0)
	#循环10次重复检查landmark
    for i in range(0, 10):
        time.sleep(0.5)
        markData = memoryProxy.getData("LandmarkDetected")
		#如果没检测到landmark
        if (markData is None or len(markData) == 0):
            continue
		#检测到landmark之后，开始算坐标
        else:
            if (len(markData) == 1):
                wzCamera = markData[1][0][0][1]
                wyCamera = markData[1][0][0][2]

                # Retrieve landmark angular size in radians.
                angularSize = markData[1][0][0][3]

                # Compute distance to landmark.
                distanceFromCameraToLandmark = landmarkTheoreticalSize / (2 * math.tan(angularSize / 2))

                motionProxy = ALProxy("ALMotion", ip, 9559)

                # Get current camera position in NAO space.
                transform = motionProxy.getTransform(currentCamera, 2, True)
                transformList = almath.vectorFloat(transform)
                robotToCamera = almath.Transform(transformList)

                # Compute the rotation to point towards the landmark.
                cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, wyCamera, wzCamera)

                # Compute the translation to reach the landmark.
                cameraToLandmarkTranslationTransform = almath.Transform(distanceFromCameraToLandmark, 0, 0)

                # Combine all transformations to get the landmark position in NAO space.

                robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform * cameraToLandmarkTranslationTransform
                landMarkProxy.unsubscribe("Test_LandMark")
                # print  "landmark detect",robotToLandmark.r1_c4,robotToLandmark.r2_c4,robotToLandmark.r3_c4,distanceFromCameraToLandmark
                return 1, robotToLandmark.r1_c4, robotToLandmark.r2_c4, robotToLandmark.r3_c4, distanceFromCameraToLandmark
            else:
                wzCamera = markData[1][0][0][1]
                wyCamera = markData[1][0][0][2]

                # Retrieve landmark angular size in radians.
                angularSize = markData[1][0][0][3]

                # Compute distance to landmark.
                distanceFromCameraToLandmark = landmarkTheoreticalSize / (2 * math.tan(angularSize / 2))

                motionProxy = ALProxy("ALMotion", ip, 9559)

                # Get current camera position in NAO space.
                transform = motionProxy.getTransform(currentCamera, 2, True)
                transformList = almath.vectorFloat(transform)
                robotToCamera = almath.Transform(transformList)

                # Compute the rotation to point towards the landmark.
                cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, wyCamera, wzCamera)

                # Compute the translation to reach the landmark.
                cameraToLandmarkTranslationTransform = almath.Transform(distanceFromCameraToLandmark, 0, 0)

                # Combine all transformations to get the landmark position in NAO space.

                robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform * cameraToLandmarkTranslationTransform
                landMarkProxy.unsubscribe("Test_LandMark")
                # print  "landmark detect", robotToLandmark.r1_c4, robotToLandmark.r2_c4, robotToLandmark.r3_c4, distanceFromCameraToLandmark
                return 1, robotToLandmark.r1_c4, robotToLandmark.r2_c4, robotToLandmark.r3_c4, distanceFromCameraToLandmark

    landMarkProxy.unsubscribe("Test_LandMark")
    # print  "landmark detect fff"
    return 0, 0, 0, 0, 0

#函数功能：检测黄杆
#返回参数：四个，分别为 1、是否检测到黄杆，检测到为1，未检测到为0。
#						2、黄杆在图片中的大小，与机器人的离黄杆的距离有算数关系
#						3、黄杆在图片中距左边框的距离，与机器人是否与黄杆正对面有算数关系
#						4、黄杆距机器人的真实距离
def DetecteLandmark_my():
    xx = 0.0
    for i in range(0, 5):
        # time.sleep(1.0)
        size, left, xx = landmark1.landmarkdetect(IP, PORT, 0)
        if ((size != 0) & (left != 0)):
            return 1, size, left, xx
        else:
            # print  "landmark_my detect fff"
            return 0, 0, 0, 0


# ***************************************************

# close to down cam,and adjust the just position to ball
#函数功能： 检测球并且靠近球。如果没检测到球则默认左转，找球。如果检测到球，分两种情况 1、 在上摄像头即朝球走，直到球在下摄像头被检测到。
#																					   2、 在下摄像头被检测到，对准球，使球在机器人的正前方。
#参数：threshold-使球在机器人正前方的阈值偏差、
#返回参数：无
def closeball1(threshold):
	#没找到球时候 默认转头的找球方向。
    LEFT_ = 0
	#低头，每次找球需要低头，来排除噪声干扰
    redball512_r.lookat(robotIP, PORT)
	#计数器等一些用于逼近的数值
    count = 1
    count0 = 0
    flag_p = 0
    flag_n = 0
    while (1):
        if (count0 == 10):
            Movey(0.5)
        size, left, top, cam, isfind = redball512_r.findball(robotIP, PORT)
        if (isfind == 1):

            if (cam == 1):

                if (left <= threshold) & (left >= -threshold):
                    break
                elif (left > threshold):
                    flag_p = 1
                    if ((flag_p == 1) & (flag_n == 1)):
                        count = count + 1
                        flag_n = 0
                    x = 0.0
                    y = 0.0
                    theta = -1 * math.pi / (10 * (2 * count))
                    motionProxy.moveTo(x, y, theta)
                    time.sleep(1.5)

                elif (left < - threshold):
                    flag_n = 1
                    if ((flag_p == 1) & (flag_n == 1)):
                        count = count + 1
                        flag_p = 0
                    x = 0.0
                    y = 0.0
                    theta = math.pi / (10 * (2 * count))
                    motionProxy.moveTo(x, y, theta)
                    time.sleep(1.5)
            else:
                if (top <= -10):
                    if (left < 30):
                        x = 0.0
                        y = 0.0
                        theta = math.pi / 15
                        motionProxy.moveTo(x, y, theta)
                        time.sleep(1.5)
                    elif (left > 30):
                        x = 0.0
                        y = 0.0
                        theta = -1 * math.pi / 15
                        motionProxy.moveTo(x, y, theta)
                        time.sleep(1.5)
                    Movex(0.45)
                elif (-10 <= top <= 50):
                    if (left < 25):
                        x = 0.0
                        y = 0.0
                        theta = math.pi / 15
                        motionProxy.moveTo(x, y, theta)
                        time.sleep(1.5)
                    elif (left > 25):
                        x = 0.0
                        y = 0.0
                        theta = -1 * math.pi / 15
                        motionProxy.moveTo(x, y, theta)
                        time.sleep(1.5)
                    Movex(0.30)
                else:
                    if (left < 25):
                        x = 0.0
                        y = 0.0
                        theta = math.pi / 15
                        motionProxy.moveTo(x, y, theta)
                        time.sleep(1.5)
                    elif (left > 25):
                        x = 0.0
                        y = 0.0
                        theta = -1 * math.pi / 15
                        motionProxy.moveTo(x, y, theta)
                        time.sleep(1.5)
                    Movex(0.15)


        else:
            if (LEFT_ == 0):
                count0 = count0 + 1
                x = 0.0
                y = 0.0
                theta = math.pi / 8
                motionProxy.moveTo(x, y, theta)
            else:
                count0 = count0 + 1
                x = 0.0
                y = 0.0
                theta = -math.pi / 8
                motionProxy.moveTo(x, y, theta)


# **********************************

# **************************
# 功能同closeball1，只是默认没找到球时，右转找球
def closeball1_right(threshold):
    LEFT_ = 0
    redball512_r.lookat(robotIP, PORT)
    count = 1
    count0 = 0
    flag_p = 0
    flag_n = 0
    while (1):
        if (count0 == 10):
            Movey(0.5)
        size, left, top, cam, isfind = redball512_r.findball(robotIP, PORT)
        if (isfind == 1):

            if (cam == 1):

                if (left <= threshold) & (left >= -threshold):
                    break
                elif (left > threshold):
                    flag_p = 1
                    if ((flag_p == 1) & (flag_n == 1)):
                        count = count + 1
                        flag_n = 0
                    x = 0.0
                    y = 0.0
                    theta = -1 * math.pi / (10 * (2 * count))
                    motionProxy.moveTo(x, y, theta)
                    time.sleep(1.5)

                elif (left < - threshold):
                    flag_n = 1
                    if ((flag_p == 1) & (flag_n == 1)):
                        count = count + 1
                        flag_p = 0
                    x = 0.0
                    y = 0.0
                    theta = math.pi / (10 * (2 * count))
                    motionProxy.moveTo(x, y, theta)
                    time.sleep(1.5)
            else:
                if (top <= -10):
                    if (left < 30):
                        x = 0.0
                        y = 0.0
                        theta = math.pi / 15
                        motionProxy.moveTo(x, y, theta)
                        time.sleep(1.5)
                    elif (left > 30):
                        x = 0.0
                        y = 0.0
                        theta = -1 * math.pi / 15
                        motionProxy.moveTo(x, y, theta)
                        time.sleep(1.5)
                    Movex(0.45)
                elif (-10 <= top <= 50):
                    if (left < 25):
                        x = 0.0
                        y = 0.0
                        theta = math.pi / 15
                        motionProxy.moveTo(x, y, theta)
                        time.sleep(1.5)
                    elif (left > 25):
                        x = 0.0
                        y = 0.0
                        theta = -1 * math.pi / 15
                        motionProxy.moveTo(x, y, theta)
                        time.sleep(1.5)
                    Movex(0.30)
                else:
                    if (left < 25):
                        x = 0.0
                        y = 0.0
                        theta = math.pi / 15
                        motionProxy.moveTo(x, y, theta)
                        time.sleep(1.5)
                    elif (left > 25):
                        x = 0.0
                        y = 0.0
                        theta = -1 * math.pi / 15
                        motionProxy.moveTo(x, y, theta)
                        time.sleep(1.5)
                    Movex(0.15)


        else:
            if (LEFT_ == 0):
                count0 = count0 + 1
                x = 0.0
                y = 0.0
                theta = math.pi / 8
                motionProxy.moveTo(x, y, theta)
            else:
                count0 = count0 + 1
                x = 0.0
                y = 0.0
                theta = -math.pi / 8
                motionProxy.moveTo(x, y, theta)


# *********************************************************
#函数功能：每次调用closeball1之后需要调用此函数，用来靠近球
#参数：threshold-此参数是调整机器人走进距离球的远近， close1-此参数同close1的threshold
def closeball2(threshold, close1):
	#使机器人低下头
    redball512_r.lookat(robotIP, PORT)
    while (1):

        size, left, top, cam, isfind = redball512_r.findball(robotIP, PORT)
        if (isfind == 1):

            if (top >= threshold):
                closeball1(close1)
                break



            elif (-60 <= top < 20):
                x = 0.02
                y = 0.0
                theta = 0
                motionProxy.moveTo(x, y, theta)
                time.sleep(1.8)
                closeball1(close1)
            elif (20 <= top < threshold):
                x = 0.02
                y = 0.0
                theta = 0.0
                motionProxy.moveTo(x, y, theta)
                time.sleep(1.8)
                closeball1(27)

            elif (top < -60):
                x = 0.07
                y = 0.0
                theta = 0.0
                motionProxy.moveTo(x, y, theta)
                time.sleep(1.8)

        else:
            pass



            #  distance in meter 0.011


# *************************************************

# **************************************
#函数功能：靠近球之后，走到击球处。
#参数：threshold-此参数调整误差大小时间需要的久，太大时间多， topdistance-靠近球的时候球距离机器人球在图像中距离相框头部的距离， ditance-球距离机器人的真实距离
##返回参数：四个，分别为 
#						 1、landmark离摄像头的x轴距离，即横向距离
#						 2、landmark离摄像头的y轴距离，即纵向距离
#						 3、landmark离摄像头的z轴距离，即垂直距离
#						 4、landmark离摄像头的距离 即2，3，4各自平方的和的开根号。 
def newruntohitball(threshold, topdistance, ditance):
    # turn head
    # detecteland
    # Movex(-0.08)
    close1_ = 23
    count = 0
    fivefindlandmark = 0
    change = 8.0
    while (1):
        names = ["HeadPitch", "HeadYaw"]
        angleLists = [0 * almath.TO_RAD, (90.0 + change) * almath.TO_RAD]
        timeLists = [1.0, 2.0]
        isAbsolute = True
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        time.sleep(2.0)
        isfindLand, x, y, z, d = DetecteLandmark()
        time.sleep(2.0)
        print  "landmark"
        # 90 degre cannot find
        if (isfindLand == 0):
            for i in range(0, 5):
                # ***********************
                names = ["HeadPitch", "HeadYaw"]
                angleLists = [0.0 * almath.TO_RAD, ((60.0 - i * 30.0) + change) * almath.TO_RAD]
                timeLists = [1.0, 2.0]
                isAbsolute = True
                motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
                time.sleep(1.0)
                # *****************************
                isfindLand, x, y, z, d = DetecteLandmark()
                # find landmark

                if (isfindLand == 1):
                    if (i == 0):
                        t_ = 0.08
                    elif (i == 1):
                        t_ = 0.12
                    elif (i == 2):
                        t_ = 0.16
                    elif (i == 3):
                        t_ = 0.20
                    elif (i == 4):
                        t_ = 0.24
                    elif (i == 5):
                        t_ = 0.30
                    Movey(t_)
                    Movet(-0.75 * (math.atan(t_ / ditance)))
                    fivefindlandmark = 1
                    break
                else:
                    pass
            if (fivefindlandmark == 0):
                t_ = -0.30
                Movey(t_)
                Movet(-0.75 * math.atan(t_ / ditance))
            closeball1(20)
            closeball2(topdistance, close1_)



        elif (((x - ditance) < threshold) & ((x - ditance) > -threshold)):
            print x, threshold + ditance, ditance - threshold
            return x, y, z, d
        elif (x - ditance < -threshold):
            print x, threshold + ditance, ditance - threshold
            Movey(-0.04)
            redball512_r.lookat(robotIP, PORT)
            # *************************************
            closeball1(17)
            closeball2(topdistance, close1_)
        else:
            count = count + 1
            Movey(0.04)
            redball512_r.lookat(robotIP, PORT)
            closeball1(17)
            closeball2(topdistance, close1_)


# **************************************



#说明:与newruntohitball的功能一样，这个是旧版本的，已经被抛弃了
def runtohitball(threshold, topdistance, ditance):
    # ***********************
    close1_ = 23
    names = ["HeadPitch", "HeadYaw"]
    angleLists = [0.0 * almath.TO_RAD, 0.0 * almath.TO_RAD]
    timeLists = [1.0, 2.0]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(1.0)

    # *****************************
    while (1):
        isfindLand, x, y, z, d = DetecteLandmark()
        # find landmark
        if (isfindLand == 1):
            if (x < 0):
                # this value need y=0.25+((-x)/y)*(-x),x=0.25
                Movey(0.3)
                Movex(0.3 + (((-x) / y) * (-x)))
                # print (0.25+(((-x)/y)*(-x)))
                # 20cm -> value  = 50?
                closeball1(17)
                closeball2(topdistance, close1_)
                return runtohitball90(threshold, topdistance, ditance)
            if (x >= 0):
                # theoretics value
                mm = (-0.2 / (math.tan(((3.14159 / 4) - math.atan(x / y)))))
                # print mm
                Movey(mm)
                # Movey(0.15)
                closeball1(17)
                closeball2(topdistance, close1_)
                return runtohitball90(threshold, topdistance, ditance)
        # if not find ball
        else:
            # first consider the best position

            # ***********************
            names = ["HeadPitch", "HeadYaw"]
            angleLists = [0.0 * almath.TO_RAD, 90.0 * almath.TO_RAD]
            timeLists = [1.0, 2.0]
            isAbsolute = True
            motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
            time.sleep(1.0)

            # *****************************


            isfindLand, x, y, z, d = DetecteLandmark()
            if (isfindLand == 1):
                closeball1(17)
                closeball2(topdistance, close1_)
                return runtohitball90(threshold, topdistance, ditance)

            else:
                for i in range(0, 5):
                    # ***********************
                    names = ["HeadPitch", "HeadYaw"]
                    angleLists = [0.0 * almath.TO_RAD, (30.0 + i * 30.0) * almath.TO_RAD]
                    timeLists = [1.0, 2.0]
                    isAbsolute = True
                    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
                    time.sleep(1.0)

                    # *****************************

                    isfindLand, x, y, z, d = DetecteLandmark()
                    # find landmark
                    if (isfindLand == 1):
                        if (i == 0):
                            Movey(0.05)
                            closeball1(17)
                            closeball2(topdistance, close1_)
                            return runtohitball90(threshold, topdistance, ditance)
                        if (i <= 3):
                            return runtohitball90(threshold, topdistance, ditance)
                        if (i == 4):
                            if (x >= 0):
                                return runtohitball90(threshold, topdistance, ditance)
                            else:
                                return runtohitball90_n(threshold, topdistance, ditance)
                        if (i == 5):
                            if (x >= 0):
                                return runtohitball90(threshold, topdistance, ditance)
                            else:
                                return runtohitball90_n(threshold, topdistance, ditance)
                        break

                    else:
                        pass

                # ******************************

                names = ["HeadPitch", "HeadYaw"]
                angleLists = [0.0 * almath.TO_RAD, 0.0 * almath.TO_RAD]
                timeLists = [1.0, 2.0]
                isAbsolute = True
                motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
                time.sleep(1.0)

                # *********************************************
                for i in range(0, 5):

                    # ***********************
                    names = ["HeadPitch", "HeadYaw"]
                    angleLists = [0.0 * almath.TO_RAD, -1 * (30.0 + i * 30.0) * almath.TO_RAD]
                    timeLists = [1.0, 2.0]
                    isAbsolute = True
                    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
                    time.sleep(1.0)

                    # *****************************

                    isfindLand, x, y, z, d = DetecteLandmark()
                    # find landmark
                    # find landmark
                    if (isfindLand == 1):
                        if (i <= 3):
                            Movey(0.9)
                            Movex(0.45)
                            Movet(-math.pi / 1.5)
                            closeball1(17)
                            closeball2(topdistance, close1_)
                            return runtohitball90(threshold, topdistance, ditance)
                        if (i == 4):
                            Movey(1.0)
                            Movex(0.5)
                            Movet(-math.pi / 1.5)
                            closeball1(17)
                            closeball2(topdistance, close1_)
                            return runtohitball90(threshold, topdistance, ditance)

                        if (i == 5):
                            Movey(1.4)
                            Movex(1.2)
                            Movet(-math.pi / 1.5)
                            closeball1(17)
                            closeball2(topdistance, close1_)
                            return runtohitball90(threshold, topdistance, ditance)

                        break

                    else:
                        pass

        Movey(0.4)
        Movex(0.5)
        break


# ***************************************************************************************

# ********************************************************************************** -70~-190
# -60,
def runtohitball90_far(threshold, topdistance, ditance):
    # turn head
    # detecteland
    # Movex(-0.08)
    adj = 0.08
    close1_ = 23
    count = 0
    while (1):
        names = ["HeadPitch", "HeadYaw"]
        angleLists = [0 * almath.TO_RAD, 90.0 * almath.TO_RAD]
        timeLists = [1.0, 2.0]
        isAbsolute = True
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        time.sleep(2.0)

        isfindLand, size, x, ss = DetecteLandmark_my()
        # print x,threshold+ditance,ditance-threshold
        time.sleep(2.0)
        # print  "landmark"
        if (isfindLand == 0):
            count = count + 1
            Movey(0.12)
            redball512_r.lookat(robotIP, PORT)
            closeball1(17)
            closeball2(topdistance, close1_)

        elif (((x - ditance) > threshold) & ((x - ditance) < -threshold)):
            return size, x
        elif ((x - ditance) < threshold):

            Movey(-0.03)
            redball512_r.lookat(robotIP, PORT)
            # *************************************
            closeball1(17)
            closeball2(topdistance, close1_)
        else:
            count = count + 1
            Movey(0.04)
            redball512_r.lookat(robotIP, PORT)
            closeball1(17)
            closeball2(topdistance, close1_)


# **********************************************************************************
# **************************************
#函数功能：第三个场地，走到第二杆的击球位置，准备将球打到正八边形中
#参数：threshold-此参数调整误差大小时间需要的久，太大时间多， topdistance-靠近球的时候球距离机器人球在图像中距离相框头部的距离， ditance-此参数和threshold运算过后确定击球位置
##返回参数：两个，分别为 
#						 1、黄杆在图像中的大小
#						 2、黄杆距机器人的真实距离
#						 
def newruntohitball_far(threshold, topdistance, ditance):
    xx = 0.0
    i = 0
    close1_ = 27
    count = 0
    fivefindlandmark = 0
    while (1):
        names = ["HeadPitch", "HeadYaw"]
        angleLists = [0 * almath.TO_RAD, 90.0 * almath.TO_RAD]
        timeLists = [1.0, 2.0]
        isAbsolute = True
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        time.sleep(2.0)
        isfindLand, size, xx, ss = DetecteLandmark_my()
        print xx, threshold + ditance, ditance - threshold
        # time.sleep(2.0)
        print  "landmark"
        # 90 degre cannot find
        if (isfindLand == 0):
            while (1):
                # ***********************
                names = ["HeadPitch", "HeadYaw"]
                angleLists = [0.0 * almath.TO_RAD, (90.0 - i * 30.0) * almath.TO_RAD]
                timeLists = [1.0, 2.0]
                isAbsolute = True
                motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
                time.sleep(1.0)
                # *****************************
                isfindLand, size, xx, ss = DetecteLandmark_my()
                # find landmark

                if (isfindLand == 1):
                    if (i == 0):
                        t_ = 0.08
                    elif (i == 1):
                        t_ = 0.12
                    elif (i == 2):
                        t_ = 0.16
                    elif (i == 3):
                        t_ = 0.20
                    elif (i == 4):
                        t_ = 0.24
                    elif (i == 5):
                        t_ = 0.30
                    Movey(t_)
                    Movet(-(math.atan(t_ / ditance)))

                    fivefindlandmark = 1
                    i = i + 1
                    i = 0
                    break
                else:
                    i = i + 1
                    pass

                if (i == 6):
                    i = 0
                    break
            if (fivefindlandmark == 0):
                t_ = 0.30
                Movey(t_)
                Movet(-(math.atan(t_ / ditance) + math.pi / 16))
            closeball1(close1_)
            closeball2(topdistance, close1_)



        elif (((xx - ditance) > threshold) & ((xx - ditance) < -threshold)):
            return size, xx
        else:
            count = count + 1
            Movey(0.04)
            redball000.lookat(robotIP, PORT)
            closeball1(close1_)
            closeball2(topdistance, close1_)


# **********************************special for 1   3****
#函数功能：让机器人的正面对准黄的球杆。
#参数：threshold-此参数调整误差大小时间需要的久，太大时间多
#返回参数：两个，分别为 						
#						 1、黄杆在图像中的大小
#						 2、黄杆在图像中距离左边距的像素点
#						 3、黄杆的真实距离
def runtolandmark_face(threshold):
    flag_n = 0
    flag_p = 0
    count = 1
    ##print "s"
    while (1):
        isfindLand, size, left, xx = DetecteLandmark_my()
        # print "my",xx
        if (isfindLand == 0):
            Movet(math.pi / 6)
        else:
            if (left <= threshold) & (left >= -threshold):
                # print "return",size,left,xx
                return size, left, xx

            elif (left > threshold):
                flag_p = 1
                if ((flag_p == 1) & (flag_n == 1)):
                    count = count + 1
                    flag_n = 0
                x = 0.0
                y = 0.0
                theta = -1 * math.pi / (8 * (2 * count))
                motionProxy.moveTo(x, y, theta)
                time.sleep(1.5)

            elif (left < - threshold):
                flag_n = 1
                if ((flag_p == 1) & (flag_n == 1)):
                    count = count + 1
                    flag_p = 0
                x = 0.0
                y = 0.0
                theta = math.pi / (8 * (2 * count))
                motionProxy.moveTo(x, y, theta)
                time.sleep(1.5)


# ***********************************************************************************
#函数功能：让机器人走到距黄杆的threshold内停下
#参数：threshold-此参数为距离阈值
#返回参数：两个，分别为 						
#						 1、黄杆在图像中的大小
#						 2、黄杆在图像中距离左边距的像素点
#						 3、黄杆的真实距离
def runtolandmark13(threshold):
    while (1):
        size, left, x = runtolandmark_face(50)
        if (x <= threshold):
            break
        elif (x >= 3.5):
            Movex(0.45)
        elif (x >= 2.5):
            Movex(0.3)
        elif (x >= 1.5):
            Movex(0.2)


# *******************************************************************************


# **********************************************************************************
# 说明:此函数是runtohitball_far的子函数，旧版本的，已经被抛弃了
def far_ball():
    close1_ = 23
    topdistance = 30
    Ldistance = 30
    threshold = 20
    while (1):
        isfindLand, size, x, ss = DetecteLandmark_my()
        if (isfindLand == 0):
            count = count + 1
            Movey(0.06)
            redball000.lookat(robotIP, PORT)
        elif (((x - Ldistance) < threshold) & ((x - Ldistance) > -threshold)):
            return size
        elif (x - Ldistance < -threshold):
            Movey(-0.02)
            closeball1(17)
            closeball2(topdistance, close1_)
#说明:与newruntohitball_far的功能一样，这个是旧版本的，已经被抛弃了
def runtohitball_far(topdistance):
    # ***********************
    close1_ = 23
    closeball1(17)
    # **************
    closeball2(30, close1_)  # 55

    names = ["HeadPitch", "HeadYaw"]
    angleLists = [0.0 * almath.TO_RAD, 0.0 * almath.TO_RAD]
    timeLists = [1.0, 2.0]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(1.0)

    # *****************************
    while (1):
        isfindLand, size, x, ss = DetecteLandmark_my()
        # find landmark
        if (isfindLand == 1):
            if (x < 0):
                # this value need y=0.25+((-x)/y)*(-x),x=0.25
                # ***********************************
                names = ["HeadPitch", "HeadYaw"]
                angleLists = [0.0 * almath.TO_RAD, 90.0 * almath.TO_RAD]
                timeLists = [1.0, 2.0]
                isAbsolute = True
                motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
                time.sleep(1.0)
                far_ball()
                # **************************************
                return size
            if (x >= 0):
                # ***************
                names = ["HeadPitch", "HeadYaw"]
                angleLists = [0.0 * almath.TO_RAD, 90.0 * almath.TO_RAD]
                timeLists = [1.0, 2.0]
                isAbsolute = True
                motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
                time.sleep(1.0)
                far_ball()
                # ********************
                return size
        # if not find ball
        else:
            # first consider the best position
            # ***********************


            # *****************************
            names = ["HeadPitch", "HeadYaw"]
            angleLists = [0.0 * almath.TO_RAD, 90.0 * almath.TO_RAD]
            timeLists = [1.0, 2.0]
            isAbsolute = True
            motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
            time.sleep(1.0)
            return far_ball()

        break

#第一个场地的，封装函数
def first(robotIP, PORT):
    # StandToGetstick()
	#击球
    HitBall(0.43)
	#从站立状态到蹲下。缓冲
    Movex(0.01)  
    time.sleep(1.0)
	#转九十度，开始找球
    Movet(math.pi / 2)
    Movex(0.9)
	#while（1）循环在八边形里面找球击球
    while (1):
        # Movet(math.pi/2.8)
        # run to ball
        closeball1(23)
        # #**************
        closeball2(30, 23)
        # run to hit ball position   wtih 0


        x0, y0, z0, dis = newruntohitball(0.10, 30, 0.22)

        # Movex(-0.02)

        # closeball2(58, 25)
        # choose power depending on the distant
        if (dis < 1.0):

            HitBall(0.42)

        elif (dis <= 1.2):
            HitBall(0.41)
        elif (dis >= 1.2):
            HitBall(0.40)

#第二个场地的，封装函数
def second(robotIP, PORT):
    # hitball  max=0.27
    # StandToGetstick()
    # ******************************************
	#击球
    HitBall(0.42)  
	#从站立状态到蹲下。缓冲
    Movex(0.01)  # xxxxxxxxxxxxxxxxxxxxxxxxxxx
    time.sleep(1.0)
    Movet(math.pi / 2)  # 2eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeexxxxxxxxxxxxxxxx
    #向前走一段
	Movex(0.4)
    #正面对准landmark
	runtolandmark_face(70)
	#走到距离landmark2.9米处
    runtolandmark13(2.9)
	#开始避障
    Movey(-0.9)
    Movex(1.0)
	#照样对准landmark
    runtolandmark_face(50)
	#在1.6米处停下，此时已经走到正八边形
    runtolandmark13(1.6)
    # ******************************************

	#循环找球
    while (1):
        # Movet(math.pi/2.8)
        # run to ball
        closeball1(23)
        # #**************
        closeball2(30, 23)
        # run to hit ball position   wtih 0


        x0, y0, z0, dis = newruntohitball(0.10, 30, 0.22)


        # closeball2(58, 25)
        # choose power depending on the distant
        if (dis < 1.0):

            HitBall(0.42)

        elif (dis <= 1.2):
            HitBall(0.41)
        elif (dis >= 1.2):
            HitBall(0.40)

#第三个场地的，封装函数
def third(robotIP, PORT):
    #     #******************************************3******************************************
   
	#击球
    HitBall(0.8)  
	#从站立状态到蹲下。缓冲
    Movex(0.01)  
    time.sleep(1.0)
	#转身
    Movet(math.pi / 1.9)  
    #向前走一段距离
    Movex(0.5)  # cancel 
	#开始找球 并且击球
    closeball1(23)  # 
    closeball2(30, 23)  # 
    newruntohitball_far(-85, 30, -115)  # 30eeeeeeeeeeeeeeeeeeeeeeeeee
    HitBall(0.41)
	#对准黄杆并且走到正八边形里面去
    runtolandmark_face(70)
    runtolandmark13(1.8)
    # #print "SS",x
  
  
	#循环找球
    while (1):
        # Movet(math.pi/2.8)
        # run to ball
        closeball1(23)
        # #**************
        closeball2(30, 23)
        # run to hit ball position   wtih 0


        x0, y0, z0, dis = newruntohitball(0.10, 30, 0.22)

        # closeball2(58, 25)
        # choose power depending on the distant
        if (dis < 1.0):

            HitBall(0.42)

        elif (dis <= 1.2):
            HitBall(0.41)
        elif (dis >= 1.2):
            HitBall(0.40)






