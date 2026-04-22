import numpy as np

#----------------------------------------------------

# Set Evolution Values
NUMBER_OF_GENERATIONS = 50 # the number of generations that will be evolved

POPULATION_SIZE = 15 # number of nn's in a population
#----------------------------------------------------

# Set Simulation Values
NUM_SIM_STEPS = 500 # sets number of simulation steps

SIM_SLEEP = 0.01 # time simulation sleeps

PYBULLET_DEBUGGER = False # Turns pybuller debugger on and off

SHOW_NN_UPDATES = False # shows updates to neural network weights across steps

SUPPRESS_PYBULLET_MESSAGES = True # supresses pybullet error messages and extra messages

#----------------------------------------------------

# Sets Neural Network Values
NUM_SENSOR_NEURONS = 30 # number of sensor neurons

NUM_HIDDEN_NEURONS = 5 # number of hidden neurons

NUM_MOTOR_NEURONS = 13 # number of motor neurons

FITNESS_THRESHOLD = 0.3

#----------------------------------------------------

MAX_MOTOR_FORCE = 1000

#----------------------------------------------------

# Set leg Values
AMPLITUDE = np.pi / 4

FREQUENCY = 10

PHASE_OFFSET = 0

MOTOR_JOINT_RANGE = np.pi / 2
