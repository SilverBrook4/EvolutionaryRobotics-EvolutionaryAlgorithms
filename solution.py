import pyrosim.pyrosim as pyrosim
print(pyrosim.__file__)
import inspect
print(inspect.getsource(pyrosim.Send_Sphere))
import numpy as np
import constants as c
import random
import os
import time
from multiprocessing import Process, Pipe
from simulate import Run

class SOLUTION:

    def __init__(self, myID):

        self.weights = np.random.rand(c.NUM_SENSOR_NEURONS, c.NUM_MOTOR_NEURONS) * 2 - 1

        self.myID = myID

        self.process = None

        self.parent_connection, self.child_connection = Pipe()


    # sets ID for child solutions
    def Set_ID(self, myID):

        self.myID = myID


    # sets the pipes for the next process
    def Set_Pipes(self):

        self.parent_connection, self.child_connection = Pipe()


    # Creates world
    def Create_World(self):

        pyrosim.Start_SDF(f"world{self.myID}.sdf")

        radius = 0.5

        x = -5
        y = 5
        z = 0.5

        pyrosim.Send_Sphere(name="Ball", pos=[x, y, z], radius=radius)

        pyrosim.End()


    # creates the robots body
    def Create_Body(self):

        pyrosim.Start_URDF(f"body{self.myID}.urdf")

        # create Body
        length = 1
        width = 1
        height = 1

        x = 0
        y = 0
        z = 0.5

        pyrosim.Send_Cube(name="Body", pos=[x, y, z], size=[length, width, height])

        # ----- Upper Arm -----

        # joint Body and ShoulderSocket
        pyrosim.Send_Joint(name="Body_ShoulderSocket", parent="Body", child="ShoulderSocket", type="revolute", position=[0.5,0,0.5], jointAxis="1 0 0")

        # create ShoulderSocket
        length = 0.1
        width = 0.33
        height = 0.33

        x = 0.05
        y = 0
        z = 0

        pyrosim.Send_Cube(name="ShoulderSocket", pos=[x, y, z], size=[length, width, height])

        # joint ShoulderSocket and ShoulderBall
        pyrosim.Send_Joint(name="ShoulderSocket_ShoulderBall", parent="ShoulderSocket", child="ShoulderBall", type="revolute", position=[0.1,0,0], jointAxis="0 1 0")


        # create ShoulderBall
        length = 0.1
        width = 0.33
        height = 0.33

        x = 0.05
        y = 0
        z = 0

        pyrosim.Send_Cube(name="ShoulderBall", pos=[x, y, z], size=[length, width, height])

        # joint ShoulderBall and UpperArm
        pyrosim.Send_Joint(name="ShoulderBall_UpperArm", parent="ShoulderBall", child="UpperArm", type="revolute", position=[0.1,0,0], jointAxis="0 0 1")


        # create ShoulderBall
        length = 0.8
        width = 0.33
        height = 0.33

        x = 0.4
        y = 0
        z = 0

        pyrosim.Send_Cube(name="UpperArm", pos=[x, y, z], size=[length, width, height])

        # ----- Forarm -----

        # joint UpperArm and Elbow
        pyrosim.Send_Joint(name="UpperArm_Elbow", parent="UpperArm", child="Elbow", type="revolute", position=[0.8,0,0], jointAxis="0 0 1")

        # create Elbow
        length = 0.1
        width = 0.33
        height = 0.33

        x = 0.05
        y = 0
        z = 0

        pyrosim.Send_Cube(name="Elbow", pos=[x, y, z], size=[length, width, height])

        # joint Elbow and Forearm
        pyrosim.Send_Joint(name="Elbow_Forearm", parent="Elbow", child="Forearm", type="revolute", position=[0.1,0,0], jointAxis="1 0 0")

        # create Forearm
        length = 0.6
        width = 0.33
        height = 0.33

        x = 0.3
        y = 0
        z = 0

        pyrosim.Send_Cube(name="Forearm", pos=[x, y, z], size=[length, width, height])

        # ----- Wrist -----

        # joint Forearm and Wrist
        pyrosim.Send_Joint(name="Forarm_Wrist", parent="Forearm", child="Wrist", type="revolute", position=[0.6,0,0], jointAxis="0 1 0")

        # create Wrist
        length = 0.05
        width = 0.33
        height = 0.33

        x = 0.025
        y = 0
        z = 0

        pyrosim.Send_Cube(name="Wrist", pos=[x, y, z], size=[length, width, height])

        # joint Wrist and Palm
        pyrosim.Send_Joint(name="Wrist_Palm", parent="Wrist", child="Palm", type="revolute", position=[0.05,0,0], jointAxis="0 0 1")

        # TODO: Finish Hand
        # ----- Hand ----
        # create Palm
        length = 0.5
        width = 0.5
        height = 0.2

        x = 0.25
        y = 0
        z = 0

        pyrosim.Send_Cube(name="Palm", pos=[x, y, z], size=[length, width, height])




        '''
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

        '''

        pyrosim.End()


    # creates the robots neural network
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        '''
        # adds sensor neurons to neural network file
        pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")

        pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 3, linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 4, linkName = "RightLowerLeg")

        pyrosim.Send_Hidden_Neuron(name = 5)
        pyrosim.Send_Hidden_Neuron(name = 6)
        pyrosim.Send_Hidden_Neuron(name = 7)

        # adds motor neurons to neural network file
        pyrosim.Send_Motor_Neuron(name = 8, jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 9, jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name = 10, jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name = 11, jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name = 12, jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 13, jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 14, jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 15, jointName = "RightLeg_RightLowerLeg")


        # adds synapses from sensor to hidden
        for currentRow in range(c.NUM_SENSOR_NEURONS):

            for currentColumn in range(c.NUM_HIDDEN_NEURONS):

                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + c.NUM_SENSOR_NEURONS, weight = self.weights[currentRow][currentColumn], type = "regular")

        # add recurrent synapses
        for currentRow in range(c.NUM_HIDDEN_NEURONS):

            for currentColumn in range(c.NUM_HIDDEN_NEURONS):


                pyrosim.Send_Synapse(sourceNeuronName = currentRow + c.NUM_SENSOR_NEURONS, targetNeuronName = currentColumn + c.NUM_SENSOR_NEURONS, weight = self.weights[currentRow][currentColumn], type = "recurrent")



        # add synapses for hidden to motor
        for currentRow in range(c.NUM_HIDDEN_NEURONS):

            for currentColumn in range(c.NUM_MOTOR_NEURONS):

                pyrosim.Send_Synapse(sourceNeuronName = currentRow + c.NUM_SENSOR_NEURONS, targetNeuronName = currentColumn + c.NUM_SENSOR_NEURONS + c.NUM_HIDDEN_NEURONS, weight = self.weights[currentRow][currentColumn], type = "regular")

        '''
        pyrosim.End()


    # staerts simulation
    def Start_Simulation(self, directOrGUI):

        # creates the files for the world, robot, and robots brain to run in the physics engine
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        # TODO: write output to a file or supress
        # runs simulate.py
        self.process = Process(target=Run, args=(directOrGUI, self.myID, self.child_connection, c.SUPPRESS_PYBULLET_MESSAGES))
        self.process.start()
        # os.system(f"python3 simulate.py {directOrGUI} {self.myID} {str(self.writePipe)} 2&>1 &")
        # os.system(f"python3 simulate.py {directOrGUI} {self.myID} &")



    # reads in fitness value
    def Wait_For_Simulation_To_End(self):

        # gets fitness from subprocess and then wait to close
        self.fitness = float(self.parent_connection.recv())
        self.process.join()


    def Mutate(self):

        randomRow = random.randint(0, c.NUM_SENSOR_NEURONS - 1)
        randomColumn = random.randint(0, c.NUM_MOTOR_NEURONS - 1)

        self.weights[randomRow][randomColumn] = random.random() * 2 - 1
