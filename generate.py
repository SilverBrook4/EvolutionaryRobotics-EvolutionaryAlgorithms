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

    # create link 0 - root
    length = 1
    width = 1
    height = 1

    x = 0
    y = 0
    z = 0.5

    pyrosim.Send_Cube(name="Link0", pos=[x, y, z], size=[length, width, height])

    # joint links 0 and 1
    pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute", position=[0,0,1])

    # create link 1
    length = 1
    width = 1
    height = 1

    x = 0
    y = 0
    z = 0.5

    pyrosim.Send_Cube(name="Link1", pos=[x, y, z], size=[length, width, height])

    # joint links 1 & 2
    pyrosim.Send_Joint(name="Link1_Link2", parent="Link1", child="Link2", type="revolute", position=[0,0,1])

    # create link 2
    length = 1
    width = 1
    height = 1

    x = 0
    y = 0
    z = 0.5

    pyrosim.Send_Cube(name="Link2", pos=[x, y, z], size=[length, width, height])

    # joint links 2 & 3
    pyrosim.Send_Joint(name="Link2_Link3", parent="Link2", child="Link3", type="revolute", position=[0,0.5,0.5])

    # create link 3
    length = 1
    width = 1
    height = 1

    x = 0
    y = 0.5
    z = 0

    pyrosim.Send_Cube(name="Link3", pos=[x, y, z], size=[length, width, height])

    # joint links 3 & 4
    pyrosim.Send_Joint(name="Link3_Link4", parent="Link3", child="Link4", type="revolute", position=[0,1,0])

    # create link 4
    length = 1
    width = 1
    height = 1

    x = 0
    y = 0.5
    z = 0

    pyrosim.Send_Cube(name="Link4", pos=[x, y, z], size=[length, width, height])

    # joint links 4 & 5
    pyrosim.Send_Joint(name="Link4_Link5", parent="Link4", child="Link5", type="revolute", position=[0,0.5,-0.5])

    # create link 5
    length = 1
    width = 1
    height = 1

    x = 0
    y = 0
    z = -0.5

    pyrosim.Send_Cube(name="Link5", pos=[x, y, z], size=[length, width, height])

    # joint links 5 & 6
    pyrosim.Send_Joint(name="Link5_Link6", parent="Link5", child="Link6", type="revolute", position=[0,0,-1])

    # create link 6
    length = 1
    width = 1
    height = 1

    x = 0
    y = 0
    z = -0.5

    pyrosim.Send_Cube(name="Link6", pos=[x, y, z], size=[length, width, height])

    pyrosim.End()


# run generate code
Create_World()
Create_Robot()
