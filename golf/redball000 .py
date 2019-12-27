

import sys
import time
import cv2
from cv2 import *#import opencv库
import numpy
import choose0   #import 图形筛选文件
from PIL import Image     #import python image library
from naoqi import *  

#圈取红球的主要函数
def showNaoImage(IP, PORT,camID):#参数分别为IP、PORT、摄像头ID（区分上下摄像头）

    #链接nao的摄像头
    camProxy = ALProxy("ALVideoDevice", IP, PORT)


    resolution = 2  # VGA``
    colorSpace = 11  # RGB
    videoClient = camProxy.subscribe("python_client",  resolution, colorSpace, 5)#设置分辨率、帧速、颜色空间

    t0 = time.time()
    camProxy.setParam(18,camID)#设置摄像头

    naoImage = camProxy.getImageRemote(videoClient)#将获取的图像赋给naoImage
    t1 = time.time()

    camProxy.unsubscribe(videoClient)
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]  #naoImage[6]为imagedata


    im_cv = numpy.zeros((imageHeight, imageWidth, 3), numpy.uint8)#初始化图像im_cv
    
    im_cv.data = array  #将从摄像头获取的图像copy到im_cv，转为mat

    #转化颜色空间由BGR到RGB
    b, g, r = cv2.split(im_cv)
    img1 = cv2.merge([r, g, b])
	#转mat到cvmat
    img3 = cv2.cv.fromarray(img1)
    cv2.SaveImage("test22.bmp",img3)
    #转换颜色空间到HSV
    imgHSV = cv2.CreateImage(cv2.GetSize(img3), 8, 3)
    cv2.CvtColor(img3, imgHSV, cv2.CV_RGB2HSV)

    cimg,cimg_c=hsvProceed(imgHSV,camID) #调用hsvProceed处理图像，返回二值图
    #圈取最小矩形框
	#初始化
    storage = cv2.cv.CreateMemStorage(0)
    cnts = cv2.FindContours(cimg,storage,cv2.cv.CV_RETR_LIST,cv2.cv.CV_CHAIN_APPROX_SIMPLE)
    currtnt=cnts
    Area = 0
    left_right = 0
    up_down = 0
	#为不同摄像头设置不同筛选条件
    if camID == 0:
      areamax = 2500
      areamin = 40
      valuemin = 25
      value_w = 641
      valuemax = 481
    else :
      areamax = 5000
      areamin = 400
      valuemin = 0
      value_w = 500
      valuemax = 400

    while cnts:
        rect = cv2.cv.BoundingRect(cnts,0)#获得单连通矩形框
        area = rect[2]*rect[3] #获得矩形框面积
		#获得矩形框中心点坐标
        rect_center_x = rect[0] + rect[2] / 2
        rect_center_y = rect[1] + rect[3] / 2
        #调用choose0文件下的radio函数，筛选圆形部分
        radio_c = choose0.radio(cimg_c,rect)
       
        radio = float(rect[2])/rect[3] #计算矩形框的长宽比 
        #以下if语句均为筛选条件
        if rect[1]>=valuemin:
         if rect[1]<=valuemax:
          if rect[0]<=value_w:
           if area > areamin:
             if area < areamax:
                if radio > 0.6:
                    if radio < 1.6:
                      if radio_c == 1:
                       cv2.cv.DrawContours(img3, cnts, (255, 255, 0), (255, 255, 0), 0, 1)#画出单连通轮廓
                       cv2.cv.Rectangle(img3,(rect[0],rect[1]),(rect[0]+rect[2],rect[1]+rect[3]),(0,0,255),1)#画出矩形框

                       
                       rect_center_x = rect[0] + rect[2]/2
                       rect_center_y = rect[1] + rect[3]/2
                       #计算通过条件的矩形框的面积以及在图像中的位置
                       Area = rect[2]*rect[3]
                       left_right = rect_center_x - cimg.width / 2
                       up_down = rect_center_y - cimg.height / 2
                       

        cnts = cnts.h_next()

    
    return Area,left_right,up_down #返回球的面积以及在图像中的位置
# 实现低头动作
def lookat(IP,PORT):
    motion = ALProxy("ALTracker", IP, PORT) #连接机器人
    motion.lookAt([0.4, 0, 0], 0, 0.3, False) #低头

#将摄像头获取的图像处理为单通道
def hsvProceed(img,camID): #img为一三通道的HSV图像，camID
	#初始化
    v_min = 0
    h_max = 0
    h_min = 0
    s_max = 0
    s_min = 0
	width=0
    height=0
	#创建两个单通道图像
    single = cv2.CreateImage(cv2.GetSize(img),8,1)
    single_c = cv2.CreateImage(cv2.GetSize(img),8,1)
    #为不同的摄像头分别设置h,s,v的阈值区间
    if camID == 0:
        v_min =120
        h_max = 138
        h_min = 95
        s_max = 256
        s_min = 30
    if camID == 1:
        v_min = 10
        h_max = 140
        h_min = 95
        s_max = 256
        s_min = 30

#提取红色部分到single，组建单通道图像
 
    while(1):
        while(1):
            if (img[height,width][0] >= h_min)and(img[height,width][0] < h_max)and(img[height,width][1] >= s_min)and(img[height,width][1] < s_max)and(img[height,width][2]>=v_min):#筛选红色部分
                single[height,width] = 255.0
                single_c[height, width] = 255.0
            else:
                single[height, width] = 0.0
                single_c[height, width] = 0.0
            height =height+1
            if(height==480):
                height=0
                break
        width=width+1
        if(width==640):
            break
	#形态学处理
    cv2.Erode(single,single)
    cv2.Dilate(single, single)
   
    return single,single_c
#找红球的主要逻辑部分
def findball(IP,PORT):
  
    camID = 1 #预设调用下摄像头

    count = 0 
    #优先使用下摄像头找三次，若找到返回其在图像中的位置以及camID，否则调用上摄像头找三次，找到后返回其在图像中的位置以及camID
    while True:
      count = count + 1
      SIZE,LEFT,TOP = showNaoImage(IP, PORT,camID)
      if (SIZE==0)&(LEFT==0)&(TOP==0):
          if (count==3):
              if camID==0:
                  return SIZE,LEFT,TOP,camID,0
              camID = 0
              count = 0
          else:
              continue
      else:
          break
    # if LEFT > 10:
    #   tts.say("right")
    # if LEFT < -10:
    #   tts.say("left")
    # if TOP > 10:
    #     tts.say("down")
    # if TOP < -10:
    #     tts.say("up")
    # cv.WaitKey(5)
    return SIZE,LEFT,TOP,camID,1
 #测试用主函数，无效
if __name__ == '__main__':
        IP="192.168.0.103"
        #IP="127.0.0.1"
        PORT=9559
        lookat(IP, PORT)
        # a,s,d,f,g=findball(IP, PORT)
        # if(g==1):
        #      "ss"
        # else:
        #     print "sss"

    #     while 1:
    #     #findball(IP, PORT)
    #      showNaoImage(IP,PORT,1)
    # #cv2.imshow("fsfs", img)
    #      cv2.waitKey(1)



