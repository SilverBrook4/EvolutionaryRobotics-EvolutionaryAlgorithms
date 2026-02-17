from solution import SOLUTION
import constants as c
import copy

class HILL_CLIMBER:

    def __init__(self):

        self.parent = SOLUTION()


    def Evolve(self):

        self.parent.Evaluate()

        for currentGeneration in range(c.NUMBER_OF_GENERATIONS):

            self.Evolve_For_One_Generation()


    def Evolve_For_One_Generation(self):

        self.Spawn()
        self.Mutate()
        self.child.Evaluate()
        self.Print()
        self.Select()


    def Spawn(self):

        self.child = copy.deepcopy(self.parent)


    def Mutate(self):

        self.child.Mutate()


    def Select(self):

        if (self.parent.fitness > self.child.fitness):

            self.parent = copy.deepcopy(self.child)

    def Print(self):
        print(f"Parent Fitness: {self.parent.fitness} Child Fitness: {self.child.fitness}")
