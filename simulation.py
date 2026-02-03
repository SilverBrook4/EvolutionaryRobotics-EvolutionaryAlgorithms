import pybullet as p
import pybullet_data
from world import WORLD
from robot import ROBOT
import constants as c

class SIMULATION:

    def __init__(self):

        self.world = WORLD()
        self.robot = ROBOT()

        self.physicsClient = p.connect(p.GUI)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        if (c.PYBULLET_DEBUGGER):
            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

        p.setGravity(0, 0, -9.8, self.physicsClient)
