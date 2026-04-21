import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c
import random
import os
import time
from multiprocessing import Process, Pipe
from simulate import Run

class SOLUTION:

    def __init__(self, myID):

        #TODO: modify to include hidden neurons
        self.weightsSH = np.random.rand(c.NUM_SENSOR_NEURONS, c.NUM_HIDDEN_NEURONS) * 2 - 1
        self.weightsHM = np.random.rand(c.NUM_HIDDEN_NEURONS, c.NUM_MOTOR_NEURONS) * 2 - 1

        self.myID = myID

        self.process = None

        self.parent_connection, self.child_connection = Pipe()

        self.joints = []


    # sets ID for child solutions
    def Set_ID(self, myID):

        self.myID = myID


    # sets the pipes for the next process
    def Set_Pipes(self):

        self.parent_connection, self.child_connection = Pipe()


    # Creates world
    def Create_World(self):

        pyrosim.Start_SDF(f"world{self.myID}.sdf")

        length = 1
        width = 1
        height = 1

        x = 0
        y = 5
        z = 3

        mass = 0

        pyrosim.Send_Cube(name="target", pos=[x,y,z], size=[length,width,height], mass=mass)

        radius = 0.25

        x = 2.5
        y = 0
        z = 2

        mass = 50

        pyrosim.Send_Sphere(name="Ball", pos=[x,y,z], radius=radius, mass=mass)

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

        mass = 0

        pyrosim.Send_Cube(name="Body", pos=[x, y, z], size=[length, width, height], mass=mass)

        # ----- Upper Arm -----

        # joint Body and ShoulderSocket
        pyrosim.Send_Joint(name="Body_ShoulderSocket", parent="Body", child="ShoulderSocket", type="revolute", position=[0.5,0,0.5], jointAxis="1 0 0")
        self.joints.append("Body_ShoulderSocket")

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
        self.joints.append("ShoulderSocket_ShoulderBall")

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
        self.joints.append("ShoulderBall_UpperArm")

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
        self.joints.append("UpperArm_Elbow")

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
        self.joints.append("Elbow_Forearm")

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
        self.joints.append("Forarm_Wrist")

        # create Wrist
        length = 0.05
        width = 0.33
        height = 0.33

        x = 0.025
        y = 0
        z = 0

        pyrosim.Send_Cube(name="Wrist", pos=[x, y, z], size=[length, width, height])

        # joint Wrist and Palm
        pyrosim.Send_Joint(name="Wrist_Palm", parent="Wrist", child="Palm", type="revolute", position=[0.05,0,0.0825], jointAxis="0 0 1")
        self.joints.append("Wrist_Palm")

        # ----- Hand ----
        # create Palm
        length = 0.5
        width = 0.5
        height = 0.2

        x = 0.25
        y = 0
        z = 0

        pyrosim.Send_Cube(name="Palm", pos=[x, y, z], size=[length, width, height])

        # ----- Palm Sensor Pads -----

        pyrosim.Send_Joint(name="Palm_Q1", parent="Palm", child="Q1", type="fixed", position=[0.166,0.125,0], jointAxis="1 0 0")

        length = 0.2
        width = 0.2
        height = 0.05

        x = 0
        y = 0
        z = 0.08

        pyrosim.Send_Cube(name="Q1", pos=[x, y, z], size=[length, width, height])

        pyrosim.Send_Joint(name="Palm_Q2", parent="Palm", child="Q2", type="fixed", position=[0.333,0.125,0], jointAxis="1 0 0")

        length = 0.2
        width = 0.2
        height = 0.05

        x = 0
        y = 0
        z = 0.08

        pyrosim.Send_Cube(name="Q2", pos=[x, y, z], size=[length, width, height])

        pyrosim.Send_Joint(name="Palm_Q3", parent="Palm", child="Q3", type="fixed", position=[0.166,-0.125,0], jointAxis="1 0 0")

        length = 0.2
        width = 0.2
        height = 0.05

        x = 0
        y = 0
        z = 0.08

        pyrosim.Send_Cube(name="Q3", pos=[x, y, z], size=[length, width, height])

        pyrosim.Send_Joint(name="Palm_Q4", parent="Palm", child="Q4", type="fixed", position=[0.333,-0.125,0], jointAxis="1 0 0")

        length = 0.2
        width = 0.2
        height = 0.05

        x = 0
        y = 0
        z = 0.08

        pyrosim.Send_Cube(name="Q4", pos=[x, y, z], size=[length, width, height])

        # ----- Left Fingure -----
        # joint Palm and LeftFingureBase
        pyrosim.Send_Joint(name="Palm_LeftFingureBase", parent="Palm", child="LeftFingureBase", type="revolute", position=[0.4,0.2,0.1], jointAxis="0 1 0")
        self.joints.append("Palm_LeftFingureBase")

        # create LeftFingureBase
        length = 0.25
        width = 0.25
        height = 0.1

        x = length / 2
        y = 0
        z = -0.05

        pyrosim.Send_Cube(name="LeftFingureBase", pos=[x, y, z], size=[length, width, height])

        pyrosim.Send_Joint(name="LeftFingureBase_L1", parent="LeftFingureBase", child="L1", type="fixed", position=[0.125,0,0], jointAxis="0 1 0")
 
        length = 0.225
        width = 0.225
        height = 0.05

        x = 0
        y = 0
        z = -0.01

        pyrosim.Send_Cube(name="L1", pos=[x, y, z], size=[length, width, height])

        # joint LeftFingureBase and LeftFingureTip
        pyrosim.Send_Joint(name="LeftFingureBase_LeftFingureTip", parent="LeftFingureBase", child="LeftFingureTip", type="revolute", position=[0.25,-0.05,0], jointAxis="0 1 0")
        self.joints.append("LeftFingureBase_LeftFingureTip")

        # create LeftFingure
        length = 0.25
        width = 0.2
        height = 0.1

        x = length / 2
        y = 0
        z = -0.05

        pyrosim.Send_Cube(name="LeftFingureTip", pos=[x, y, z], size=[length, width, height])

        pyrosim.Send_Joint(name="LeftFingureTip_L2", parent="LeftFingureTip", child="L2", type="fixed", position=[0.125,0,0], jointAxis="0 1 0")
 
        length = 0.225
        width = 0.18
        height = 0.05

        x = 0
        y = 0
        z = -0.01

        pyrosim.Send_Cube(name="L2", pos=[x, y, z], size=[length, width, height])

        # ----- Right Fingure -----
        # joint Palm and LeftFingureBase
        pyrosim.Send_Joint(name="Palm_RightFingureBase", parent="Palm", child="RightFingureBase", type="revolute", position=[0.4,-0.2,0.1], jointAxis="0 1 0")
        self.joints.append("Palm_RightFingureBase")

        # create LeftFingureBase
        length = 0.25
        width = 0.25
        height = 0.1

        x = length / 2
        y = 0
        z = -0.05

        pyrosim.Send_Cube(name="RightFingureBase", pos=[x, y, z], size=[length, width, height])

        pyrosim.Send_Joint(name="RightFingureBase_R1", parent="RightFingureBase", child="R1", type="fixed", position=[0.125,0,0], jointAxis="0 1 0")
 
        length = 0.225
        width = 0.225
        height = 0.05

        x = 0
        y = 0
        z = -0.01

        pyrosim.Send_Cube(name="R1", pos=[x, y, z], size=[length, width, height])


        # joint RightFingureBase and RightFingureTip
        pyrosim.Send_Joint(name="RightFingureBase_RightFingureTip", parent="RightFingureBase", child="RightFingureTip", type="revolute", position=[0.25,0.05,0], jointAxis="0 1 0")
        self.joints.append("RightFingureBase_RightFingureTip")

        # create LeftFingure
        length = 0.25
        width = 0.2
        height = 0.1

        x = length / 2
        y = 0
        z = -0.05

        pyrosim.Send_Cube(name="RightFingureTip", pos=[x, y, z], size=[length, width, height])

        pyrosim.Send_Joint(name="RightFingureTip_R2", parent="RightFingureTip", child="R2", type="fixed", position=[0.125,0,0], jointAxis="0 1 0")
 
        liength = 0.225
        width = 0.18
        height = 0.05

        x = 0
        y = 0
        z = -0.01

        pyrosim.Send_Cube(name="R2", pos=[x, y, z], size=[length, width, height])

        # ----- Thumb -----
        # joint Palm and Thumb Base
        pyrosim.Send_Joint(name="Palm_ThumbBase", parent="Palm", child="ThumbBase", type="revolute", position=[0.1,0,0.1], jointAxis="0 1 0")
        self.joints.append("Palm_ThumbBase")

        # create LeftFingureBase
        length = 0.3
        width = 0.3
        height = 0.1

        x = -(length / 2)
        y = 0
        z = -0.05

        pyrosim.Send_Cube(name="ThumbBase", pos=[x, y, z], size=[length, width, height])

        pyrosim.Send_Joint(name="ThumbBase_T1", parent="ThumbBase", child="T1", type="fixed", position=[-0.15,0,0], jointAxis="0 1 0")
 
        length = 0.28
        width = 0.28
        height = 0.05

        x = 0
        y = 0
        z = -0.01

        pyrosim.Send_Cube(name="T1", pos=[x, y, z], size=[length, width, height])

        # joint LeftFingureBase and LeftFingureTip
        pyrosim.Send_Joint(name="ThumbBase_ThumbTip", parent="ThumbBase", child="ThumbTip", type="revolute", position=[-0.3,0.,0], jointAxis="0 1 0")
        self.joints.append("ThumbBase_ThumbTip")

        # create LeftFingure
        length = 0.2
        width = 0.2
        height = 0.1

        x = -(length / 2)
        y = 0
        z = -0.05

        pyrosim.Send_Cube(name="ThumbTip", pos=[x, y, z], size=[length, width, height])

        pyrosim.Send_Joint(name="ThumbTip_T2", parent="ThumbTip", child="T2", type="fixed", position=[-0.1,0,0], jointAxis="0 1 0")
 
        length = 0.18
        width = 0.18
        height = 0.05

        x = 0
        y = 0
        z = -0.01

        pyrosim.Send_Cube(name="T2", pos=[x, y, z], size=[length, width, height])

        pyrosim.End()


    # creates the robots neural network
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        # creates the hidden neurons
        neuronIndex = 0
        for i in range(c.NUM_SENSOR_NEURONS):

            pyrosim.Send_Sensor_Neuron(name = neuronIndex, linkName = f"neuronIndex")
            neuronIndex = neuronIndex + 1

        # creates the hidden neurons
        for i in range(c.NUM_HIDDEN_NEURONS):

            pyrosim.Send_Hidden_Neuron(name = neuronIndex)
            neuronIndex = neuronIndex + 1

        # creates the motor neurons
        for i in range(c.NUM_MOTOR_NEURONS):

            pyrosim.Send_Motor_Neuron(name = neuronIndex, jointName = self.joints[i])
            neuronIndex = neuronIndex + 1

        for currentRow in range(c.NUM_SENSOR_NEURONS):

            for currentColumn in range(c.NUM_HIDDEN_NEURONS):

                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + c.NUM_SENSOR_NEURONS, weight=self.weightsSH[currentRow][currentColumn], type="regular")

        for currentRow in range(c.NUM_HIDDEN_NEURONS):

            for currentColumn in range(c.NUM_MOTOR_NEURONS):

                pyrosim.Send_Synapse(sourceNeuronName = currentRow + c.NUM_SENSOR_NEURONS, targetNeuronName = currentColumn + c.NUM_SENSOR_NEURONS + c.NUM_HIDDEN_NEURONS, weight=self.weightsHM[currentRow][currentColumn], type="regular")

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

        neuronSet = random.random() < 0.5

        if neuronSet:

            randomRow = random.randint(0, c.NUM_SENSOR_NEURONS - 1)
            randomColumn = random.randint(0, c.NUM_HIDDEN_NEURONS - 1)
            self.weightsSH[randomRow][randomColumn] = random.random() * 2 - 1

        else:

            randomRow = random.randint(0, c.NUM_HIDDEN_NEURONS - 1)
            randomColumn = random.randint(0, c.NUM_MOTOR_NEURONS - 1)
            self.weightsHM[randomRow][randomColumn] = random.random() * 2 - 1



    # gets x, y and theta of fingures put on a unit circle from center of previous link
    def Get_Fingure_Pos(self, radius, unitTheta):

        # calculate x and y
        x = radius + (radius * np.cos(unitTheta))
        y = radius * np.sin(unitTheta)

        '''
        a = radius
        c = radius
        b = np.sqrt(np.square(x) + np.square(y))

        theta = np.sqrt(np.square(a) + np.square(b) - (2 * a * b * np.cos(c)))
        '''

        return [x, y]
