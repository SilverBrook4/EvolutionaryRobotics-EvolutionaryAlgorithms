import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import os
import time


class SOLUTION:

    def __init__(self, myID):

        self.weights = 1 - (np.random.rand(3, 2) * 2)

        self.myID = myID


    # sets ID for child solutions
    def Set_ID(self, myID):

        self.myID = myID


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
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

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


    # staerts simulation
    def Start_Simulation(self, directOrGUI):

        # creates the files for the world, robot, and robots brain to run in the physics engine
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        # runs the simulation
        os.system(f"python3 simulate.py {directOrGUI} {self.myID} &")


    # reads in fitness value
    def Wait_For_Simulation_To_End(self):

        # checks that fitness file exists before opening
        while not os.path.exists(f"data//fitness{self.myID}.txt"):

            time.sleep(0.01)

        # read in fitness value for iteration
        with open(f"data//fitness{self.myID}.txt", "r") as f:

            self.fitness = float(f.read())

            f.close()

        # cleans up fitness file
        os.system(f"rm data//fitness{self.myID}.txt")


    def Mutate(self):

        randomRow = random.randint(0, 2)
        randomColumn = random.randint(0, 1)

        self.weights[randomRow][randomColumn] = 1 - (random.random() * 2)
