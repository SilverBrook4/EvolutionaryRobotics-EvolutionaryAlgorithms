import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from world import WORLD
from robot import ROBOT
import constants as c
import time

class SIMULATION:

    # class constructor
    def __init__(self):

        # connects to physics client 
        self.physicsClient = p.connect(p.GUI)

        # sets physics client search path
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # checks if pybullet debugger is enabled 
        if (not(c.PYBULLET_DEBUGGER)):
            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

        # sets physics client gravity 
        p.setGravity(0, 0, -9.8, self.physicsClient)

        self.world = WORLD()
        self.robot = ROBOT()


    # class destructor
    def __del__(self):

        p.disconnect()


    # runs the simulation loop and steps simulation
    def Run(self):

        # executes simulation loop
        for i in range(c.NUM_SIM_STEPS):

            # step simulation
            print("Simulation Step: " + str(i))
            p.stepSimulation()

            # runs sensors in robots links
            self.robot.Sense(i)

            # tells the robot to interpret sensor input with its neural network
            self.robot.Think()

            # updates motors for the current step
            self.robot.Act(i)

            # slows simulation so it can be observed
            time.sleep(c.SIM_SLEEP)
