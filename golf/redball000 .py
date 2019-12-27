

import sys
import time
import cv2
from cv2 import *#import opencv��
import numpy
import choose0   #import ͼ��ɸѡ�ļ�
from PIL import Image     #import python image library
from naoqi import *  

#Ȧȡ�������Ҫ����
def showNaoImage(IP, PORT,camID):#�����ֱ�ΪIP��PORT������ͷID��������������ͷ��

    #����nao������ͷ
    camProxy = ALProxy("ALVideoDevice", IP, PORT)


    resolution = 2  # VGA``
    colorSpace = 11  # RGB
    videoClient = camProxy.subscribe("python_client",  resolution, colorSpace, 5)#���÷ֱ��ʡ�֡�١���ɫ�ռ�

    t0 = time.time()
    camProxy.setParam(18,camID)#��������ͷ

    naoImage = camProxy.getImageRemote(videoClient)#����ȡ��ͼ�񸳸�naoImage
    t1 = time.time()

    camProxy.unsubscribe(videoClient)
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]  #naoImage[6]Ϊimagedata


    im_cv = numpy.zeros((imageHeight, imageWidth, 3), numpy.uint8)#��ʼ��ͼ��im_cv
    
    im_cv.data = array  #��������ͷ��ȡ��ͼ��copy��im_cv��תΪmat

    #ת����ɫ�ռ���BGR��RGB
    b, g, r = cv2.split(im_cv)
    img1 = cv2.merge([r, g, b])
	#תmat��cvmat
    img3 = cv2.cv.fromarray(img1)
    cv2.SaveImage("test22.bmp",img3)
    #ת����ɫ�ռ䵽HSV
    imgHSV = cv2.CreateImage(cv2.GetSize(img3), 8, 3)
    cv2.CvtColor(img3, imgHSV, cv2.CV_RGB2HSV)

    cimg,cimg_c=hsvProceed(imgHSV,camID) #����hsvProceed����ͼ�񣬷��ض�ֵͼ
    #Ȧȡ��С���ο�
	#��ʼ��
    storage = cv2.cv.CreateMemStorage(0)
    cnts = cv2.FindContours(cimg,storage,cv2.cv.CV_RETR_LIST,cv2.cv.CV_CHAIN_APPROX_SIMPLE)
    currtnt=cnts
    Area = 0
    left_right = 0
    up_down = 0
	#Ϊ��ͬ����ͷ���ò�ͬɸѡ����
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
        rect = cv2.cv.BoundingRect(cnts,0)#��õ���ͨ���ο�
        area = rect[2]*rect[3] #��þ��ο����
		#��þ��ο����ĵ�����
        rect_center_x = rect[0] + rect[2] / 2
        rect_center_y = rect[1] + rect[3] / 2
        #����choose0�ļ��µ�radio������ɸѡԲ�β���
        radio_c = choose0.radio(cimg_c,rect)
       
        radio = float(rect[2])/rect[3] #������ο�ĳ���� 
        #����if����Ϊɸѡ����
        if rect[1]>=valuemin:
         if rect[1]<=valuemax:
          if rect[0]<=value_w:
           if area > areamin:
             if area < areamax:
                if radio > 0.6:
                    if radio < 1.6:
                      if radio_c == 1:
                       cv2.cv.DrawContours(img3, cnts, (255, 255, 0), (255, 255, 0), 0, 1)#��������ͨ����
                       cv2.cv.Rectangle(img3,(rect[0],rect[1]),(rect[0]+rect[2],rect[1]+rect[3]),(0,0,255),1)#�������ο�

                       
                       rect_center_x = rect[0] + rect[2]/2
                       rect_center_y = rect[1] + rect[3]/2
                       #����ͨ�������ľ��ο������Լ���ͼ���е�λ��
                       Area = rect[2]*rect[3]
                       left_right = rect_center_x - cimg.width / 2
                       up_down = rect_center_y - cimg.height / 2
                       

        cnts = cnts.h_next()

    
    return Area,left_right,up_down #�����������Լ���ͼ���е�λ��
# ʵ�ֵ�ͷ����
def lookat(IP,PORT):
    motion = ALProxy("ALTracker", IP, PORT) #���ӻ�����
    motion.lookAt([0.4, 0, 0], 0, 0.3, False) #��ͷ

#������ͷ��ȡ��ͼ����Ϊ��ͨ��
def hsvProceed(img,camID): #imgΪһ��ͨ����HSVͼ��camID
	#��ʼ��
    v_min = 0
    h_max = 0
    h_min = 0
    s_max = 0
    s_min = 0
	width=0
    height=0
	#����������ͨ��ͼ��
    single = cv2.CreateImage(cv2.GetSize(img),8,1)
    single_c = cv2.CreateImage(cv2.GetSize(img),8,1)
    #Ϊ��ͬ������ͷ�ֱ�����h,s,v����ֵ����
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

#��ȡ��ɫ���ֵ�single���齨��ͨ��ͼ��
 
    while(1):
        while(1):
            if (img[height,width][0] >= h_min)and(img[height,width][0] < h_max)and(img[height,width][1] >= s_min)and(img[height,width][1] < s_max)and(img[height,width][2]>=v_min):#ɸѡ��ɫ����
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
	#��̬ѧ����
    cv2.Erode(single,single)
    cv2.Dilate(single, single)
   
    return single,single_c
#�Һ������Ҫ�߼�����
def findball(IP,PORT):
  
    camID = 1 #Ԥ�����������ͷ

    count = 0 
    #����ʹ��������ͷ�����Σ����ҵ���������ͼ���е�λ���Լ�camID���������������ͷ�����Σ��ҵ��󷵻�����ͼ���е�λ���Լ�camID
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
 #����������������Ч
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



