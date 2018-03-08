import json

class OutputGenerator:
    def __init__(self):
        self.output_file = "data.json"
        # Configure the right format for json      
        self.Configure_dict = {}

        self.Sphere_list = []
        self.Cube_list = []
        self.Tetrahedron_list = []
        self.Cylinder_list = []
        self.Cone_list = []
        self.Scene_list = []

    def Scene_Config(self,plane_position,plane_normal):
        Scene_dict_temp = {}
        Scene_dict_temp["position"] = plane_position
        Scene_dict_temp["normal"] = plane_normal
        self.Scene_list.append(Scene_dict_temp)

    def Add_Sphere(self,position,radius,color):
        Sphere_dict_temp = {}
        Sphere_dict_temp["position"] = position
        Sphere_dict_temp["radius"] = radius
        Sphere_dict_temp["color"] = color
        self.Sphere_list.append(Sphere_dict_temp)

    def Add_Cube(self,position,length,rotation_angle,color):
        Cube_dict_temp = {}
        Cube_dict_temp["position"] = position
        Cube_dict_temp["length"] = length
        Cube_dict_temp["rotation_angle"] = rotation_angle
        Cube_dict_temp["color"] = color
        self.Cube_list.append(Cube_dict_temp)

    def Add_Tetrahedron(self,position1,position2,position3,position4,color):
        Tetrahedron_dict_temp = {}
        Tetrahedron_dict_temp["position1"] = position1
        Tetrahedron_dict_temp["position2"] = position2
        Tetrahedron_dict_temp["position3"] = position3
        Tetrahedron_dict_temp["position4"] = position4
        Tetrahedron_dict_temp["color"] = color
        self.Tetrahedron_list.append(Tetrahedron_dict_temp)

    def Add_Cylinder(self,position,height,radius,rotation_angle,color):
        Cylinder_dict_temp = {}
        Cylinder_dict_temp["position"] = position
        Cylinder_dict_temp["height"] = height
        Cylinder_dict_temp["radius"] = radius
        Cylinder_dict_temp["rotation_angle"] = rotation_angle
        Cylinder_dict_temp["color"] = color
        self.Cylinder_list.append(Cylinder_dict_temp)

    def Add_Cone(self,position,height,radius,rotation_angle,color):
        Cone_dict_temp = {}
        Cone_dict_temp["position"] = position
        Cone_dict_temp["height"] = height
        Cone_dict_temp["radius"] = radius
        Cone_dict_temp["rotation_angle"] = rotation_angle
        Cone_dict_temp["color"] = color
        self.Cone_list.append(Cone_dict_temp)

    def Generate_File(self):
        if self.Tetrahedron_list: # if there is at least one Tetrahedron in the scene
            self.Configure_dict["tetrahedron"] = self.Tetrahedron_list
        if self.Cube_list:
            self.Configure_dict["cube"] = self.Cube_list
        if self.Cone_list:
            self.Configure_dict["cone"] = self.Cone_list
        if self.Sphere_list:
            self.Configure_dict["sphere"] = self.Sphere_list
        if self.Cylinder_list:
            self.Configure_dict["cylinder"] = self.Cylinder_list
        self.Configure_dict["plane"] = self.Scene_list
        content = json.dumps(self.Configure_dict, sort_keys=True, indent=4)
        with open(self.output_file, 'w') as f:
            f.write(content)
            f.close()


# f = OutputGenerator()
# f.Add_Sphere()
# f.Add_Sphere()
# f.Generate_File()

