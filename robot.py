import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR
import constants as c
import numpy as np
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

        # TODO: create sensors to sense if hand is touching ground
        self.armToGroundSensors = {}
        for link in pyrosim.linkNamesToIndices:

            linkIndex = pyrosim.linkNamesToIndices[link]

            if linkIndex >= 0:

                self.armToGroundSensors[linkIndex] = SENSOR(linkIndex)


    # get and store sensor data for robot object
    def Sense(self, i, ballId, floorId):

        currentSensorValues = []

        for sensor in self.jointSensors.values():

            sensor.Get_Joint_Angle(i, self.robotId)

            if c.INCLUDE_JOINT_SENSORS:

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

        # sense if any link has touched ground
        for sensor in self.armToGroundSensors.values():

            sensor.Get_Is_Robot_Touching_Object(i, floorId, self.robotId)

        return currentSensorValues



    # prepare motors at each joint
    def Prepare_To_Act(self):

        self.motors = {}

        for jointName in pyrosim.jointNamesToIndices:

            joint = jointName.decode("UTF-8")
            if joint == "Palm_LeftRotator" or joint == "Palm_RightRotator" or joint == "Palm_ThumbRotator":

                self.motors[jointName] = MOTOR(jointName, c.FINGURE_ROTATOR_JOINT_RANGE)

            elif joint == "Writst_Palm":

                self.motors[jointName] = MOTOR(jointName, c.WRIST_SHIFT_JOINT_RANGE)

            else:

                self.motors[jointName] = MOTOR(jointName)


    # updates each motor
    def Act(self, i):

        for neuronName in self.nn.Get_Neuron_Names():

            if self.nn.Is_Motor_Neuron(neuronName):

                # gets motor neurons output value and correct motor
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                jointRange = self.motors[jointName.encode()].Get_Joint_Range()
                desiredAngle = self.nn.Get_Value_Of(neuronName) * jointRange

                # updates motor neurons
                self.motors[jointName.encode()].Set_Value(desiredAngle, self.robotId)


    # activates neural network to interpret sensor input and update robot
    def Think(self, sensorValues):

        self.nn.Update(sensorValues)

        if (c.SHOW_NN_UPDATES):

            self.nn.Print()


    # gets the fitness of the robot
    def Get_Fitness(self, connection, distanceToGoal, ballOnGround, ballPos):

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

        fingureJoints = ["LeftRotator_LeftFingureBase".encode(),
        "LeftFingureBase_LeftFingureTip".encode(),
        "RightRotator_RightFingureBase".encode(),
        "RightFingureBase_RightFingureTip".encode(),
        "ThumbRotator_ThumbBase".encode(),
        "ThumbBase_ThumbTip".encode()]

        timeInQ1 = 0
        timeInQ2 = 0
        timeInQ3 = 0
        timeInQ4 = 0

        whenBallTouchesHand = c.NUM_SIM_STEPS - 1
        touchedHand = False

        timeInL1 = 0
        timeInL2 = 0
        timeInL = 0
        contactL = False

        timeInR1 = 0
        timeInR2 = 0
        timeInR = 0
        contactR = False

        timeInT1 = 0
        timeInT2 = 0
        timeInT = 0
        contactT = False

        fullContact = False

        whenBallTouchesGround = c.NUM_SIM_STEPS
        groundTouched = False

        timeTouchingGround = 1

        negativeRotation = 0
        positiveRotation = 0

        preContactFingureMovement = 0

        closingMotion = 0

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

            # checks if fingures are tocuhing ball at same time
            if valuesL1[i] == 1.0 and valuesL2[i] == 1.0:

                timeInL += 1
                contactL = True

            if valuesR1[i] == 1.0 and valuesR2[i] == 1.0:

                timeInR += 1
                contactR = True

            if valuesT1[i] == 1.0 and valuesT2[i] == 1.0:

                timeInT += 1
                contactT = True


            # gets timestep the ball touches the ground at
            if (ballOnGround[i] == 1.0) and not(groundTouched):

                whenBallTouchesGround = i
                groundTouched = True

            # gets timestep ball touches hand
            if not(touchedHand) and ((timeInQ1 + timeInQ2 + timeInQ3 + timeInQ4) > 0):

                whenBallTouchesHand = i
                touchedHand = True

            if touchedHand and i > whenBallTouchesHand:

                for joint in fingureJoints:

                    current = self.jointSensors[joint].Get_Current_Value(i)
                    previous = self.jointSensors[joint].Get_Current_Value(i - 1)
                    delta = current - previous

                    if delta > 0:

                        closingMotion += delta

                    else:

                        negativeRotation += 1

            for sensor in self.armToGroundSensors.values():

                if sensor.Get_Current_Value(i) == 1.0:

                    timeTouchingGround += 1

            '''
            # TODO: count when joints are negativly rotated
            if self.jointSensors["LeftRotator_LeftFingureBase".encode()].Get_Current_Value(i) < 0:

                if touchedHand:

                    negativeRotation += 1

            else:

                if touchedHand:

                    positiveRotation += 1

            if self.jointSensors["LeftFingureBase_LeftFingureTip".encode()].Get_Current_Value(i) < 0:

                if touchedHand:

                    negativeRotation += 1

            else:

               if touchedHand:

                    positiveRotation += 1

            if self.jointSensors["RightRotator_RightFingureBase".encode()].Get_Current_Value(i) < 0:

                if touchedHand:

                    negativeRotation += 1

            else:

               if touchedHand:

                    positiveRotation += 1

            if self.jointSensors["RightFingureBase_RightFingureTip".encode()].Get_Current_Value(i) < 0:

                if touchedHand:

                    negativeRotation += 1

            else:

               if touchedHand:

                    positiveRotation += 1

            if self.jointSensors["ThumbRotator_ThumbBase".encode()].Get_Current_Value(i) < 0:

                if touchedHand:

                    negativeRotation += 1

            else:

               if touchedHand:

                    positiveRotation += 1

            if self.jointSensors["ThumbBase_ThumbTip".encode()].Get_Current_Value(i) < 0:

                if touchedHand:

                    negativeRotation += 1

            else:

               if touchedHand:

                    positiveRotation += 1
            '''

        fullContact = contactL and contactR and contactT

        leftBaseShift = abs(self.jointSensors["LeftRotator_LeftFingureBase".encode()].Get_Current_Value(whenBallTouchesHand) - self.jointSensors["LeftRotator_LeftFingureBase".encode()].Get_Current_Value(0))
        leftTipShift = abs(self.jointSensors["LeftFingureBase_LeftFingureTip".encode()].Get_Current_Value(whenBallTouchesHand) - self.jointSensors["LeftFingureBase_LeftFingureTip".encode()].Get_Current_Value(0))
        rightBaseShift = abs(self.jointSensors["RightRotator_RightFingureBase".encode()].Get_Current_Value(whenBallTouchesHand) - self.jointSensors["RightRotator_RightFingureBase".encode()].Get_Current_Value(0))
        rightTipShift = abs(self.jointSensors["RightFingureBase_RightFingureTip".encode()].Get_Current_Value(whenBallTouchesHand) - self.jointSensors["RightFingureBase_RightFingureTip".encode()].Get_Current_Value(0))
        thumbBaseShift = abs(self.jointSensors["ThumbRotator_ThumbBase".encode()].Get_Current_Value(whenBallTouchesHand) - self.jointSensors["ThumbRotator_ThumbBase".encode()].Get_Current_Value(0))
        thumbTipShift = abs(self.jointSensors["ThumbBase_ThumbTip".encode()].Get_Current_Value(whenBallTouchesHand) - self.jointSensors["ThumbBase_ThumbTip".encode()].Get_Current_Value(0))



        phase0 = whenBallTouchesHand
        phase1 = 0
        fitness = -9999999.9
        if whenBallTouchesGround < whenBallTouchesHand:

            print("phase 0")
            preContactShiftPenalty = (leftTipShift + leftBaseShift + rightBaseShift + rightTipShift + thumbBaseShift + thumbTipShift) * 0.01
            handStability = 1.0 / (1.0 + np.linalg.norm(np.array(palmPos[whenBallTouchesHand]) - np.array(palmPos[0])))
            proximity = (1.0 / (np.linalg.norm(np.array(palmPos) - np.array(ballPos)) + 1.0))


            fitness = (handStability * proximity) / timeTouchingGround - preContactShiftPenalty
            #fitness = 100 / ((palmPos[whenBallTouchesGround][0] - ballPos[whenBallTouchesGround][0]) * (palmPos[whenBallTouchesGround][1] - ballPos[whenBallTouchesGround][1]) * (palmPos[whenBallTouchesGround][2] - ballPos[whenBallTouchesGround][2]) + 1)
            #fitness = 100 / (np.abs(palmPos[0][0] - palmPos[phase0][0]) * np.abs(palmPos[0][1] - palmPos[phase0][1]) * np.abs(palmPos[0][2] - palmPos[phase0][2])) 

        elif (whenBallTouchesGround >= phase0) and not(fullContact):

            print("phase 1")
            palmContact = (timeInQ1 * timeInQ4) * (timeInQ3 * timeInQ2)
            contactL = timeInL1 * timeInL2
            contactR = timeInR1 * timeInR2
            contactT = timeInT1 * timeInT2
            joinedContact = 1.0 + (timeInL + timeInR) * timeInT
            groundPenalty = 1.0 / (1.0 + timeTouchingGround * 10)
            rotationPenalty = negativeRotation * 1
    
            contactScore = (palmContact + contactL + contactR + contactT) * joinedContact
            fitness = (100.0 / (1.0 / (1.0 + contactScore))) * groundPenalty
            fitness += closingMotion * 5000
            fitness -= rotationPenalty
            #fitness = (100.0 / (1.0 / ((palmContact + contactL + contactR + 2.0 * contactT) * joinedContact) + 1.0)) - timeTouchingGround
            #fitness = (100.0 / (1.0 / (1.0 + ((palmContact + contactL + contactR + contactL) * joinedContact)))) - penalty

        elif fullContact:

            fitness = 10000000000000000000000000000000000

        else:

            print("broken function")
        # use pipe to send fitness to parent program
        connection.send(fitness)
        connection.close()
