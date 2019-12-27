# coding:utf-8
from VisualBasis import VisualBasis
import vision_definitions as vd
import cv2
import numpy as np
class Ball_Detect(VisualBasis):
    def __init__(self, IP, cameraId=vd.kBottomCamera, resolution=vd.kVGA):
        """
        initialization.
        """
        super(Ball_Detect, self).__init__(IP, cameraId)
        self._ballData = {"centerX": 0, "centerY": 0, "radius": 0}
        self._ballPosition = {"disX": 0, "disY": 0, "angle": 0}
        self._ballRadius = 0.05

    # 图形预处理函数
    def _preprocess(self, minHSV, maxHSV, cropKeep, morphology):
        """
        preprocess the current frame for stick detection.(binalization, crop etc.)
        Arguments:
            minHSV: the lower limit for binalization.  黄色的HSV阈值
            maxHSV: the upper limit for binalization.
            cropKeep: crop ratio (>=0.5).
            morphology: erosion and dilation.腐蚀和膨胀
        Return:
            preprocessed image for stick detection.
        """
        self._cropKeep = cropKeep
        frameArray = self._frameArray
        height = self._frameHeight
        width = self._frameWidth
        try:
            frameArray = frameArray[int((1 - cropKeep) * height):, :]
        except IndexError:
            raise
        frameHSV = cv2.cvtColor(frameArray, cv2.COLOR_BGR2HSV)
        frameBin = cv2.inRange(frameHSV, minHSV, maxHSV)

        kernelErosion = np.ones((5, 5), np.uint8)  # 腐蚀
        kernelDilation = np.ones((5, 5), np.uint8)  # 膨胀
        frameBin = cv2.erode(frameBin, kernelErosion, iterations=1)  # 腐蚀图二值化
        frameBin = cv2.dilate(frameBin, kernelDilation, iterations=1)  # 膨胀二值化
        frameBin = cv2.GaussianBlur(frameBin, (9, 9), 0)  # 高斯滤波
        return frameBin

    # 霍夫圆检测寻找形状
    def _findCircles(self, img, minDist, minRadius, maxRadius):
        """
        detect circles from an image.
        Arguments:
            img: image to be detected.
            minDist: minimum distance between the centers of the detected circles.
            minRadius: minimum circle radius.
            maxRadius: maximum circle radius.
        Return: an uint16 numpy array shaped circleNum*3 if circleNum>0, ([[circleX, circleY,radius]])
                else return None.
        """
        # 霍夫圆检测返回的是 圆心坐标和半径长度
        circles = cv2.HoughCircles(np.uint8(img), cv2.HOUGH_GRADIENT, 1, minDist,
                                   param1=150, param2=15, minRadius=minRadius, maxRadius=maxRadius)

        if circles is None:
            return np.uint16([])
        else:
            return np.uint16(np.around(circles[0]))

    def _updateBallPosition(self, standState):
        """
        compute and update the ball position with the ball data in frame.
        standState: "standInit" or "standUp".
        """

        bottomCameraDirection = {"standInit": 49.2 / 180 * np.pi, "standUp": 39.7 / 180 * np.pi}
        try:
            cameraDirection = bottomCameraDirection[standState]
        except KeyError:
            print("Error! unknown standState, please check the value of stand state!")
            raise
        else:
            if self._ballData["radius"] == 0:
                self._ballPosition = {"disX": 0, "disY": 0, "angle": 0}
            else:
                centerX = self._ballData["centerX"]
                centerY = self._ballData["centerY"]
                radius = self._ballData["radius"]
                # self._cameraName
                cameraPos = self._motionProxy.getPosition(0, self._motionProxy.FRAME_WORLD, True)
                cameraX, cameraY, cameraHeight = cameraPos[:3]
                head_yaw, head_pitch = self._motionProxy.getAngles("Head", True)
                camera_pitch = head_pitch + cameraDirection
                img_center_x = self._frameWidth / 2
                img_center_y = self._frameHeight / 2
                center_x = self._ballData["centerX"]
                center_y = self._ballData["centerY"]
                img_pitch = (center_y - img_center_y) / (self._frameHeight) * self._cameraPitchRange
                img_yaw = (img_center_x - center_x) / (self._frameWidth) * self._cameraYawRange

                ball_pitch = camera_pitch + img_pitch
                ball_yaw = img_yaw + head_yaw
                print("ball yaw = ", ball_yaw / np.pi * 180)
                dis_x = (cameraHeight - self._ballRadius) / np.tan(ball_pitch) + np.sqrt(cameraX ** 2 + cameraY ** 2)
                dis_y = dis_x * np.sin(ball_yaw)
                dis_x = dis_x * np.cos(ball_yaw)
                self._ballPosition["disX"] = dis_x
                self._ballPosition["disY"] = dis_y
                self._ballPosition["angle"] = ball_yaw

    # 红球定位2.0
    def _updateBallPositionFitting(self, standState):
        """
        compute and update the ball position with compensation.
        Args:
            standState: "standInit" or "standUp".
        """
        bottomCameraDirection = {"standInit": 49.2, "standUp": 39.7}
        ballRadius = self._ballRadius
        try:
            cameraDirection = bottomCameraDirection[standState]
        except KeyError:
            print("Error! unknown standState, please check the value of stand state!")
            raise
        else:
            if self._ballData["radius"] == 0:
                self._ballPosition = {"disX": 0, "disY": 0, "angle": 0}
            else:
                centerX = self._ballData["centerX"]
                centerY = self._ballData["centerY"]
                radius = self._ballData["radius"]
                cameraPosition = self._motionProxy.getPosition("CameraBottom", 2, True)
                cameraX = cameraPosition[0]
                cameraY = cameraPosition[1]
                cameraHeight = cameraPosition[2]
                headPitches = self._motionProxy.getAngles("HeadPitch", True)
                headPitch = headPitches[0]
                headYaws = self._motionProxy.getAngles("HeadYaw", True)
                headYaw = headYaws[0]
                ballPitch = (centerY - 240.0) * self._cameraPitchRange / 480.0  # y (pitch angle)
                ballYaw = (320.0 - centerX) * self._cameraYawRange / 640.0  # x (yaw angle)
                dPitch = (cameraHeight - ballRadius) / np.tan(cameraDirection / 180 * np.pi + headPitch + ballPitch)
                dYaw = dPitch / np.cos(ballYaw)
                ballX = dYaw * np.cos(ballYaw + headYaw) + cameraX
                ballY = dYaw * np.sin(ballYaw + headYaw) + cameraY
                ballYaw = np.arctan2(ballY, ballX)
                self._ballPosition["disX"] = ballX

                # 误差补偿（多项式）
                if (standState == "standInit"):
                    ky = 42.513 * ballX ** 4 - 109.66 * ballX ** 3 + 104.2 * ballX ** 2 - 44.218 * ballX + 8.5526
                    # ky = 12.604*ballX**4 - 37.962*ballX**3 + 43.163*ballX**2 - 22.688*ballX + 6.0526
                    ballY = ky * ballY
                    ballYaw = np.arctan2(ballY, ballX)
                self._ballPosition["disY"] = ballY
                self._ballPosition["angle"] = ballYaw

    def _getChannelAndBlur(self, color):
        """
        get the specified channel and blur the result.

        Arguments:
            color: the color channel to split, only supports the color of red, geen and blue.
        Return:
            the specified color channel or None (when the color is not supported).
        """
        try:
            channelB = self._frameArray[:, :, 0]
            channelG = self._frameArray[:, :, 1]
            channelR = self._frameArray[:, :, 2]
        except:
            raise Exception("no image detected!")

        Hm = 6
        if color == "red":
            channelB = channelB * 0.1 * Hm
            channelG = channelG * 0.1 * Hm
            channelR = channelR - channelB - channelG
            channelR = 3 * channelR
            channelR = cv2.GaussianBlur(channelR, (9, 9), 1.5)
            channelR[channelR < 0] = 0
            channelR[channelR > 255] = 255
            return np.uint8(np.round(channelR))

        elif color == "blue":
            channelR = channelR * 0.1 * Hm
            channelG = channelG * 0.1 * Hm
            channelB = channelB - channelG - channelR
            channelB = 3 * channelB
            channelB = cv2.GaussianBlur(channelB, (9, 9), 1.5)
            channelB[channelB < 0] = 0
            channelB[channelB > 255] = 255
            return np.uint8(np.round(channelB))

        elif color == "green":
            channelB = channelB * 0.1 * Hm
            channelR = channelR * 0.1 * Hm
            channelG = channelG - channelB - channelR
            channelG = 3 * channelG
            channelG = cv2.GaussianBlur(channelG, (9, 9), 1.5)
            channelG[channelG < 0] = 0
            channelG[channelG > 255] = 255
            return np.uint8(np.round(channelG))

        else:
            print("can not recognize the color!")
            print("supported color:red, green and blue.")
            return None

    def _binImageHSV(self, color):
        """
        get binary image from the HSV image (transformed from BGR image)
        Args:
            color: the color for binarization.
        Return:
            binImage: binary image.
        """
        try:
            frameArray = self._frameArray.copy()
            imgHSV = cv2.cvtColor(frameArray, cv2.COLOR_BGR2HSV)
        except:
            raise Exception("no image detected!")

        if color == "red":
            minHSV1 = np.array([0, 43, 46])
            maxHSV1 = np.array([10, 255, 255])
            minHSV2 = np.array([156, 43, 46])
            maxHSV2 = np.array([180, 255, 255])
            frameBin1 = cv2.inRange(imgHSV, minHSV1, maxHSV1)
            frameBin2 = cv2.inRange(imgHSV, minHSV2, maxHSV2)
            frameBin = np.maximum(frameBin1, frameBin2)
            return frameBin
        else:
            raise Exception("not recognize the color!")

    def _selectCircle(self, circles):
        """
        select one circle in list type from all circles detected.
        Args:
            circles: numpy array shaped (N, 3),　N is the number of circles.
        Return:
            selected circle or None (no circle is selected).
        """

        if len(circles) == 0:
            return circles

        if circles.shape[0] == 1:
            centerX = circles[0][0]
            centerY = circles[0][1]
            radius = circles[0][2]
            initX = centerX - 2 * radius
            initY = centerY - 2 * radius
            if initX < 0 or initY < 0 or (initX + 4 * radius) > self._frameWidth or (
                    initY + 4 * radius) > self._frameHeight or radius < 1:
                return circles

        channelB = self._frameArray[:, :, 0]
        channelG = self._frameArray[:, :, 1]
        channelR = self._frameArray[:, :, 2]

        rRatioMin = 1.0;
        circleSelected = np.uint16([])
        for circle in circles:
            centerX = circle[0]
            centerY = circle[1]
            radius = circle[2]
            initX = centerX - 2 * radius
            initY = centerY - 2 * radius

            if initX < 0 or initY < 0 or (initX + 4 * radius) > self._frameWidth or (
                    initY + 4 * radius) > self._frameHeight or radius < 1:
                continue

            rectBallArea = self._frameArray[initY:initY + 4 * radius + 1, initX:initX + 4 * radius + 1, :]
            bFlat = np.float16(rectBallArea[:, :, 0].flatten())
            gFlat = np.float16(rectBallArea[:, :, 1].flatten())
            rFlat = np.float16(rectBallArea[:, :, 2].flatten())

            rScore1 = np.uint8(rFlat > 1.0 * gFlat)
            rScore2 = np.uint8(rFlat > 1.0 * bFlat)
            rScore = float(np.sum(rScore1 * rScore2))

            gScore = float(np.sum(np.uint8(gFlat > 1.0 * rFlat)))

            rRatio = rScore / len(rFlat)
            gRatio = gScore / len(gFlat)

            print("red ratio = ", rRatio)
            print("green ratio = ", gRatio)

            if rRatio >= 0.12 and gRatio >= 0.1 and abs(rRatio - 0.19) < abs(rRatioMin - 0.19):
                circleSelected = circle

        return circleSelected

        # 使用一个方法封装函数
    def updateBallData(self, standState="standInit", color="red", color_space="BGR", fitting=False):
        """
        update the ball data with the frame get from the bottom camera.
        Arguments:
            standState: ("standInit", default), "standInit" or "standUp".
            color: ("red", default) the color of ball to be detected.
            color_space: "BGR", "HSV".
            fittting: the method of localization.
        Return:
            a dict with ball data. for example: {"centerX":0, "centerY":0, "radius":0}.
        """

        self.updateFrame()
        # cv2.imwrite("src_image.jpg", self._frameArray)
        minDist = int(self._frameHeight / 30.0)
        minRadius = 1
        maxRadius = int(self._frameHeight / 10.0)
        if color_space == "BGR":
            grayFrame = self._getChannelAndBlur(color)
        else:
            grayFrame = self._binImageHSV(color)
        # cv2.imshow("bin frame", grayFrame)
        # cv2.imwrite("bin_frame.jpg", grayFrame)
        # cv2.waitKey(20)
        circles = self._findCircles(grayFrame, minDist, minRadius, maxRadius)
        circle = self._selectCircle(circles)

        if len(circle) == 0:
            self._ballData = {"centerX": 0, "centerY": 0, "radius": 0}
            self._ballPosition = {"disX": 0, "disY": 0, "angle": 0}
        else:
            self._ballData = {"centerX": circle[0], "centerY": circle[1], "radius": circle[2]}
            if fitting == True:
                self._updateBallPositionFitting(standState=standState)
            else:
                self._updateBallPosition(standState=standState)
