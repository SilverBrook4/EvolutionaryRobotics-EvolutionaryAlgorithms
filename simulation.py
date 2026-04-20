import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from world import WORLD
from robot import ROBOT
import constants as c
import time

class SIMULATION:

    # class constructor
    def __init__(self, directOrGUI, solutionID):

        # connects to physics client
        if (directOrGUI == "DIRECT"):

            self.physicsClient = p.connect(p.DIRECT)
            self.shouldSleep = False

        else:

            self.physicsClient = p.connect(p.GUI)
            self.shouldSleep = True

        # sets physics client search path
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # checks if pybullet debugger is enabled 
        if (not(c.PYBULLET_DEBUGGER)):

            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

        # sets physics client gravity 
        p.setGravity(0, 0, -9.8, self.physicsClient)

        self.world = WORLD(solutionID)
        self.robot = ROBOT(solutionID)


    # class destructor
    def __del__(self):

        p.disconnect()


    # runs the simulation loop and steps simulation
    def Run(self):

        # executes simulation loop
        for i in range(c.NUM_SIM_STEPS):

            # step simulation
            if (c.SHOW_NN_UPDATES):
                print("Simulation Step: " + str(i))

            p.stepSimulation()

            # runs sensors in robots links and world
            worldSensorvalues = self.world.Sense(i)
            robotSensorValues = self.robot.Sense(i, self.world.Get_Ball_ID())

            # tells the robot to interpret sensor input with its neural network
            self.robot.Think(robotSensorValues + worldSensorvalues)

            # updates motors for the current step
            self.robot.Act(i)

            # slows simulation so it can be observed
            if (self.shouldSleep):
                time.sleep(c.SIM_SLEEP)


    # evaluates the fitness of a specific robot
    def Get_Fitness(self, connection):

        self.robot.Get_Fitness(connection, self.world.Get_Closest_To_Goal_Value())
