import numpy as np
import os

#----------------------------------------------------

TEST = os.environ.get("TEST")

#----------------------------------------------------

# Set Evolution Values
NUMBER_OF_GENERATIONS = 5 # the number of generations that will be evolved

POPULATION_SIZE = 5 # number of nn's in a population
#----------------------------------------------------

# Set Simulation Values
NUM_SIM_STEPS = 750 # sets number of simulation steps

SIM_SLEEP = 0.01 # time simulation sleeps

PYBULLET_DEBUGGER = False # Turns pybuller debugger on and off

SHOW_NN_UPDATES = False # shows updates to neural network weights across steps

SUPPRESS_PYBULLET_MESSAGES = True # supresses pybullet error messages and extra messages

#----------------------------------------------------

# Sets Neural Network Values
if TEST == "A":

    NUM_SENSOR_NEURONS = 30 # number of sensor neurons

elif TEST == "B":

    NUM_SENSOR_NEURONS = 30 # number of sensor neurons

else:

    NUM_SENSOR_NEURONS = 30 # number of sensor neurons

NUM_HIDDEN_NEURONS = 7 # number of hidden neurons

NUM_MOTOR_NEURONS = 16 # number of motor neurons

FITNESS_THRESHOLD = 0.3 # threshold fitness must meet to avoid a total neural network reinitilization

#----------------------------------------------------

MAX_MOTOR_FORCE = 1100

MOTOR_JOINT_RANGE = np.pi / 2

FINGURE_ROTATOR_JOINT_RANGE = np.pi / 6

WRIST_SHIFT_JOINT_RANGE = np.pi / 6
