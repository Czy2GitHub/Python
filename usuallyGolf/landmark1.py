# coding:utf-8

import sys
import time
import cv2
from cv2 import *
import numpy
import choose0
#import Image
from naoqi import *



# 通过检测到的黄杆的宽值和左右偏值计算黄杆相对摄像头的x，y坐标
def getloacation(width,left):
	#三米处测量初始x，y值
    x0 = 3.0
    y0 = 1.5
    height_x = 21.0
	#相似三角形计算
    r = float(width)/height_x
    x = x0/r
    y = ((x/x0) * (float(left)/320.0))*y0
    return x,y
def landmarkdetect(IP, PORT,camID):


    camProxy = ALProxy("ALVideoDevice", IP, PORT) #连接nao的摄像头


    resolution = 2  # VGA``
    colorSpace = 11  # RGB
    videoClient = camProxy.subscribe("python_client",  resolution, colorSpace, 5) #设置摄像头的获取图像的颜色空间，分辨率，帧速

    camProxy.setParam(18,camID) #设置摄像头ID（默认0为上摄像头，1为下摄像头）
    #将获取到的图像的data赋给array
    naoImage = camProxy.getImageRemote(videoClient)
    camProxy.unsubscribe(videoClient)
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]

    array = naoImage[6]
   
    #将array转为mat
    im_cv = numpy.zeros((imageHeight, imageWidth, 3), numpy.uint8)
    im_cv.data = array
    #更改颜色空间由BGR到RGB
    b, g, r = cv2.split(im_cv)
    img1 = cv2.merge([r, g, b])
    #将mat转为cvmat类型
    img3 = cv2.cv.fromarray(img1)
    cv.SaveImage("save1.jpg",img3)  
    #转换颜色空间由RGB到HSV
    imgHSV = cv.CreateImage(cv.GetSize(img3), 8, 3)
    cv.CvtColor(img3, imgHSV, cv.CV_RGB2HSV)

    cimg,cimg_c=hsvProceed(imgHSV) #调用hsvProceed函数处理hsv图像并返回处理后的单通道图像

 
    #圈取最小矩形框
    storage = cv2.cv.CreateMemStorage(0)
    cnts = cv.FindContours(cimg,storage,cv2.cv.CV_RETR_LIST,cv2.cv.CV_CHAIN_APPROX_SIMPLE)
    currtnt=cnts
    x = 0.0
    Area = 0
    left_right = 0
    up_down = 0
    #为不同摄像头分别设置不同的筛选条件
    if camID == 0:
      areamax = 6000
      areamin = 350
      value = img3.height/7 
    else :
      areamax = 5000
      areamin = 400
      value = 0
    #循环获得所有的最小矩形框
    while cnts:
        rect = cv2.cv.BoundingRect(cnts,0)
        area = rect[2]*rect[3]
        rect_center_x = rect[0] + rect[2] / 2
        rect_center_y = rect[1] + rect[3] / 2
    

        radio = float(rect[2])/rect[3]
        #筛选条件
        if rect[1]>10:

          if area > areamin:
             if area < areamax:
                if radio > 0.1:
                     if radio < 1.0:
                       rect_center_x = rect[0] + rect[2]/2
                       rect_center_y = rect[1] + rect[3]/2
                       #获得黄杆在图像中的位置以及相对当前摄像头的x，y值
                       Area = rect[2]*rect[3]
                       left_right = rect_center_x - cimg.width / 2
                       up_down = rect_center_y - cimg.height / 2
                       x, y = getloacation(rect[2],left_right)


        cnts = cnts.h_next()

    
    return Area,left_right,x  #返回黄杆面积，在图像中的左右位置，摄像头到黄杆的距离（m）



#同redball000的hsvProceed

def hsvProceed(img):
    single = cv.CreateImage(cv.GetSize(img),8,1)
    single_c = cv.CreateImage(cv.GetSize(img),8,1)
    width=0
    height=0
    while(1):
        while(1):
            if (img[height,width][0] > 70)and(img[height,width][0] < 95)and(img[height,width][1] > 53)and(img[height,width][1] < 230):#and(img[height,width][2]<200):
                single[height,width] = 255
                single_c[height, width] = 255
            else:
                single[height, width] = 0
                single_c[height, width] = 0
            height =height+1
            if(height==480):
                height=0
                break
        width=width+1
        if(width==640):
            break
    cv.Erode(single,single)
    cv.Dilate(single, single)
    cv.Erode(single_c, single_c)
    cv.Dilate(single_c, single_c)
    
    return single,single_c


#测试函数，无效
if __name__ == '__main__':
        IP="192.168.1.104"
        #IP="127.0.0.1"
        PORT=9559
        #lookat(IP, PORT)
        #a,s,d,f,g=findball(IP, PORT)
        # if(g==1):
        #     print "ss"
        # else:
        #     print "sss"

       # while 1:
         #findball(IP, PORT)
        landmarkdetect(IP,PORT,0)
    #cv2.imshow("fsfs", img)
        #cv2.waitKey(0)



