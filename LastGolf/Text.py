# coding:utf-8
from naoqi import ALProxy
motionPrx = ALProxy("ALMotion", "192.168.43.32", 9559)
shouganJoint = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"]
shouganSongshou = [1.0995575, -0.0069813, -1.4486233, -1.0314896, -1.6737708, 1.0]
shouganFangxia = [1.462586, 0.0820305, -1.4765486, -0.0349066, 0.0]
def ShoulderpitchAmend2():
    names = list()
    keys = list()
    times = list()
    names.append("LShoulderPitch")  #
    times.append([0.5, 1])
    keys.append([1.43856, 1.88495559])
    names.append("RShoulderPitch")  #
    times.append([0.5, 1])
    keys.append([1.43856, 1.88495559])
    names.append("LElbowRoll")  #
    times.append([0.5, 1])
    keys.append([-1.23490659, -1.51843645])
    names.append("RElbowRoll")  #
    times.append([0.5, 1])
    keys.append([1.23490659, 1.51843645])
    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.angleInterpolation(names, keys, times, True)
def shougang(): # 收杆
    # 声明三个空列表
    names = list()      # 关节名
    times = list()      # 关节移动所用时间
    keys = list()       # 关节坐标
    # 添加头部横轴 关节动作
    names.append("HeadPitch")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("HeadYaw")  # Z轴动
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])
    # ankle 脚踝
    names.append("LAnklePitch")  # 脚踝Z轴
    times.append([1, 2, 3, 4])
    keys.append([-0.349794, -0.349794, -0.349794, -0.349794])

    names.append("LAnkleRoll")  # 脚踝X轴
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])
    # elbow 肘部
    names.append("LElbowRoll")  # 肘Z轴
    times.append([1, 2, 3, 4])
    keys.append([-0.321141, -0.321141, -1.1, -1.1])

    names.append("LElbowYaw")  # X轴
    times.append([1, 2, 3, 4])
    keys.append([-1.37757, -1.37757, -1.466076, -1.466076])

    names.append("LHand")  # 左掌
    times.append([1, 2, 3, 4, 5.2])
    keys.append([0.9800, 0.9800, 0.9800, 0.9800, 0.1800])
    # hip 臀部
    names.append("LHipPitch")  # 腿Y轴
    times.append([1, 2, 3, 4])
    keys.append([-0.450955, -0.450955, -0.450955, -0.450955])

    names.append("LHipRoll")  # 腿X轴
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("LHipYawPitch")  # 啥关节
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("LKneePitch")  # 膝盖Y轴
    times.append([1, 2, 3, 4])
    keys.append([0.699462, 0.699462, 0.699462, 0.699462])

    names.append("LShoulderPitch")  # 左肩轴
    times.append([1, 2, 3, 4, 5.2])
    ##------------------------------------------------------------
    keys.append([1.53885, 1.43885, 1.3, 1.3, 1.3])

    names.append("LShoulderRoll")  # 肩Z轴
    times.append([1, 2, 3, 4, 5.2])
    keys.append([0.268407, 0.268407, -0.04014, -0.04014, -0.04014])

    names.append("LWristYaw")  # 手腕X轴
    times.append([1, 2, 3, 4])
    keys.append([-0.016916, -0.016916, -1.632374, -1.632374])

    names.append("RAnklePitch")  # 脚踝Y轴
    times.append([1, 2, 3, 4])
    keys.append([-0.354312, -0.354312, -0.354312, -0.354312])

    names.append("RAnkleRoll")  # 脚踝X轴
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("RElbowRoll")  # 肘Z轴
    times.append([1, 2, 3, 4])
    keys.append([0.958791, 0.958791, 0.958791, 0.958791])

    names.append("RElbowYaw")  # 肘X轴
    times.append([1, 2, 3, 4])
    keys.append([1.466076, 1.466076, 1.466076, 1.466076])

    names.append("RHand")
    times.append([1, 2, 3, 4])
    keys.append([0.0900, 0.0900, 0.0900, 0.0900])

    names.append("RHipPitch")  # 腿Y轴
    times.append([1, 2, 3, 4])
    keys.append([-0.451038, -0.451038, -0.451038, -0.451038])

    names.append("RHipRoll")  # 腿X轴
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("RHipYawPitch")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("RKneePitch")  # 膝盖Y轴
    times.append([1, 2, 3, 4])
    keys.append([0.699545, 0.699545, 0.699545, 0.699545])

    names.append("RShoulderPitch")  # 肩Y轴
    times.append([0.5,1, 2, 3, 4, 5.2])
    # keys.append([1.03856, 1.03856, 1.03856, 1.03856, 1.03856])
    keys.append([0.9, 1.03856, 1.03856,1.03856, 1.03856, 1.03856])

    names.append("RShoulderRoll")  # 肩Z轴
    times.append([1, 2, 3, 4, 5.2])
    keys.append([0.04014, 0.04014, 0.04014, 0.04014, 0.04014])

    names.append("RWristYaw")  # 腕X轴
    times.append([1, 2, 3, 4])
    keys.append([1.632374, 1.632374, 1.632374, 1.632374])
    motionPrx.setMoveArmsEnabled(False, False)  # 设置移动时候左右手不动
    motionPrx.angleInterpolation(names, keys, times, True)  # 如果为true，则以绝对角度描述运动，否则角度相对于当前角度why？

def LShoulderpitchAmend():
    names = list()
    keys = list()
    times = list()
    names.append("LShoulderPitch")  #
    times.append([1])
    keys.append([1.03856])
    names.append("LHand")
    times.append([1, 2, 3, 4])
    keys.append([0.0200, 0.0200, 0.0200, 0.0200])
    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.angleInterpolation(names, keys, times, True)
shougang()
# ShoulderpitchAmend2()
LShoulderpitchAmend()