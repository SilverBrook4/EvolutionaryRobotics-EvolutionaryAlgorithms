from parallelHillClimber import PARALLEL_HILL_CLIMBER
import os

def Run():

    phc = PARALLEL_HILL_CLIMBER()

    phc.Evolve()

    phc.Show_Best()

    phc.Save_Data()

if __name__ == "__main__":

    Run()
