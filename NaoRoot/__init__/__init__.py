# coding:utf-8
from NaoVision import VisionBasic
import numpy as np
import ShapeDetector
from RecognizeShape import NaoShape
from RecognizeBall import Recognize
import cv2
if __name__ == "__main__":
    # 识别形状
    shape = Recognize()
    while True:
        shape.getImage()
        shape.readImage()
        shape.searchBall()
        shape.showImage(shape.frameArray)


