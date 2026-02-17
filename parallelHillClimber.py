from solution import SOLUTION
import constants as c
import copy

class PARALLEL_HILL_CLIMBER:

    # creates an instance of the parallel hill climber class
    def __init__(self):

        self.parents = {}

        self.nextAvailableID = 0


        # creates a population of parents
        for parent in range(c.POPULATION_SIZE):

            self.parents[parent] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1


    def Evolve(self):

        for parent in self.parents:

            self.parents[parent].Evaluate("GUI")

        '''
        for currentGeneration in range(c.NUMBER_OF_GENERATIONS):

            self.Evolve_For_One_Generation("DIRECT")
        '''


    def Evolve_For_One_Generation(self, directOrGUI):

        self.Spawn()
        self.Mutate()
        self.child.Evaluate(directOrGUI)
        self.Print()
        self.Select()


    def Spawn(self):

        self.child = copy.deepcopy(self.parent)

        self.child.Set_ID(self.nextAvailableID)
        self.nextAvailableID = self.nextAvailableID + 1


    def Mutate(self):

        self.child.Mutate()


    def Select(self):

        if (self.parent.fitness > self.child.fitness):

            self.parent = copy.deepcopy(self.child)

    def Print(self):
        print(f"Parent Fitness: {self.parent.fitness} Child Fitness: {self.child.fitness}")

    def Show_Best(self):

        pass

        #self.parent.Evaluate("GUI")
