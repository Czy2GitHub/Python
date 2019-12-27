# -*- coding:utf-8 -*-

from naoqi import ALProxy

robotIP = "192.168.31.206"
tts = ALProxy("ALTextToSpeech", robotIP, 9559)
tts.say("Hello")
