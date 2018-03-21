import json

class OutputGenerator:
    def __init__(self):
        self.object_count = 0
        self.output_file = "data.json"
        # Configure the right format for json      
        self.Configure_dict = {}
        self.Sphere_list = []
        self.Cube_list = []
        self.Tetrahedron_list = []
        self.Cylinder_list = []
        self.Cone_list = []
        self.Plane_list = []
        self.camera_position = []
        self.camera_point_to = []
        self.light = []

    def Truncate_File(self):
        with open(self.output_file, 'r+') as f:
            f.seek(0)
            f.truncate()
        self.object_count = 0
        self.Configure_dict = {}
        self.Sphere_list = []
        self.Cube_list = []
        self.Tetrahedron_list = []
        self.Cylinder_list = []
        self.Cone_list = []
        self.Plane_list = []
        self.camera_position = []
        self.camera_point_to = []
        self.light = []

    def Scene_Config(self,camera_c,camera_l,light):
        self.camera_position = camera_c
        self.camera_point_to = camera_l
        self.light = light

    def Add_Plane(self,plane_position,plane_normal,transparency):
        Plane_dict_temp = {}
        Plane_dict_temp["position"] = plane_position
        Plane_dict_temp["normal"] = plane_normal
        Plane_dict_temp["transparency_level"] = transparency
        self.Plane_list.append(Plane_dict_temp)

    def Add_Sphere(self,position,radius,color,transparency):
        self.object_count += 1
        Sphere_dict_temp = {}
        Sphere_dict_temp["position"] = position
        Sphere_dict_temp["radius"] = radius
        Sphere_dict_temp["color"] = color
        Sphere_dict_temp["transparency_level"] = transparency
        self.Sphere_list.append(Sphere_dict_temp)

    def Add_Cube(self,position,length,rotation_angle,color,transparency):
        self.object_count += 1
        Cube_dict_temp = {}
        Cube_dict_temp["position"] = position
        Cube_dict_temp["length"] = length
        Cube_dict_temp["rotation_angle"] = rotation_angle
        Cube_dict_temp["color"] = color
        Cube_dict_temp["transparency_level"] = transparency
        self.Cube_list.append(Cube_dict_temp)

    def Add_Tetrahedron(self,position,length,rotation_angle,color,transparency):
        self.object_count += 1
        Tetrahedron_dict_temp = {}
        Tetrahedron_dict_temp["position"] = position
        Tetrahedron_dict_temp["length"] = length
        Tetrahedron_dict_temp["rotation_angle"] = rotation_angle
        Tetrahedron_dict_temp["color"] = color
        Tetrahedron_dict_temp["transparency_level"] = transparency
        self.Tetrahedron_list.append(Tetrahedron_dict_temp)

    def Add_Cylinder(self,position,height,radius,rotation_angle,color,transparency):
        self.object_count += 1
        Cylinder_dict_temp = {}
        Cylinder_dict_temp["position"] = position
        Cylinder_dict_temp["height"] = height
        Cylinder_dict_temp["radius"] = radius
        Cylinder_dict_temp["rotation_angle"] = rotation_angle
        Cylinder_dict_temp["color"] = color
        Cylinder_dict_temp["transparency_level"] = transparency
        self.Cylinder_list.append(Cylinder_dict_temp)

    def Add_Cone(self,position,height,radius,rotation_angle,color,transparency):
        self.object_count += 1
        Cone_dict_temp = {}
        Cone_dict_temp["position"] = position
        Cone_dict_temp["height"] = height
        Cone_dict_temp["radius"] = radius
        Cone_dict_temp["rotation_angle"] = rotation_angle
        Cone_dict_temp["color"] = color
        Cone_dict_temp["transparency_level"] = transparency
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
        self.Configure_dict["plane"] = self.Plane_list
        self.Configure_dict["camera_position"] = self.camera_position
        self.Configure_dict["camera_point_to"] = self.camera_point_to
        self.Configure_dict["light"] = self.light
        content = json.dumps(self.Configure_dict, sort_keys=True, indent=4)
        with open(self.output_file, 'w') as f:
            f.write(content)
            f.close()
