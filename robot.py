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

        # create palm touch sensors
        jointIndex = pyrosim.linkNamesToIndices["Q1"]
        self.palmTouchSensorQ1 = SENSOR(jointIndex)

        jointIndex = pyrosim.linkNamesToIndices["Q2"]
        self.palmTouchSensorQ2 = SENSOR(jointIndex)

        jointIndex = pyrosim.linkNamesToIndices["Q3"]
        self.palmTouchSensorQ3 = SENSOR(jointIndex)

        jointIndex = pyrosim.linkNamesToIndices["Q4"]
        self.palmTouchSensorQ4 = SENSOR(jointIndex)

        # create left fingure touch sensors
        jointIndex = pyrosim.linkNamesToIndices["L1"]
        self.fingureSensorL1 = SENSOR(jointIndex)

        jointIndex = pyrosim.linkNamesToIndices["L2"]
        self.fingureSensorL2 = SENSOR(jointIndex)

        # create rigth fingure touch sensors
        jointIndex = pyrosim.linkNamesToIndices["R1"]
        self.fingureSensorR1 = SENSOR(jointIndex)

        jointIndex = pyrosim.linkNamesToIndices["R2"]
        self.fingureSensorR2 = SENSOR(jointIndex)

        # create thumb touch sensors
        jointIndex = pyrosim.linkNamesToIndices["T1"]
        self.fingureSensorT1 = SENSOR(jointIndex)

        jointIndex = pyrosim.linkNamesToIndices["T2"]
        self.fingureSensorT2 = SENSOR(jointIndex)



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

        # gets palm touch values
        self.palmTouchSensorQ1.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.palmTouchSensorQ1.Get_Current_Value(i))
        self.palmTouchSensorQ2.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.palmTouchSensorQ2.Get_Current_Value(i))
        self.palmTouchSensorQ3.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.palmTouchSensorQ3.Get_Current_Value(i))
        self.palmTouchSensorQ4.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.palmTouchSensorQ4.Get_Current_Value(i))

        # gets left fingure touch values
        self.fingureSensorL1.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.fingureSensorL1.Get_Current_Value(i))
        self.fingureSensorL2.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.fingureSensorL2.Get_Current_Value(i))

        # get right fingure touch values
        self.fingureSensorR1.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.fingureSensorR1.Get_Current_Value(i))
        self.fingureSensorR2.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.fingureSensorR2.Get_Current_Value(i))

        # get thumb touch values
        self.fingureSensorT1.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.fingureSensorT1.Get_Current_Value(i))
        self.fingureSensorT2.Get_Is_Robot_Touching_Object(i, ballId, self.robotId)
        currentSensorValues.append(self.fingureSensorT2.Get_Current_Value(i))

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
    def Get_Fitness(self, connection, distanceToGoal, ballOnGround):

        '''
        # gets the x position or fitness of the robot
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)

        basePosition = basePositionAndOrientation[0]

        xPosition = basePosition[0]
        '''

        # gets balls hand touch values
        valuesQ1 = self.palmTouchSensorQ1.Get_Values()
        valuesQ2 = self.palmTouchSensorQ2.Get_Values()
        valuesQ3 = self.palmTouchSensorQ3.Get_Values()
        valuesQ4 = self.palmTouchSensorQ4.Get_Values()

        # get time left fingrue touch values
        valuesL1 = self.fingureSensorL1.Get_Values()
        valuesL2 = self.fingureSensorL2.Get_Values()

        # get touch values for right fingure
        valuesR1 = self.fingureSensorR1.Get_Values()
        valuesR2 = self.fingureSensorR2.Get_Values()

        # get touch values for the thumb
        valuesT1 = self.fingureSensorT1.Get_Values()
        valuesT2 = self.fingureSensorT2.Get_Values()

        # gets locations of palm
        palmPos = self.palmLocationSensor.Get_Values()

        timeInQ1 = 0
        timeInQ2 = 0
        timeInQ3 = 0
        timeInQ4 = 0

        whenBallTouchesHand = 0

        timeInL1 = 0
        timeInL2 = 0

        timeInR1 = 0
        timeInR2 = 0

        timeInT1 = 0
        timeInT2 = 0

        whenBallTouchesGround = c.NUM_SIM_STEPS
        groundTouched = False

        for i in range(c.NUM_SIM_STEPS):

            # sums time spent in each hand quadrent
            if valuesQ1[i] == 1.0:

                timeInQ1 += 1

            if valuesQ2[i] == 1.0:

                timeInQ2 += 1

            if valuesQ3[i] == 1.0:

                timeInQ3 += 1

            if valuesQ4[i] == 1.0:

                timeInQ4 += 1

            # sum time spent touching each part of left fingure
            if valuesL1[i] == 1.0:

                timeInL1 += 1

            if valuesL2[i] == 1.0:

                timeInL2 += 4

            # sum time spent touching right fingure
            if valuesR1[i] == 1.0:

                timeInR1 += 1

            if valuesR2[i] == 1.0:

                timeInR2 += 4

            # sum time spent touching right fingure
            if valuesT1[i] == 1.0:

                timeInT1 += 1

            if valuesT2[i] == 1.0:

                timeInT2 += 4

            # gets timestep the ball touches the ground at
            if (ballOnGround[i] == 1.0) and not(groundTouched):

                whenBallTouchesGround = i
                groundTouched = True

            # gets timestep ball touches hand
            if (whenBallTouchesHand == 0) and ((timeInQ1 + timeInQ2 + timeInQ3 + timeInQ4) > 0):

                whenBallTouchesHand = i


        # get fitness
        phase0 = whenBallTouchesHand
        phase1 = 0
        fitness = -9999999.9
        if whenBallTouchesGround < phase0:

            fitness = 0 - (np.abs(palmPos[0]) * np.abs(palmPos[1]) * np.abs(palmPos[2])) 

        elif whenBallTouchesGround >= phase0:

            fitness = ((timeInQ1 * timeInQ2 * timeInQ3 * timeInQ4) / 4) + \
                (timeInL1 * timeInL2) * (timeInR1 * timeInR2) * (timeInT1 * timeInT2)

        # use pipe to send fitness to parent program
        connection.send(fitness)
        connection.close()
