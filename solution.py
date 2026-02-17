import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import os


class SOLUTION:

    def __init__(self):

        self.weights = 1 - (np.random.rand(3, 2) * 2)


    # Creates world
    def Create_World(self):

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
    def Create_Body(self):

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
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")

        # adds sensor neurons to neural network file
        pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")

        # adds motor neurons to neural network file
        pyrosim.Send_Motor_Neuron(name = 3, jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 4, jointName = "Torso_FrontLeg")

        # adds synapses
        for currentRow in range(3):

            for currentColumn in range(2):

                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + 3, weight = self.weights[currentRow][currentColumn])


        pyrosim.End()


    # evaluates the qualety of given solution
    def Evaluate(self):

        # creates the files for the world, robot, and robots brain to run in the physics engine
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        # runs the simulation
        os.system("python3 simulate.py")

        # read in fitness value for iteration
        with open("data//fitness.txt", "r") as f:

            self.fitness = float(f.read())

            f.close()


    def Mutate(self):

        randomRow = random.randint(0, 2)
        randomColumn = random.randint(0, 1)

        self.weights[randomRow][randomColumn] = 1 - (random.random() * 2)
