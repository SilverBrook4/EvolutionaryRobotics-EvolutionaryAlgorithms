import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c
import random
import os
import time
import subprocess


class SOLUTION:

    def __init__(self, myID):

        self.weights = 1 - (np.random.rand(c.NUM_SENSOR_NEURONS, c.NUM_MOTOR_NEURONS) * 2)

        self.myID = myID

        self.readPipe, self.writePipe = os.pipe()


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
        y = 5
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
        z = 1

        pyrosim.Send_Cube(name="Torso", pos=[x, y, z], size=[length, width, height])

        # ----- Upper Legs ----

        # joint Torso and BackLeg
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0,-0.5,1], jointAxis="1 0 0")

        # create BackLeg
        length = 0.2
        width = 1
        height = 0.2

        x = 0
        y = -0.5
        z = 0

        pyrosim.Send_Cube(name="BackLeg", pos=[x, y, z], size=[length, width, height])

        # joint Torso and FrontLeg
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0,0.5,1], jointAxis="1 0 0")

        # create FrontLeg
        length = 0.2
        width = 1
        height = 0.2

        x = 0
        y = 0.5
        z = 0

        pyrosim.Send_Cube(name="FrontLeg", pos=[x, y, z], size=[length, width, height])

        # joint Torso and LeftLeg 
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[-0.5, 0, 1], jointAxis="0 1 0")

        # create LeftLeg
        length = 1
        width = 0.2
        height = 0.2

        x = -0.5
        y = 0
        z = 0

        pyrosim.Send_Cube(name="LeftLeg", pos=[x, y, z], size=[length, width, height])

        # joint Torso and RightLeg 
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[0.5, 0, 1], jointAxis="0 1 0")

        # create RightLeg
        length = 1
        width = 0.2
        height = 0.2

        x = 0.5
        y = 0
        z = 0

        pyrosim.Send_Cube(name="RightLeg", pos=[x, y, z], size=[length, width, height])

        # ----- Lower Legs -----

        # joint FrontLeg and FrontLowerLeg 
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0, 1, 0], jointAxis="1 0 0")

        # create FrontLowerLeg
        length = 0.2
        width = 0.2
        height = 1

        x = 0
        y = 0
        z = -0.5

        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[x, y, z], size=[length, width, height])

        # joint BackLeg BackLowerLeg
        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute", position=[0, -1, 0], jointAxis="1 0 0")

        # create BackLeg
        length = 0.2
        width = 0.2
        height = 1

        x = 0
        y = 0
        z = -0.5

        pyrosim.Send_Cube(name="BackLowerLeg", pos=[x, y, z], size=[length, width, height])

        # joint LeftLeg and LeftLowerLeg
        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute", position=[-1, 0, 0], jointAxis="0 1 0")

        # create LeftLowerLeg
        length = 0.2
        width = 0.2
        height = 1

        x = 0
        y = 0
        z = -0.5

        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[x, y, z], size=[length, width, height])

        # joint RightLeg and RightLowerLeg
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position=[1, 0, 0], jointAxis="0 1 0")

        # create RightLowerLeg
        length = 0.2
        width = 0.2
        height = 1

        x = 0
        y = 0
        z = -0.5

        pyrosim.Send_Cube(name="RightLowerLeg", pos=[x, y, z], size=[length, width, height])

        pyrosim.End()


    # creates the robots neural network
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        # adds sensor neurons to neural network file
        pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")
        '''
        pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 3, linkName = "LeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 4, linkName = "RightLeg")
        '''
        pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 3, linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 4, linkName = "RightLowerLeg")

        # adds motor neurons to neural network file
        pyrosim.Send_Motor_Neuron(name = 5, jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 6, jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name = 7, jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name = 8, jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name = 9, jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 10, jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 11, jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 12, jointName = "RightLeg_RightLowerLeg")


        # adds synapses
        for currentRow in range(c.NUM_SENSOR_NEURONS):

            for currentColumn in range(c.NUM_MOTOR_NEURONS):

                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + c.NUM_SENSOR_NEURONS, weight = self.weights[currentRow][currentColumn])


        pyrosim.End()


    # staerts simulation
    def Start_Simulation(self, directOrGUI):

        # creates the files for the world, robot, and robots brain to run in the physics engine
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        # runs the simulation
        if (c.SUPPRESS_PYBULLET_MESSAGES):

            subprocess.Popen(["python3", "simulate.py", directOrGUI, str(self.myID), str(self.writePipe)],
                             pass_fds=(self.writePipe,),
                             stderr=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL)
            # os.system(f"python3 simulate.py {directOrGUI} {self.myID} {str(self.writePipe)} 2&>1 &")

        else:

            subprocess.Popen(["python3", "simulate.py", directOrGUI, str(self.myID), str(self.writePipe)],
                             pass_fds=(self.writePipe,))
            # os.system(f"python3 simulate.py {directOrGUI} {self.myID} &")



    # reads in fitness value
    def Wait_For_Simulation_To_End(self):

        os.close(self.writePipe)
        self.fitness = float(os.read(self.readPipe, 100))
        os.close(self.readPipe)

        '''
        # checks that fitness file exists before opening
        print(f"searching for data//tmp{self.myID}.txt")
        while not os.path.exists(f"data//fitness{self.myID}.txt")

            time.sleep(0.01)

        # read in fitness value for iteration
        with open(f"data//fitness{self.myID}.txt", "r") as f:

            self.fitness = float(f.read())

            f.close()

        # cleans up fitness file
        os.system(f"rm data//fitness{self.myID}.txt")
        '''


    def Mutate(self):

        randomRow = random.randint(0, c.NUM_SENSOR_NEURONS - 1)
        randomColumn = random.randint(0, c.NUM_MOTOR_NEURONS - 1)

        self.weights[randomRow][randomColumn] = 1 - (random.random() * 2)
