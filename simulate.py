from simulation import SIMULATION
import sys
import os

def Run(directOrGUI, solutionID, connection, supressMessages):

    # TODO: implement message suppression
    if supressMessages:

        pass

    simulation = SIMULATION(directOrGUI, solutionID)

    simulation.Run()

    simulation.Get_Fitness(connection)
