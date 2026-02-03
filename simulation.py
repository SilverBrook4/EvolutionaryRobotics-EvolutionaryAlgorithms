import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from world import WORLD
from robot import ROBOT
import constants as c

class SIMULATION:

    def __init__(self):

        # connects to physics client 
        self.physicsClient = p.connect(p.GUI)

        # sets physics client search path
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # checks if pybullet debugger is enabled 
        if (c.PYBULLET_DEBUGGER):
            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

        # sets physics client gravity 
        p.setGravity(0, 0, -9.8, self.physicsClient)

        self.world = WORLD()
        self.robot = ROBOT()
