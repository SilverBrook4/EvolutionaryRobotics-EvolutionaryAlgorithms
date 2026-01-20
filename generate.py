import pyrosim.pyrosim as pyrosim


pyrosim.Start_SDF("boxs.sdf")

length = 1
width = 1
height = 1

x = 0
y = 0
z = 0.5

for k in range(5):
    for j in range(5):
        for i in range(5):
            pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])
            z = z + 1
            length = length * 0.9
            width = width * 0.9
            height = height * 0.9
        length = 1
        width = 1
        height = 1
        z = 0.5
        y = y + 1
    y = 0
    x = x + 1

pyrosim.End()
