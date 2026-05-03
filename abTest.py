# this runs A/B testing of the robotic arm experiment
from multiprocessing import Process
from search import Run
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

NUM_TESTS_EACH = 2

def Graph():

    a_files = glob.glob("data//data_A*.npy")
    b_files = glob.glob("data//data_B*.npy")

    i = 0
    for file in a_files:

        data = np.load(file)
        plt.plot(data, color="blue", alpha=0.5, label="A" if i == 0 else "_nolegend_")
        i += 1

    i = 0
    for file in b_files:

        data = np.load(file)
        plt.plot(data, color="orange", alpha=0.5, label="B" if i == 0 else "_nolegend_")
        i += 1

    plt.title("Robotic Arm Grasping A/B Tests")
    plt.xlabel("Evolutionary Time")
    plt.ylabel("Fitness")
    plt.legend()
    plt.show()
    plt.savefig("ABResults.png")

if __name__ == "__main__":

    # run each test for amount of tests
    for i in range(NUM_TESTS_EACH):

        os.environ["TESTNUMBER"] = str(i)

        # spawn A test
        os.environ["TEST"] = "A"

        p = Process(target=Run)

        p.start()
        p.join()

        # spawn B test
        os.environ["TEST"] = "B"

        p = Process(target=Run)

        p.start()
        p.join()

    # graph data
    Graph()
