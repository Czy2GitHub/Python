import cv2
import time
import numpy as np
import math
def findYellowStick(camProxy):
    """
    :param minPerimeter: yellow area min perimeter
    """
    TIME = time.strftime('%m-%d_%H-%M-%S', time.localtime(time.time()))
    print("Finding Yellow Stick")
    # 15-20 contains orange
    low = np.array([15, 80, 80])             # 设置最低阈值
    up = np.array([36, 255, 255])
    camProxy.setActiveCamera(0)
    videoClient = camProxy.subscribe("python_client", 2, 11, 5) # 640*480，RGB, FPS
    rowImgData = camProxy.getImageRemote(videoClient)
    camProxy.unsubscribe(videoClient)
    imgWidth = rowImgData[0]
    imgHeight = rowImgData[1]
    # 初始化一个三维动态矩阵
    image = np.zeros((imgHeight, imgWidth, 3), dtype='uint8')
    image.data = rowImgData[6]
    # 使用split来拆分，获得三通道
    b, g, r = cv2.split(image)
    # 将BGR转换为RGB
    # merge 合并
    img = cv2.merge([r, g, b])
    # deal img
    cv2.imwrite("scr.jpg", img)
    frameHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    frameBin = cv2.inRange(frameHSV, low, up)
    # np.ones:创建任意维度和元素个数的数组，其元素值均为一；初始化一个数组
    kernelErosion = np.ones((5, 5), np.uint8)
    kernelDilation = np.ones((5, 5), np.uint8)

    # cv2.erode 方法对二值图进行腐蚀操作
    frameBin = cv2.erode(frameBin, kernelErosion, iterations=1)
    # cv2.dilate 方法对二值图进行膨胀操作
    frameBin = cv2.dilate(frameBin, kernelDilation, iterations=1)
    # 高斯滤波
    frameBin = cv2.GaussianBlur(frameBin, (3, 3), 0)
    # frameBin debug
    cv2.imwrite("bin.jpg", frameBin)
     # 获取轮廓
    _, contours = cv2.findContours(frameBin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) == 0:
        cv2.imwrite("not_find_stick%s.jpg" %TIME, img)
        print("no Yellow in img")
        return []
    # abandon some yello shape because of width
    good_contour = []
    for contour in contours:
        # perimeter 周长
        # 得到轮廓的周长
        perimeter = cv2.arcLength(contour, True)
        print perimeter
        # 根据周长筛选掉不合要求的区块，如果后期要反复调用，可以把周长作为参数
        if perimeter <= 200 or perimeter >= 400:
            continue
        # ratio为长宽之比等于三
        ratio = 3
        if perimeter >= 250:
            ratio = 4
        # 通过形状得到最小外接矩形
        box2D = cv2.minAreaRect(contour)
        # 取box2D[1]][0]与box2D[1][1]中,小的值为
        w = min(box2D[1][0], box2D[1][1])
        h = max(box2D[1][0], box2D[1][1])
        # 如果长小于宽的四倍，继续寻找
        if w * ratio > h:
            continue
        # 如果长超出宽的四倍，添加形状good_contour
        good_contour.append(contour)
    # 如果为零，则
    if len(good_contour) == 0:
        cv2.imwrite("not_find_stick%s.jpg" %TIME, img)
        print("Yellow range width is to large")
        return []
    # find big contour
    maxContour = good_contour[0]
    maxPerimeter = 100
    for contour in good_contour:
        perimeter = cv2.arcLength(contour, True)
        if perimeter > maxPerimeter:
            maxPerimeter = perimeter
            maxContour = contour
    # find alpha
    box2D = cv2.minAreaRect(maxContour)
    if box2D[1][0] > box2D[1][1]:
        w = box2D[1][1]
        h = box2D[1][0]
        center = box2D[0]
        theta = -box2D[2] * math.pi / 180
        alpha = theta + math.atan(1.0 * w / h)
        bevel = math.sqrt(w * w + h * h) / 2
        x1 = int(center[0] - bevel * math.cos(alpha))
        x2 = int(x1 - w * math.sin(theta))
        x = int((x1 + x2) / 2)
    else:
        w = box2D[1][0]
        h = box2D[1][1]
        center = box2D[0]
        theta = -box2D[2] * math.pi / 180
        alpha = theta + math.atan(1.0 * h / w)
        bevel = math.sqrt(w * w + h * h) / 2
        x1 = int(center[0] - bevel * math.cos(alpha) )
        x2 = int(x1 + w * math.cos(theta) )
        x = int((x1 + x2) / 2)
    cv2.drawContours(img, maxContour, -1, (0, 0, 255), 1)
    cv2.imwrite("ok.jpg", img)
    return (320.0 - x)/640.0 * 60.97 * math.pi / 180
