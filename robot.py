import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR

class ROBOT:

    # class constructor
    def __init__(self):

        self.motors = {}

        # loads robot from body.urdf
        self.robotId = p.loadURDF("body.urdf")

        # prepares to simulate robot
        pyrosim.Prepare_To_Simulate(self.robotId)

        # prepare sensors for links
        self.Prepare_To_Sense()

    # prepares sensors for every link
    def Prepare_To_Sense(self):

        self.sensors = {}

        for linkName in pyrosim.linkNamesToIndices:

            print(linkName)
