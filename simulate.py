import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import time
import math
import random

#sets number of steps for simulation
numSimSteps = 1000

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
backLegSensorValues = numpy.zeros(numSimSteps)
frontLegSensorValues = numpy.zeros(numSimSteps)

for i in range(numSimSteps):
    # steps simulation
    p.stepSimulation()

    # gets sensor feedback
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    if (frontLegSensorValues[i] == 0.0):
        print("Crash Avoided")

    # update motors
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = b'Torso_BackLeg', controlMode = p.POSITION_CONTROL, targetPosition = math.pi/2-(4*random.random()), maxForce = 50)
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = b'Torso_FrontLeg', controlMode = p.POSITION_CONTROL, targetPosition = math.pi/2-(4*random.random()), maxForce = 50)

    print(i)
    time.sleep(0.1)
p.disconnect()

# save sensor values
numpy.save("data//BackLegSensorValues.npy", backLegSensorValues)
numpy.save("data//FrontLegSensorValues.npy", frontLegSensorValues)

