# coding:utf-8

from naoqi import ALProxy
import numpy as np
import cv2
import vision_definitions
import math
# nao机器人视觉基础类
class VisionBasic(object):
    def __init__(self):
        # 端口号 相机代理
        self.port = 9559  # crf 机器人端口
        self.robot_ip = "192.168.31.132"  # crf 机器人IP
        self.CameraProxy = ALProxy("ALVideoDevice", self.robot_ip, self.port)

        # 基本参数
        self.resolution = vision_definitions.kVGA
        self.colorSpace = vision_definitions.kBGRColorSpace
        self.fps = 30
        self.frameHeight = 0            # 图像的高度
        self.frameWidth = 0             # 图像的宽度
        self.frameChannels = 0          # 图像的RGB通道
        self.frameArray = None          # 用于显现图像的数组
        self.cameraPitchRange = 47.64 / 180 * math.pi   # 展示范围
        self.cameraYawRange = 60.97 / 180 * math.pi     # 偏角范围

    # 获取图片
    def getImage(self):
        self.CameraProxy.setActiveCamera(1)
        videoClient = self.CameraProxy.subscribe("python_GVM", self.resolution, self.colorSpace, self.fps)
        self.frame = self.CameraProxy.getImageRemote(videoClient)
        self.CameraProxy.unsubscribe(videoClient)
    # 读取图片
    def readImage(self):
        self.frameWidth = self.frame[0]
        self.frameHeight = self.frame[1]
        self.frameChannels = self.frame[2]
        self.frameArray = np.frombuffer(self.frame[6], dtype=np.uint8).reshape([self.frameHeight, self.frameWidth, self.frameChannels])
        return self.frameArray
    # 显示图片
    def showImage(self, image):
        cv2.imshow("result", image)
        cv2.waitKey(30)
        # cv2.destroyAllWindows()
    # 对图像进行平滑处理
    def smooth(self):
        gray = cv2.cvtColor(self.frameArray, cv2.COLOR_BGR2GRAY) # 转换为BGR图像
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)             # 霍夫降噪 平滑处理
        self.thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]   # 取得二值图
        cv2.imshow("smooth", self.thresh)
        return self.thresh