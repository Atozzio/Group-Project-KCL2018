"""
Read the input from JSON file

"""



import json
with open('data.json', 'r') as f:
    data = json.load(f)

scene = []

def addTetrahedron():
    print("add tetrahedron")


def addCube():
    print("add cube")


def addCylinder():
    print("add cylinder")


def addSphere():
    print("add sphere")


def addPlane():
    print("add plane")



print(data.keys())
for key in data.keys():
    #print('key',key, 'value',data[key])
    if key == 'tetrahedron':
        for _ in range(len(data[key])):
            position1 = data[key][_]['position1']
            position2 = data[key][_]['position2']
            position3 = data[key][_]['position3']
            position4 = data[key][_]['position4']
            position = tuple()
            position = tuple((position1,)) + (position2,) + (position3,) + (position4,)
            color = data[key][_]['color']
            #print(position)
            addTetrahedron()
            #scene.append(add_tetrahedron(position, color))
    elif key == 'cube':
        for _ in range(len(data[key])):
            position = data[key][_]['position']
            length = data[key][_]['length']
            rotation_angle = data[key][_]['rotation_angle']
            color = data[key][_]['color']
            addCube()
            #scene.append(add_cube(position,length,rotation_angle,color))
    elif key == 'cylinder':
        for _ in range(len(data[key])):
            position = data[key][_]['position']
            height = data[key][_]['height']
            radius = data[key][_]['radius']
            color = data[key][_]['color']
            addCylinder()
            #scene.append(add_cylinder(position, height, radius, rotation_angle, color))
    elif key == 'sphere':
        for _ in range(len(data[key])):
            position = data[key][_]['position']
            radius = data[key][_]['radius']
            color = data[key][_]['color']
            addSphere()
            #scene.append(add_sphere(position, radius, color))
    elif key == 'plane':
        for _ in range(len(data[key])):
            position = data[key][_]['position']
            normal = data[key][_]
            addPlane()
            #scene.append(add_plane(position, normal))


