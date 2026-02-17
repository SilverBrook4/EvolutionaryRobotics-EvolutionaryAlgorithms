from simulation import SIMULATION
import sys

if __name__ == ("__main__"):

    directOrGUI = sys.argv[1]
    simulation = SIMULATION(directOrGUI)

    simulation.Run()

    simulation.Get_Fitness()

