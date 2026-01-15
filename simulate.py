import pybullet as p
import time

pyhsicsClient = p.connect(p.GUI)

# comment out to enable debugger in pybullet simulation
# p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

for i in range(1000):
    print(i)
    p.stepSimulation()
    time.sleep(0.1)

p.disconnect()

