from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:

    # creates an instance of the parallel hill climber class
    def __init__(self):

        # cleans up any files leftover from a crash
        os.system("rm brain*.nndf")
        os.system("rm data//fitness*.nndf")
        os.system("rm data//tmp*.nndf")

        self.parents = {}

        self.nextAvailableID = 0


        # creates a population of parents
        for parent in range(c.POPULATION_SIZE):

            self.parents[parent] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1


    # carrys out evolution of neural networks across generations
    def Evolve(self):

        # evaluate parents
        self.Evaluate(self.parents)

        # evolves each generation
        for currentGeneration in range(c.NUMBER_OF_GENERATIONS):

            self.Evolve_For_One_Generation("DIRECT")


    # evolves one generation of neural networks
    def Evolve_For_One_Generation(self, directOrGUI):

        pass

        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()


    # spawns children from parent
    def Spawn(self):

        self.children = {}

        for child in range(c.POPULATION_SIZE):

            self.children[child] = copy.deepcopy(self.parents[child])
            self.children[child].Set_ID(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1


    # mutates children to facilitate evolution
    def Mutate(self):

        for child in self.children:

            self.children[child].Mutate()


    # evaluates passed in solutions 
    def Evaluate(self, solutions):

        # starts simulation of solutions
        for solution in solutions:

            solutions[solution].Start_Simulation("DIRECT")

        # end parent simulations
        for solution in solutions:

            solutions[solution].Wait_For_Simulation_To_End()


    # selects most fit parent or child
    def Select(self):

        for key in range(c.POPULATION_SIZE):

            if (self.parents[key].fitness > self.children[key].fitness):

                self.parents[key] = copy.deepcopy(self.children[key])


    # prints parent and childs fitness
    def Print(self):

        print("\n")

        for key in range(c.POPULATION_SIZE):

            print(f"Parent Fitness: {self.parents[key].fitness} || Child Fitness: {self.children[key].fitness}")

        print("\n")


    # replays best solution in GUI to see improvment from training
    def Show_Best(self):

        bestSolution = 0

        for solution in range(1, c.POPULATION_SIZE):

            if (self.parents[bestSolution].fitness > self.parents[solution].fitness):

                bestSolution = solution

        print(f"Best Fitness Found: {self.parents[bestSolution].fitness}")
        self.parents[bestSolution].Start_Simulation("GUI")
