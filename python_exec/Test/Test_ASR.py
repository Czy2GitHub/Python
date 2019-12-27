# -*- coding:utf-8 -*-
import time
from naoqi import ALProxy

robotIP = "192.168.31.120"  # 获取本地ip地址
asr = ALProxy("ALSpeechRecognition", robotIP, 9559)
memProxy = ALProxy("ALMemory", robotIP, 9559)

asr.setLanguage("Chinese")                          # 设置语言
vocabulary = ['1', '2', '3']                # 设置关键字
asr.setVocabulary(vocabulary, True)                 # 设置语音引擎识别的发现列表，为False发现一个，为True发现多个
asr.subscribe("Test_ASR")                           # 向服务器提交
print 'Speech recognition engine started'
time.sleep(10)                                      # 十秒内进行语音输入
try:
    val = memProxy.getData("WordRecognized")        # 创建列表接受记忆模块得到的语音流
    print(val)                                      # 打印
except:
    print("error")
asr.unsubscribe("Test_ASR")                         # 结束提交
