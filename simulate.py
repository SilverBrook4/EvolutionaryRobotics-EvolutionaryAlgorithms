import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import time
import math
import random
import constants as c
from simulation import SIMULATION

'''
# initilize variables
NUMSIMSTEPS = 1000 # sets number of simulation steps
amplitudeBL = numpy.pi / 6
frequencyBL = 10
phaseOffsetBL = 0
amplitudeFL = numpy.pi / 2
frequencyFL = 10
phaseOffsetFL = 0
'''

'''
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# comment out to enable debugger in pybullet simulation
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

# add gravity
p.setGravity(0, 0, -9.8, physicsClient)

# load links
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

# initialize sensors
pyrosim.Prepare_To_Simulate(robotId)

# initilaze numpy values
backLegSensorValues = numpy.zeros(c.NUM_SIM_STEPS)
frontLegSensorValues = numpy.zeros(c.NUM_SIM_STEPS)

# intitilize movement array
targetAnglesBL = c.AMPLITUDE_BL * numpy.sin(c.FREQUENCY_BL * numpy.linspace(-numpy.pi, numpy.pi, c.NUM_SIM_STEPS) + c.PHASE_OFFSET_BL)
targetAnglesFL = c.AMPLITUDE_FL * numpy.sin(c.FREQUENCY_FL * numpy.linspace(-numpy.pi, numpy.pi, c.NUM_SIM_STEPS) + c.PHASE_OFFSET_FL)
#numpy.save("data//TargetAnglesBL.npy", targetAnglesBL)
#numpy.save("data//TargetAnglesFL.npy", targetAnglesFL)
#exit()

for i in range(c.NUM_SIM_STEPS):
    # steps simulation
    p.stepSimulation()

    # gets sensor feedback
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    if (frontLegSensorValues[i] == 0.0):
        print("Crash Avoided")

    # update motors
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = b'Torso_BackLeg', controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesBL[i], maxForce = 25)
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = b'Torso_FrontLeg', controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesFL[i], maxForce = 25)

    print(i)
    time.sleep(c.SIM_SLEEP)
p.disconnect()

# save sensor values
numpy.save("data//BackLegSensorValues.npy", backLegSensorValues)
numpy.save("data//FrontLegSensorValues.npy", frontLegSensorValues)
'''
simulation = SIMULATION()

