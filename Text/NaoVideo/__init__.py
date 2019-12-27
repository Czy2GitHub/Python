# coding:utf-8
from naoqi import ALProxy
import time
import vision_definitions
IP = "192.168.31.120"
PORT = 9559
videoRecorderProxy = ALProxy("ALVideoRecorder", IP, PORT)
videoRecorderProxy.setResolution(1)
videoRecorderProxy.setFrameRate(10)
videoRecorderProxy.setVideoFormat("MJPG")
Camera = ALProxy("ALVideoDevice", IP, PORT)
Camera.recordVideo("/home/nao/recordings/cameras", "myvideo")
videoInfo = videoRecorderProxy.stopVideoRecord()
# 播放视频
resolution = vision_definitions.kVGA
colorSpace = vision_definitions.kBGRColorSpace
fps = 20
nameId = "video"
camProxy = ALProxy("ALVideoDevice", IP, PORT)
nameId = camProxy.subscribe(nameId, resolution, colorSpace, fps)
recording = camProxy.recordVideo(nameId, "/home/nao/naoqi/001_VGA", 3500, 1)
for i in range(0, 500):
    image = camProxy.getImageLocal(nameId)
    camProxy.releaseImage(nameId)
    time.sleep(0.003)
camProxy.stopVideo(nameId)
camProxy.unsubscribe(nameId)
