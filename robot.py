import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR

class ROBOT:

    def __init__(self):

        self.sensors = {}
        self.motors = {}

        # loads robot from body.urdf
        self.robotId = p.loadURDF("body.urdf")

        # prepares to simulate robot
        pyrosim.Prepare_To_Simulate(self.robotId)
