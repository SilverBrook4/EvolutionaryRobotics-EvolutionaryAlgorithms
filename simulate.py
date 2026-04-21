from simulation import SIMULATION
import sys
import os

def Run(directOrGUI, solutionID, connection, supressMessages):

    if supressMessages:

        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        os.dup2(devnull, sys.stderr.fileno())
        os.close(devnull)

    simulation = SIMULATION(directOrGUI, solutionID)

    simulation.Run()

    simulation.Get_Fitness(connection)
