# -*- coding: utf-8 -*-
import sys
from threading import Thread
from time import sleep

from naoqi import ALProxy

from scapy.all import srp, Ether, ARP, conf

# IP = ['192.168.0.3', '192.168.0.7', '192.168.0.5', '192.168.0.6', '192.168.0.2', '192.168.0.9',
#       '192.168.0.8', '192.168.0.10', '192.168.0.4']

# danceName = "thriller-dance"  # 舞蹈ID  #thriller-dance   little-apple-dance
danceName = "untitled11-be9b28"               #untitled-0f0269   WXYwxy1528154605.. untitled11-be9b28   .lastUploadedChoregrapheBehavior
#untitled-4aac89

# 新机器人与旧机器人之间启动时间间隔timeLater
timeLater = 0

#新机器人数量
# ，少于这个数量程序不执行
robotsNum = 2

#旧机器人数量，少于这个数量程序不执行
oldRobotsNum = 2
"bc:30:7d:f5:d6:f7"  "28:24:ff:82:54:d4" "28:24:ff:82:55:31"
# 机器人所在局域网的 网段
lan = '192.168.0.1/24'      #lan = '192.168.43.1/24'

# mac_list = ["28:24:ff:4d:3e:5b", "28:24:ff:82:54:d4", "28:24:ff:4c:e1:45",
#             "28:24:ff:4d:41:bf","28:24:ff:4d:16:03","28:24:ff:82:55:31",
#             "48:a9:d2:96:98:b9","bc:30:7d:f5:d6:f7","28:24:ff:4d:19:3b","28:24:ff:4d:3f:e5"]  # 机器人mac地址
danceThread = ['192.168.0.3', '192.168.0.7', '192.168.0.5', '192.168.0.6', '192.168.0.2', '192.168.0.9',
    '192.168.0.8', '192.168.0.10', '192.168.0.4']
stopDanceThread = ['192.168.0.3', '192.168.0.7', '192.168.0.5', '192.168.0.6', '192.168.0.2', '192.168.0.9',
    '192.168.0.8', '192.168.0.10', '192.168.0.4'],
standThread = ['192.168.0.3', '192.168.0.7', '192.168.0.5', '192.168.0.6', '192.168.0.2', '192.168.0.9',
    '192.168.0.8', '192.168.0.10', '192.168.0.4']
sitThread = ['192.168.0.3', '192.168.0.7', '192.168.0.5', '192.168.0.6', '192.168.0.2', '192.168.0.9',
    '192.168.0.8', '192.168.0.10', '192.168.0.4']

class Dance(Thread):
    def __init__(self, ip):
        Thread.__init__(self)
        self.ip = ip
        self.danceBehaviorManager = ALProxy("ALBehaviorManager", self.ip, 9559)

    def run(self):
        self.danceBehaviorManager.startBehavior(danceName)
        print(self.ip)


class StopDance(Thread):
    def __init__(self, ip):
        Thread.__init__(self)
        self.ip = ip
        self.stopDanceBehaviorManager = ALProxy("ALBehaviorManager", self.ip, 9559)

    def run(self):
        self.stopDanceBehaviorManager.stopBehavior(danceName)


class Stand(Thread):
    def __init__(self, ip):
        Thread.__init__(self)
        self.ip = ip
        self.postureService = ALProxy("ALRobotPosture", self.ip, 9559)

    def run(self):
        self.postureService.goToPosture('Stand', 0.5)


class Sit(Thread):
    def __init__(self, ip):
        Thread.__init__(self)
        self.ip = ip
        self.motion = ALProxy("ALMotion", self.ip, 9559)

    def run(self):
        self.motion.rest()


if __name__ == '__main__':                              #主函数
        if (len(sys.argv) == 2):
            if (sys.argv[1] == 'dance'):
                print("start dance!")
                # 将跳舞的进程存到数组里  先存新机器人  后存旧机器人
                for k in range(0,8):                       #新旧机器人数量总和
                    # if (k == len(ipList)):
                        # 新机器人与就机器人之间时间间隔timelate
                        # sleep(timeLater)
                    danceThread[k].start()
            elif (sys.argv[1] == 'stop'):
                print("stop dance!")
                for k in range(0,8):
                    stopDanceThread[k].start()
            elif (sys.argv[1] == 'stand'):
                print("Stand up")
                for k in range(0,8):
                    standThread[k].start()
            elif (sys.argv[1] == 'sit'):
                print("Sit")
                for k in range(0,8):
                    sitThread[k].start()


