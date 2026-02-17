from parallelHillClimber import PARALLEL_HILL_CLIMBER
import os


if __name__ == "__main__":

    phc = PARALLEL_HILL_CLIMBER()

    phc.Evolve()

    phc.Show_Best()
