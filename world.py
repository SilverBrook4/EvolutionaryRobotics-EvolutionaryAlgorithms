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
        self.goalBallDistanceSensor = SENSOR(self.objects[0])

    def Sense(self, i):

        self.goalSensor.Get_Is_Touching_Object(i, self.objects[1])
        self.ballSensor.Get_Is_Touching_Object(i, self.planeId)
        self.goalBallDistanceSensor.Get_Distance_To(i, self.objects[1])

        return self.goalBallDistanceSensor.Get_Current_Value(i)

    def Get_Ball_ID(self):

        return self.objects[1]

    def Get_Ball_On_Ground_Values(self):

        return self.ballSensor.Get_Values()

    def Get_Closest_To_Goal_Value(self):

        values = self.goalBallDistanceSensor.Get_Values()

        distance = 1000

        for value in values:

            if value < distance:

                distance = value

        return distance

    def Get_Goal_Scored(self):

        values = self.goalBallDistanceSensor.Get_Values()

        for values in values:

            if value == 1.0:

                return 1.0

        return 0.0
