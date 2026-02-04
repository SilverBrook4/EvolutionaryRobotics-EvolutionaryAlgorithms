import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np

class MOTOR:

    # class constructor
    def __init__(self, jointName):

        self.jointName = jointName

        self.Prepare_To_Act()


    # prepares motor's movement values
    def Prepare_To_Act(self):

        # create values to modify motor oscilation
        self.amplitude = c.AMPLITUDE
        self.frequency = c.FREQUENCY
        self.offset = c.PHASE_OFFSET

        # sets the oscilation wave for the motor
        self.motorValues = np.linspace(-np.pi, np.pi, c.NUM_SIM_STEPS)
        self.motorValues = self.amplitude * np.sin(self.frequency * self.motorValues + self.offset)


    # sets the motor value for current time step
    def Set_Value(self, i, robotId):

        pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = self.jointName, controlMode = p.POSITION_CONTROL, targetPosition = self.motorValues[i], maxForce = 25)


    # saves motor values to disk
    def Save_Values(self):

        np.save(f"data//{self.jointName}Values.npy", self.motorValues)
