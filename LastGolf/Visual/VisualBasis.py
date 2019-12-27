# coding:utf-8
# 视觉基本类
from configureNao import ConfigureNao
import vision_definitions as vd
import cv2
import numpy as np
class VisualBasis(ConfigureNao):
    """
    a basic class for visual task.
    """
    def __init__(self, IP, cameraId):
        """
        initilization.
        Args:
            IP: NAO's IP
            cameraId: bottom camera (1,default) or top camera (0).
            resolution: kVGA, default: 640*480)
        Return: none
        """
        super(VisualBasis, self).__init__(IP)
        self._cameraId = cameraId
        self._resolution = vd.kVGA

        self._colorSpace = vd.kBGRColorSpace
        self._fps = 20

        self._frameHeight = 0
        self._frameWidth = 0
        self._frameChannels = 0
        self._frameArray = None

        self._cameraPitchRange = 47.64/180*np.pi
        self._cameraYawRange = 60.97/180*np.pi
        self._cameraProxy.setActiveCamera(self._cameraId)


    def updateFrame(self, client="python_client"):
        """
        get a new image from the specified camera and save it in self._frame.
        Args:
            client: client name.
        Return: none.
        """

        """
        if self._cameraProxy.getActiveCamera() == self._cameraId:
            print("current camera has been actived.")
        else:
            self._cameraProxy.setActiveCamera(self._cameraId)
        """
        self._videoClient = self._cameraProxy.subscribe(client, self._resolution, self._colorSpace, self._fps)
        frame = self._cameraProxy.getImageRemote(self._videoClient)
        self._cameraProxy.unsubscribe(self._videoClient)

        try:
            self._frameWidth = frame[0]
            self._frameHeight = frame[1]
            self._frameChannels = frame[2]
            self._frameArray = np.frombuffer(frame[6], dtype=np.uint8).reshape([frame[1],frame[0],frame[2]])
        except IndexError:
            raise

    def getFrameArray(self):
        """
        get current frame.
        Return:
            current frame array (numpy array).
        """
        if self._frameArray is None:
            return np.array([])
        return self._frameArray

    def showFrame(self):
        """
        show current frame image.
        """

        if self._frameArray is None:
            print("please get an image from Nao with the method updateFrame()")
        else:
            cv2.imshow("current frame", self._frameArray)

    def printFrameData(self):
        """
        print current frame data.
        """
        print("frame height = ", self._frameHeight)
        print("frame width = ", self._frameWidth)
        print("frame channels = ", self._frameChannels)
        print("frame shape = ", self._frameArray.shape)

    def saveFrame(self, framePath):
        """
        save current frame to specified direction.
        Arguments:
            framePath: image path.
        """

        cv2.imwrite(framePath, self._frameArray)
        print("current frame image has been saved in", framePath)

    def setParam(self, paramName=None, paramValue = None):
        raise NotImplementedError

    def setAllParamsToDefault(self):
        raise NotImplementedError
