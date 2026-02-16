import pyrosim.pyrosim as pyrosim
import random


# define creation functions

# Creates world
def Create_World():

    pyrosim.Start_SDF("world.sdf")

    length = 1
    width = 1
    height = 1

    x = -5
    y = 0
    z = 0.5

    pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])

    pyrosim.End()


# creates the robots body
def Generate_Body():

    pyrosim.Start_URDF("body.urdf")

    # create Torso
    length = 1
    width = 1
    height = 1

    x = 0
    y = 0
    z = 1.5

    pyrosim.Send_Cube(name="Torso", pos=[x, y, z], size=[length, width, height])

    # joint Torso and BackLeg
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[-0.5,0,1])

    # create BackLeg
    length = 1
    width = 1
    height = 1

    x = -0.5
    y = 0
    z = -0.5

    pyrosim.Send_Cube(name="BackLeg", pos=[x, y, z], size=[length, width, height])

    # joint Torso FrontLeg
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0.5,0,1])

    # create FrontLEg
    length = 1
    width = 1
    height = 1

    x = 0.5
    y = 0
    z = -0.5

    pyrosim.Send_Cube(name="FrontLeg", pos=[x, y, z], size=[length, width, height])

    pyrosim.End()


# creates the robots neural network
def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")

    # adds sensor neurons to neural network file
    pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
    pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")

    # adds motor neurons to neural network file
    pyrosim.Send_Motor_Neuron(name = 3, jointName = "Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name = 4, jointName = "Torso_FrontLeg")

    # adds synapses
    for sensor in range(1, 3):

        for motor in range(3, 5):

            weight = 1 - (random.random() * 2)
            pyrosim.Send_Synapse(sourceNeuronName = sensor, targetNeuronName = motor, weight = weight)


    pyrosim.End()


# run generate code
if __name__ == "__main__":
    Create_World()
    Generate_Body()
    Generate_Brain()
