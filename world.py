import pybullet as p
import os

class WORLD:

    def __init__(self, solutionID):

        self.planeId = p.loadURDF("plane.urdf")
        self.objects = p.loadSDF(f"world{solutionID}.sdf")
        os.system(f"rm world{solutionID}.sdf")
