import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np

class MOTOR:

    # class constructor
    def __init__(self, jointName, jointRange=None):

        self.jointName = jointName

        if jointRange == None:

            self.jointRange = c.MOTOR_JOINT_RANGE

        else:

            self.jointRange = jointRange


    # sets the motor value for current time step
    def Set_Value(self, desiredAngle, robotId):

        pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = self.jointName, controlMode = p.POSITION_CONTROL, targetPosition = desiredAngle, maxForce = c.MAX_MOTOR_FORCE)

    def Get_Joint_Range(self):

        return self.jointRange
