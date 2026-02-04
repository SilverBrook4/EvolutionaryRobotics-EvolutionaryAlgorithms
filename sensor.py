import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c

class SENSOR:

    # class constructor
    def __init__(self, linkName):

        self.linkName = linkName

        # initilaize sensor data array to 0's
        self.values = np.zeros(c.NUM_SIM_STEPS)


    # stores sensor value in values at index i
    def Get_Value(self, i):

        self.values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)


    # saves sensor input to disk
    def Save_Values(self):

        np.save(f"data//{self.linkName}SensorValues.npy", self.values)
