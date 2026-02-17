from hillclimber import HILL_CLIMBER
import os


if __name__ == "__main__":

    hc = HILL_CLIMBER()

    hc.Evolve()

    '''
    for i in range(5):
        os.system("python3 generate.py")

        os.system("python3 simulate.py")
    '''
