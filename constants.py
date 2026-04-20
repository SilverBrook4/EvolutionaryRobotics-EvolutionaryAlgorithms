import numpy

#----------------------------------------------------

# Set Evolution Values
NUMBER_OF_GENERATIONS = 2 # the number of generations that will be evolved

POPULATION_SIZE = 2 # number of nn's in a population
#----------------------------------------------------

# Set Simulation Values
NUM_SIM_STEPS = 5000 # sets number of simulation steps

SIM_SLEEP = 0.01 # time simulation sleeps

PYBULLET_DEBUGGER = False # Turns pybuller debugger on and off

SHOW_NN_UPDATES = True # shows updates to neural network weights across steps

SUPPRESS_PYBULLET_MESSAGES = True # supresses pybullet error messages and extra messages

#----------------------------------------------------

# Sets Neural Network Values
NUM_SENSOR_NEURONS = 24 # number of sensor neurons

NUM_HIDDEN_NEURONS = 0

NUM_MOTOR_NEURONS = 13 # number of motor neurons

#----------------------------------------------------

# Set leg Values
AMPLITUDE = numpy.pi / 4

FREQUENCY = 10

PHASE_OFFSET = 0

MOTOR_JOINT_RANGE = 0.7
