import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import time

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
backLegSensorValues = numpy.zeros(100)

for i in range(100):
    # steps simulation
    p.stepSimulation()

    # gets sensor feedback
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")

    time.sleep(0.1)

p.disconnect()
numpy.save("data//BackLegSensorValues.npy", backLegSensorValues)

