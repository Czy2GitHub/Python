# -*- coding: utf-8 -*-
import sys
from threading import Thread
from time import sleep

from naoqi import ALProxy

from scapy.all import srp, Ether, ARP, conf

# IP = ['192.168.0.10', '192.168.0.2', '192.168.0.25', '192.168.0.11', '192.168.0.16', '192.168.0.6', '192.168.0.12',
#       '192.168.0.8', '192.168.0.4', '192.168.0.14']

# danceName = "thriller-dance"  # 舞蹈ID  #thriller-dance   little-apple-dance
danceName = "zhuanjia-a519e2"               #untitled-0f0269   WXYwxy1528154605.. untitled11-be9b28   .lastUploadedChoregrapheBehavior
#untitled-4aac89

# 新机器人与旧机器人之间启动时间间隔timeLater
timeLater = 0

#新机器人数量
# ，少于这个数量程序不执行
robotsNum = 6

#旧机器人数量，少于这个数量程序不执行
oldRobotsNum = 0

# 机器人所在局域网的 网段
lan = '192.168.31.1/24'      #lan = '192.168.43.1/24'

# mac_list = ["28:24:ff:4d:3e:5b", "28:24:ff:82:54:d4", "28:24:ff:4c:e1:45",#   格    世
#             "28:24:ff:4d:41:bf","28:24:ff:4d:16:03","28:24:ff:82:55:31",
#             "48:a9:d2:96:98:b9","bc:30:7d:f5:d6:f7","28:24:ff:4d:19:3b","28:24:ff:4d:3f:e5"]  # 机器人mac地址
macList = ["28:24:ff:4d:16:03", "28:24:ff:4d:19:3b", "28:24:ff:4d:3e:5b", "28:24:ff:4d:3f:e5",
           "28:24:ff:4c:e1:45", "28:24:ff:4d:41:bf"]#
macListOld = ["28:24:ff:82:55:31", "48:a9:d2:96:98:b9", "bc:30:7d:f5:d6:f7",
              "28:24:ff:82:54:d4"]
ipList = []
ipListOld = []
danceThread = []
stopDanceThread = []
standThread = []
sitThread = []
vocThread = []
ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=lan), timeout=5)

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


class Volume(Thread):
    def __init__(self, ip, voice):
        Thread.__init__(self)
        self.ip = ip
        # self.voice = 50
        self.voice = int(voice)
        self.motion = ALProxy("ALAudioDevice", self.ip, 9559)

    def run(self):
        try:
            self.motion.setOutputVolume(self.voice)
        except:
            print(self.ip + "超时")


if __name__ == '__main__':                              #主函数
    for snd, rcv in ans:
        cur_mac = rcv.sprintf("%Ether.src%")
        cur_ip = rcv.sprintf("%ARP.psrc%")

        for mac in macListOld:
            if (cur_mac == mac):
                ipListOld.append(cur_ip)
                print cur_mac + ' - ' + cur_ip

        for mac in macList:
            if (cur_mac == mac):
                ipList.append(cur_ip)
                print cur_mac + ' - ' + cur_ip

    for ip in ipListOld, ipList:
        print(ip)

    for ip in ipList:
        print(ip)
    print(len(ipList))
    print(len(ipListOld))
    if (len(ipList) == robotsNum and len(ipListOld) == oldRobotsNum):       #判断机器人数量
        print("the number of nao is ok!")
        if (len(sys.argv) == 2):
            if (sys.argv[1] == 'dance'):
                j = len(ipList) + len(ipListOld)
                print("start dance!")
                # 将跳舞的进程存到数组里  先存新机器人  后存旧机器人
                for i in ipList:                            #i = ip
                    danceThread.append(Dance(i))
                for i in ipListOld:
                    danceThread.append(Dance(i))

                for k in range(0, j):                       #新旧机器人数量总和
                    # if (k == len(ipList)):
                        # 新机器人与就机器人之间时间间隔timelate
                        # sleep(timeLater)
                    danceThread[k].start()

            elif (sys.argv[1] == 'stop'):
                j = len(ipList) + len(ipListOld)
                print("stop dance!")

                for i in ipList:
                    stopDanceThread.append(StopDance(i))
                for i in ipListOld:
                    stopDanceThread.append(StopDance(i))
                for k in range(0, j):
                    stopDanceThread[k].start()

            elif (sys.argv[1] == 'stand'):
                j = len(ipList) + len(ipListOld)
                print("Stand up")
                for i in ipList:
                    standThread.append(Stand(i))
                for i in ipListOld:
                    standThread.append(Stand(i))
                for k in range(0, j):
                    standThread[k].start()

            elif (sys.argv[1] == 'sit'):
                j = 0
                print("Sit")
                for i in ipList:
                    sitThread.append(Sit(i))
                    j = j + 1
                    print(i)
                for i in ipListOld:
                    sitThread.append(Sit(i))
                    j = j + 1
                    print(i)
                for k in range(0, j):
                    sitThread[k].start()

        elif (len(sys.argv) == 3):
            if (sys.argv[1] == 'voice'):

                voc = sys.argv[2]
                j = 0
                print("changeVoice")

                for i in ipListOld:
                    vocThread.append(Volume(i, voc))
                    j = j + 1
                for i in ipList:
                    vocThread.append(Volume(i, voc))
                    j = j + 1

                for i in ipList:
                    j = j - 1
                    vocThread[j].start()
                sleep(timeLater)
                for i in ipListOld:
                    j = j - 1
                    vocThread[j].start()

        else:
            print("Error in number of argv!")
    else:
        print("too few nao!")
    print len(ipList) + len(ipListOld)
