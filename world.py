import pybullet as p
import os
from sensor import SENSOR

class WORLD:

    def __init__(self, solutionID):

        self.planeId = p.loadURDF("plane.urdf")
        self.objects = p.loadSDF(f"world{solutionID}.sdf")
        os.system(f"rm world{solutionID}.sdf")

        # initilize sensors
        self.Prepare_To_Sense()

    def Prepare_To_Sense(self):

        self.goalSensor = SENSOR(self.objects[0])
        self.ballSensor = SENSOR(self.objects[1])

    def Sense(self, i):

        self.goalSensor.Get_Is_Touching_Object(i, self.objects[1])
        self.ballSensor.Get_Is_Touching_Object(i, self.planeId)

    def Get_Ball_ID(self):

        return self.objects[1]
