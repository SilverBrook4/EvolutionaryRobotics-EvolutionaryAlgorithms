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
            
            '''
            # gets sensor feedback
            backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
            if (frontLegSensorValues[i] == 0.0):
                print("Crash Avoided")

            # update motors
            pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = b'Torso_BackLeg', controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesBL[i], maxForce = 25)
            pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = b'Torso_FrontLeg', controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesFL[i], maxForce = 25)
            '''

            time.sleep(c.SIM_SLEEP)
