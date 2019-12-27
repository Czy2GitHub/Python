# coding:utf-8
import numpy as np
from naoqi import ALProxy
motionProxy = ALProxy("ALMotion", "192.168.31.32", 9559)
bottomCameraDirection = {"standInit": 49.2 / 180 * np.pi, "standUp": 39.7 / 180 * np.pi} # 字典，储存两个角度
cameraPitchRange = 47.64/180*np.pi
cameraYawRange = 60.97/180*np.pi
ballRadius = 0.05
def redBallLocation(standState, frameArray, ballData):
    """
    compute and update the ball position with the ball data in frame.
    standState: "standInit" or "standUp".
    """
    frameWidth = frameArray[0]
    frameHeight = frameArray[1]
    ballDict = {"centerX":0, "centerY":0, "radius":0}      # 图像坐标字典
    ballDict["centerX"] = ballData[0]
    ballDict["centerY"] = ballData[1]
    ballDict["radius"] = ballData[2]
    ballPosition = {"disX": 0, "disY": 0, "angle": 0}      # 实际坐标字典
    bottomCameraDirection = {"standInit": 49.2 / 180 * np.pi, "standUp": 39.7 / 180 * np.pi}
    try:
        cameraDirection = bottomCameraDirection[standState]
    except KeyError:
        print("Error! unknown standState, please check the value of stand state!")
        raise
    else:
        if ballDict["radius"] == 0:
            ballPosition = {"disX": 0, "disY": 0, "angle": 0}
        else:
            centerX = ballDict["centerX"]
            centerY = ballDict["centerY"]
            radius = ballDict["radius"]
            # self._cameraName
            cameraPos = motionProxy.getPosition(0, motionProxy.FRAME_WORLD, True)
            cameraX, cameraY, cameraHeight = cameraPos[:3]
            head_yaw, head_pitch = motionProxy.getAngles("Head", True)
            camera_pitch = head_pitch + cameraDirection
            img_center_x = frameWidth / 2
            img_center_y = frameHeight / 2
            center_x = ballDict["centerX"]
            center_y = ballDict["centerY"]
            img_pitch = (center_y - img_center_y) / (frameHeight) * cameraPitchRange
            img_yaw = (img_center_x - center_x) / (frameWidth) * cameraYawRange

            ball_pitch = camera_pitch + img_pitch
            ball_yaw = img_yaw + head_yaw
            print("ball yaw = ", ball_yaw / np.pi * 180)
            dis_x = (cameraHeight - ballRadius) / np.tan(ball_pitch) + np.sqrt(cameraX ** 2 + cameraY ** 2)
            dis_y = dis_x * np.sin(ball_yaw)
            dis_x = dis_x * np.cos(ball_yaw)
            ballPosition["disX"] = dis_x
            ballPosition["disY"] = dis_y
            ballPosition["angle"] = ball_yaw
    return ballPosition