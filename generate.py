import pyrosim.pyrosim as pyrosim

# define cration functions

def Create_World():
    pyrosim.Start_SDF("world.sdf")

    length = 1
    width = 1
    height = 1

    x = -5
    y = 0
    z = 0.5

    pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])

    pyrosim.End()

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")

    # create Torso
    length = 1
    width = 1
    height = 1

    x = 0
    y = 0
    z = 1.5

    pyrosim.Send_Cube(name="Torso", pos=[x, y, z], size=[length, width, height])

    # joint Torso and BackLeg
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[-0.5,0,1])

    # create BackLeg
    length = 1
    width = 1
    height = 1

    x = -0.5
    y = 0
    z = -0.5

    pyrosim.Send_Cube(name="BackLeg", pos=[x, y, z], size=[length, width, height])

    # joint Torso FrontLeg
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0.5,0,1])

    # create FrontLEg
    length = 1
    width = 1
    height = 1

    x = 0.5
    y = 0
    z = -0.5

    pyrosim.Send_Cube(name="FrontLeg", pos=[x, y, z], size=[length, width, height])

    pyrosim.End()


# run generate code
Create_World()
Create_Robot()
