import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR
import constants as c
import os

class ROBOT:

    # class constructor
    def __init__(self, solutionID):

        # loads robot from body.urdf
        self.robotId = p.loadURDF(f"body{solutionID}.urdf")

        # load neural network from brain.nndf
        self.myID = solutionID
        self.nn = NEURAL_NETWORK(f"brain{self.myID}.nndf")

        # prepares to simulate robot
        pyrosim.Prepare_To_Simulate(self.robotId)

        # prepare sensors for links
        self.Prepare_To_Sense()

        # prepares motors to move
        self.Prepare_To_Act()

        # cleans up brain files
        os.system(f"rm brain{self.myID}.nndf")
        os.system(f"rm body{self.myID}.urdf")


    # prepares sensors for every link
    def Prepare_To_Sense(self):

        # initilizes joint angle sensors
        self.jointSensors = {}

        for joint in pyrosim.jointNamesToIndices:

            self.jointSensors[joint] = SENSOR(joint)

        self.palmLocationSensor = SENSOR("Palm")

        jointIndex = pyrosim.linkNamesToIndices["Q1"]
        self.palmTouchSensorQ1 = SENSOR(jointIndex)

        jointIndex = pyrosim.linkNamesToIndices["Q2"]
        self.palmTouchSensorQ2 = SENSOR(jointIndex)

        jointIndex = pyrosim.linkNamesToIndices["Q3"]
        self.palmTouchSensorQ3 = SENSOR(jointIndex)

        jointIndex = pyrosim.linkNamesToIndices["Q4"]
        self.palmTouchSensorQ4 = SENSOR(jointIndex)


    # get and store sensor data for robot object
    def Sense(self, i, ballId):

        currentSensorValues = []

        for sensor in self.jointSensors.values():

            sensor.Get_Joint_Angle(i, self.robotId)
            currentSensorValues.append(sensor.Get_Current_Value(i))

        self.palmLocationSensor.Get_Link_Position(i, self.robotId)
        pos = self.palmLocationSensor.Get_Current_Value(i)
        currentSensorValues.append(pos[0])
        currentSensorValues.append(pos[1])
        currentSensorValues.append(pos[2])

        self.palmTouchSensorQ1.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.palmTouchSensorQ1.Get_Current_Value(i))
        self.palmTouchSensorQ2.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.palmTouchSensorQ2.Get_Current_Value(i))
        self.palmTouchSensorQ3.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.palmTouchSensorQ3.Get_Current_Value(i))
        self.palmTouchSensorQ4.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.palmTouchSensorQ4.Get_Current_Value(i))

        return currentSensorValues


    # prepare motors at each joint
    def Prepare_To_Act(self):

        self.motors = {}

        for jointName in pyrosim.jointNamesToIndices:

            self.motors[jointName] = MOTOR(jointName)


    # updates each motor
    def Act(self, i):

        for neuronName in self.nn.Get_Neuron_Names():

            if self.nn.Is_Motor_Neuron(neuronName):

                # gets motor neurons output value and correct motor
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.MOTOR_JOINT_RANGE

                # updates motor neurons
                self.motors[jointName.encode()].Set_Value(desiredAngle, self.robotId)


    # activates neural network to interpret sensor input and update robot
    def Think(self, sensorValues):

        self.nn.Update(sensorValues)

        if (c.SHOW_NN_UPDATES):

            self.nn.Print()


    # gets the fitness of the robot
    def Get_Fitness(self, connection, distanceToGoal):

        '''
        # gets the x position or fitness of the robot
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)

        basePosition = basePositionAndOrientation[0]

        xPosition = basePosition[0]
        '''

        # use pipe to send fitness to parent program
        connection.send(distanceToGoal)
        connection.close()
