# coding:utf-8

from naoqi import ALProxy
import time
import math
print 69.7 * math.pi / 180.0
# <type 'list'>: [[3691, 136218], [-0.12791083753108978, -0.1820196807384491, 0.026518099009990692, 0.027383489534258842], [0.050945501774549484, -0.000627366651315242, 0.14354035258293152, 0.0, 0.7066597938537598, -0.012313843704760075], [0.06870284676551819, -0.008956825360655785, 0.45710310339927673, 0.001952563296072185, 0.7035399675369263, -0.011221031658351421], 1]
# PositionJointNamesR = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
# golfPositionJointAnglesR5 = [1.319469, -0.5131268, 1.6615535, 1.3578662, 0.2076942, 0.0]
# golfPositionJointAnglesR6 = [1.319469, -0.5131268, 1.6615535, 1.3578662, 0.2076942, 1.0]
# golfPositionJointAnglesR101 = [1.1868239, 0.0698132, 1.6144296, 0.12514011, 0.3804818, 0.0]
ip = "192.168.31.120"
port = 9559
motion = ALProxy("ALMotion", ip, port)
motion.wakeUp()
motion.angleInterpolationWithSpeed("HeadPitch", 0.5236, 0.3)
# time.sleep(3)
# motion.angleInterpolationWithSpeed(PositionJointNamesR, golfPositionJointAnglesR5, 0.4)
# time.sleep(1)
# motion.angleInterpolationWithSpeed(PositionJointNamesR, golfPositionJointAnglesR101, 0.01)
