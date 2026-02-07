import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR

class ROBOT:

    # class constructor
    def __init__(self):

        # loads robot from body.urdf
        self.robotId = p.loadURDF("body.urdf")

        # load neural network from brain.nndf
        self.nn = NEURAL_NETWORK("brain.nndf")

        # prepares to simulate robot
        pyrosim.Prepare_To_Simulate(self.robotId)

        # prepare sensors for links
        self.Prepare_To_Sense()

        # prepares motors to move
        self.Prepare_To_Act()


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

        for motor in self.motors.values():

            motor.Set_Value(i, self.robotId)


    # activates neural network to interpret sensor input and update robot
    def Think(self):

        self.nn.Update()

        self.nn.Print()
