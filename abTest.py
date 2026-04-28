# this runs A/B testing of the robotic arm experiment
from multiprocessing import Process
from search import Run
import os

NUM_TESTS_EACH = 1

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
