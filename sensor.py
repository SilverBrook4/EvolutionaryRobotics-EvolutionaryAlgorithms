import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c

class SENSOR:

    # class constructor
    def __init__(self, name):

        self.name = name

        # initilaize sensor data array to 0's
        self.values = np.zeros(c.NUM_SIM_STEPS)

        self.firstRun = True


    # stores sensor value in values at index i
    def Get_Value(self, i):

        self.values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.name)


    # gets if sensor is contacting a specific object
    def Get_Is_Touching_Object(self, i, objName):

        self.values[i] = pyrosim.Get_Contact_Between_Objects(self.name, objName)


    def Get_Is_Robot_Touching_Object(self, i, objName, robotId):

        self.values[i] = pyrosim.Get_Contact_Between_Robot_And_Object(robotId, objName, self.name)
        print(self.values[i])


    def Get_Joint_Angle(self, i, robotId):

        self.values[i] = pyrosim.Get_Joint_Angle(robotId, self.name)


    def Get_Link_Position(self, i, robotId):

        if self.firstRun:

            self.values = np.zeros((c.NUM_SIM_STEPS, 3))

        x, y, z = pyrosim.Get_Link_Position(robotId, self.name)
        self.values[i] = [x, y, z]


    def Get_Distance_To(self, i, obj):

        self.values[i] = pyrosim.Get_Distance_Between(self.name, obj)

    # saves sensor input to disk
    def Save_Values(self):

        np.save(f"data//{self.linkName}SensorValues.npy", self.values)
