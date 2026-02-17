from solution import SOLUTION
import constants as c
import copy

class HILL_CLIMBER:

    def __init__(self):

        self.parent = SOLUTION()


    def Evolve(self):

        self.parent.Evaluate("GUI")

        for currentGeneration in range(c.NUMBER_OF_GENERATIONS):

            self.Evolve_For_One_Generation("DIRECT")


    def Evolve_For_One_Generation(self, directOrGUI):

        self.Spawn()
        self.Mutate()
        self.child.Evaluate(directOrGUI)
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

    def Show_Best(self):

        self.parent.Evaluate("GUI")
