# coding:utf-8
from naoqi import ALProxy

# ConfigureNao类为所有类的父类，定义了大部分的模块对象
class ConfigureNao(object):
    """
    a basic class for all nao tasks, including motion, bisualization etc.
    """
    def __init__(self, IP):
        self._IP = IP                       # IP 需要我们传参数
        self._PORT = 9559                   # 端口号
        self._cameraProxy = ALProxy("ALVideoDevice", self._IP, self._PORT)      # 调用摄像模块
        self._motionProxy = ALProxy("ALMotion", self._IP, self._PORT)           # 调用行动模块
        self._postureProxy = ALProxy("ALRobotPosture", self._IP, self._PORT)    # 调用机器人姿势库
        self._tts = ALProxy("ALTextToSpeech",self._IP, self._PORT)              # 说话模块
        self._memoryProxy = ALProxy("ALMemory", self._IP, self._PORT)           # 记忆模块