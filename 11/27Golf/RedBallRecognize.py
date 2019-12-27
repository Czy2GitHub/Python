# coding:utf-8

# 红球识别逻辑部分
from configureNao import *
def recognizeBall():
    # 使用摄像头获取图像
    cameraProxy.setActiveCamera(1)
    video = cameraProxy.subscribe("Take_photo", resulation=vision_definitions.kVGA, colorSpace=vision_definitions.kBGRColorSpace, fps=5)
