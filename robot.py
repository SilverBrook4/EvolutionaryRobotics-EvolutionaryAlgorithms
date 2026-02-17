import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR
import constants as c
import os

class ROBOT:

    # class constructor
    def __init__(self, solutionID):

        # loads robot from body.urdf
        self.robotId = p.loadURDF("body.urdf")

        # load neural network from brain.nndf
        self.myID = solutionID
        self.nn = NEURAL_NETWORK(f"brain{self.myID}.nndf")

        # prepares to simulate robot
        pyrosim.Prepare_To_Simulate(self.robotId)

        # prepare sensors for links
        self.Prepare_To_Sense()

        # prepares motors to move
        self.Prepare_To_Act()

        # cleans up brain files
        os.system(f"rm brain{self.myID}.nndf")


    # prepares sensors for every link
    def Prepare_To_Sense(self):

        self.sensors = {}

        for linkName in pyrosim.linkNamesToIndices:

            self.sensors[linkName] = SENSOR(linkName)


    # get and store sensor data for robot object
    def Sense(self, i):

        for sensor in self.sensors.values():

            sensor.Get_Value(i)


    # prepare motors at each joint
    def Prepare_To_Act(self):

        self.motors = {}

        for jointName in pyrosim.jointNamesToIndices:

            self.motors[jointName] = MOTOR(jointName)


    # updates each motor
    def Act(self, i):

        for neuronName in self.nn.Get_Neuron_Names():

            if self.nn.Is_Motor_Neuron(neuronName):

                # gets motor neurons output value and correct motor
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)

                # updates motor neurons
                self.motors[jointName.encode()].Set_Value(desiredAngle, self.robotId)


    # activates neural network to interpret sensor input and update robot
    def Think(self):

        self.nn.Update()

        if (c.SHOW_NN_UPDATES):
            self.nn.Print()


    # gets the fitness of the robot
    def Get_Fitness(self):

        # gets the x position or fitness of the robot
        stateOfLinkZero = p.getLinkState(self.robotId, 0)

        positionOfLinkZero = stateOfLinkZero[0]

        xCoordinateOfLinkZero = positionOfLinkZero[0]

        # writes fitness to a temporary file
        with open(f"data//tmp{self.myID}.txt", "w") as f:

            f.write(str(xCoordinateOfLinkZero))

            f.close()

        # copys the fitness value to the fitness file
        os.system(f"mv data//tmp{self.myID}.txt data//fitness{self.myID}.txt")
