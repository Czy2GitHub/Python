# -*- coding:utf-8 -*-
import cv2
from naoqi import ALProxy

robot_IP = "192.168.31.206"
# tts = ALProxy("ALTextToSpeech", robot_IP, 9559)
# tts.say("Hello!")
# motion = ALProxy("ALMotion", robot_IP, 9559)
# motion.moveInit()
# motion.moveTo(0.1, 0, 0)
view = ALProxy("ALVideoDevice", robot_IP, 9559)
view.openCamera(0)
view.startCamera(0)
view.stopCamera(0)
cv2.V
# while 1:
#     frame = cap.read()
#     cv2.imshow("capture", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

