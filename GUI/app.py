from flask import Flask,request, render_template
from generate_output import OutputGenerator
import json

app = Flask(__name__)
OutputFile = OutputGenerator()
 
@app.route('/')
def render_static():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/ObjectQuantity', methods=['POST', 'GET'])
def ObjectQuantity():
    if request.method == 'POST':
        quantity = request.form['mySelect']
        if quantity:
            return render_template('ObjectFeature.html',quantity=quantity)
        else:
            print "something went wrong"
    return render_template('ObjectQuantity.html')

@app.route('/Figure')
def Figure():
    pass
    return render_template('Figure.html')

@app.route('/ObjectFeature', methods=['POST', 'GET'])
def ObjectFeature():
    global OutputFile
    object_quantity = 0
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data["object_quantity"]:
            object_quantity_web = post_data["object_quantity"]
        else:
            return "Object_quantity receiving error!"
# Scene Parameters
    #Plane Starting Point
        Plane_Position_X = float(post_data['Plane_Position_X'])
        Plane_Position_Y = float(post_data['Plane_Position_Y'])
        Plane_Position_Z = float(post_data['Plane_Position_Z'])
    #Plane Normal Vector
        Plane_Normal_X = float(post_data['Plane_Normal_X'])
        Plane_Normal_Y = float(post_data['Plane_Normal_Y'])
        Plane_Normal_Z = float(post_data['Plane_Normal_Z'])
    #Plane Transparency
        Plane_Transparency = int(post_data['Plane_Transparency'])
    #Camera Coordinates
        Camera_C_X = float(post_data['Camera_C_X'])
        Camera_C_Y = float(post_data['Camera_C_Y'])
        Camera_C_Z = float(post_data['Camera_C_Z'])
    #Camera Looking Point
        Camera_L_X = float(post_data['Camera_C_X'])
        Camera_L_Y = float(post_data['Camera_C_Y'])
        Camera_L_Z = float(post_data['Camera_C_Z'])
    #Light source
        Light_X = float(post_data['Light_X'])
        Light_Y = float(post_data['Light_Y'])
        Light_Z = float(post_data['Light_Z'])
    #Constructing Proper Data Structure
        Plane_Position = [Plane_Position_X,Plane_Position_Y,Plane_Position_Z]
        Plane_Normal = [Plane_Normal_X,Plane_Normal_Y,Plane_Normal_Z]
        Camera_Coordinates = [Camera_C_X,Camera_C_Y,Camera_C_Z]
        Camera_Looking = [Camera_L_X,Camera_L_Y,Camera_L_Z]
        Light_Source = [Light_X,Light_Y,Light_Z]
        OutputFile.Add_Plane(Plane_Position,Plane_Normal,Plane_Transparency)
        OutputFile.Scene_Config(Camera_Coordinates,Camera_Looking,Light_Source)
        
#   First Object
        if 'Object1' in post_data:
            flag = 1 # If user fills in all the blank for this object, otherwise flag == 0.
            Transparency1 = int(post_data["Transparency1"])
            # user choose to have a Sphere
            if post_data["Object1"]=="Sphere":
                if post_data["Sphere_x1"]:
                    Sphere_x = float(post_data['Sphere_x1']) 
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Sphere!"
                if post_data["Sphere_y1"]:
                    Sphere_y = float(post_data['Sphere_y1'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Sphere!"
                if post_data["Sphere_z1"]:
                    Sphere_z = float(post_data['Sphere_z1'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Sphere!"
                if post_data["Sphere_cr1"]:
                    Sphere_Color_R = float(post_data['Sphere_cr1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cg1"]:
                    Sphere_Color_G = float(post_data['Sphere_cg1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cb1"]:
                    Sphere_Color_B = float(post_data['Sphere_cb1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_r1"]:
                    Sphere_Radius = float(post_data["Sphere_r1"])
                else:
                    flag = 0
                    return "Please input the radius of the Sphere!"
                if flag == 1:
                    object_quantity += 1
                    Sphere_Coordinates = [Sphere_x,Sphere_y,Sphere_z]
                    Sphere_Color = [Sphere_Color_R,Sphere_Color_G,Sphere_Color_B]
                    OutputFile.Add_Sphere(Sphere_Coordinates,Sphere_Radius,Sphere_Color,Transparency1)
            
            # user choose to have a Cube
            elif post_data["Object1"]=="Cube":
                if post_data["Cube_x1"]:
                    Cube_x = float(post_data['Cube_x1'])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cube!"
                if post_data["Cube_y1"]:
                    Cube_y = float(post_data['Cube_y1'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube!"
                if post_data["Cube_z1"]:
                    Cube_z = float(post_data['Cube_z1'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube!"
                if post_data["Cube_l1"]:
                    Cube_SideLength = float(post_data['Cube_l1'])
                else:
                    flag = 0
                    return "Please input value for the Cube Side Length!"
                if post_data["Cube_cr1"]:
                    Cube_Color_R = float(post_data['Cube_cr1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cg1"]:
                    Cube_Color_G = float(post_data['Cube_cg1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cb1"]:
                    Cube_Color_B = float(post_data['Cube_cb1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_rx1"]:
                    Cube_Rotate_x = float(post_data['Cube_rx1'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cube Rotation!"
                if post_data["Cube_ry1"]:
                    Cube_Rotate_y = float(post_data['Cube_ry1'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube Rotation!"
                if post_data["Cube_rz1"]:
                    Cube_Rotate_z = float(post_data['Cube_rz1'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube Rotation!"
                if flag == 1:
                    object_quantity += 1
                    Cube_Coordinates = [Cube_x,Cube_y,Cube_z]
                    Cube_Rotation = [Cube_Rotate_x,Cube_Rotate_y,Cube_Rotate_z]
                    Cube_Color = [Cube_Color_R,Cube_Color_G,Cube_Color_B]
                    OutputFile.Add_Cube(Cube_Coordinates,Cube_SideLength,Cube_Rotation,Cube_Color,Transparency1)
            
            #user choose to have a Tetrahedron
            elif post_data["Object1"]=="Tetrahedron":
                if post_data["Tetrahedron_x1"]:
                    Tetrahedron_x = float(post_data['Tetrahedron_x1'])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_y1"]:
                    Tetrahedron_y = float(post_data['Tetrahedron_y1'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_z1"]:
                    Tetrahedron_z = float(post_data['Tetrahedron_z1'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_l1"]:
                    Tetrahedron_SideLength = float(post_data['Tetrahedron_l1'])
                else:
                    flag = 0
                    return "Please input value for the Tetrahedron Side Length!"
                if post_data["Tetrahedron_cr1"]:
                    Tetrahedron_Color_R = float(post_data['Tetrahedron_cr1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cg1"]:
                    Tetrahedron_Color_G = float(post_data['Tetrahedron_cg1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cb1"]:
                    Tetrahedron_Color_B = float(post_data['Tetrahedron_cb1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_rx1"]:
                    Tetrahedron_Rotate_x = float(post_data['Tetrahedron_rx1'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_ry1"]:
                    Tetrahedron_Rotate_y = float(post_data['Tetrahedron_ry1'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_rz1"]:
                    Tetrahedron_Rotate_z = float(post_data['Tetrahedron_rz1'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Rotation!"
                if flag == 1:
                    object_quantity += 1
                    Tetrahedron_Coordinates = [Tetrahedron_x,Tetrahedron_y,Tetrahedron_z]
                    Tetrahedron_Rotation = [Tetrahedron_Rotate_x,Tetrahedron_Rotate_y,Tetrahedron_Rotate_z]
                    Tetrahedron_Color = [Tetrahedron_Color_R,Tetrahedron_Color_G,Tetrahedron_Color_B]
                    OutputFile.Add_Tetrahedron(Tetrahedron_Coordinates,Tetrahedron_SideLength,Tetrahedron_Rotation,Tetrahedron_Color,Transparency1)
            
            #user choose to have a Cylinder
            elif post_data["Object1"]=="Cylinder":
                if post_data["Cylinder_x1"]:
                    Cylinder_x = float(post_data["Cylinder_x1"])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cylinder!"
                if post_data["Cylinder_y1"]:
                    Cylinder_y = float(post_data['Cylinder_y1'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder!"
                if post_data["Cylinder_z1"]:
                    Cylinder_z = float(post_data['Cylinder_z1'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder!"
                if post_data["Cylinder_rx1"]:
                    Cylinder_Rotate_x = float(post_data['Cylinder_rx1'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_ry1"]:
                    Cylinder_Rotate_y = float(post_data['Cylinder_ry1'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_rz1"]:
                    Cylinder_Rotate_z = float(post_data['Cylinder_rz1'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_cr1"]:
                    Cylinder_Color_R = float(post_data['Cylinder_cr1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cg1"]:
                    Cylinder_Color_G = float(post_data['Cylinder_cg1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cb1"]:
                    Cylinder_Color_B = float(post_data['Cylinder_cb1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_h1"]:
                    Cylinder_Height = float(post_data['Cylinder_h1'])
                else:
                    flag = 0
                    return "Please input value for the Cylinder Height!"
                if post_data["Cylinder_r1"]:
                    Cylinder_Radius = float(post_data['Cylinder_r1'])
                else:
                    flag = 0
                    return "Please input value for the Cylinder Radius!"
                if flag == 1:
                    object_quantity += 1
                    Cylinder_Coordinates = [Cylinder_x,Cylinder_y,Cylinder_z]
                    Cylinder_Rotation = [Cylinder_Rotate_x,Cylinder_Rotate_y,Cylinder_Rotate_z]
                    Cylinder_Color = [Cylinder_Color_R,Cylinder_Color_G,Cylinder_Color_B]
                    OutputFile.Add_Cylinder(Cylinder_Coordinates,Cylinder_Height,Cylinder_Radius,Cylinder_Rotation,Cylinder_Color,Transparency1)
            
            #user choose to have a Cone
            elif post_data["Object1"]=="Cone":
                if post_data["Cone_x1"]:
                    Cone_x = float(post_data["Cone_x1"])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cone!"
                if post_data["Cone_y1"]:
                    Cone_y = float(post_data['Cone_y1'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone!"
                if post_data["Cone_z1"]:
                    Cone_z = float(post_data['Cone_z1'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone!"
                if post_data["Cone_rx1"]:
                    Cone_Rotate_x = float(post_data['Cone_rx1'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cone Rotation!"
                if post_data["Cone_ry1"]:
                    Cone_Rotate_y = float(post_data['Cone_ry1'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone Rotation!"
                if post_data["Cone_rz1"]:
                    Cone_Rotate_z = float(post_data['Cone_rz1'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone Rotation!"
                if post_data["Cone_cr1"]:
                    Cone_Color_R = float(post_data['Cone_cr1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cg1"]:
                    Cone_Color_G = float(post_data['Cone_cg1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cb1"]:
                    Cone_Color_B = float(post_data['Cone_cb1'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_h1"]:
                    Cone_Height = float(post_data['Cone_h1'])
                else:
                    flag = 0
                    return "Please input value for the Cone Height!"
                if post_data["Cone_r1"]:
                    Cone_Radius = float(post_data['Cone_r1'])
                else:
                    flag = 0
                    return "Please input value for the Cone Radius!"
                if flag == 1:
                    object_quantity += 1
                    Cone_Coordinates = [Cone_x,Cone_y,Cone_z]
                    Cone_Rotation = [Cone_Rotate_x,Cone_Rotate_y,Cone_Rotate_z]
                    Cone_Color = [Cone_Color_R,Cone_Color_G,Cone_Color_B]
                    OutputFile.Add_Cone(Cone_Coordinates,Cone_Height,Cone_Radius,Cone_Rotation,Cone_Color,Transparency1)
            else:
                return "Input did not complete!"
        elif object_quantity_web>0:
            return "Please at least choose one object then press 'Save'! "


#  Second Object
        if 'Object2' in post_data:
            flag = 1 # If user fills in all the blank for this object, otherwise flag == 0.
            Transparency2 = int(post_data["Transparency2"])
            # user choose to have a Sphere
            if post_data["Object2"]=="Sphere":
                if post_data["Sphere_x2"]:
                    Sphere_x = float(post_data['Sphere_x2']) 
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Sphere!"  
                if post_data["Sphere_y2"]:
                    Sphere_y = float(post_data['Sphere_y2'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Sphere!"
                if post_data["Sphere_z2"]:
                    Sphere_z = float(post_data['Sphere_z2'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Sphere!"
                if post_data["Sphere_cr2"]:
                    Sphere_Color_R = float(post_data['Sphere_cr2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cg2"]:
                    Sphere_Color_G = float(post_data['Sphere_cg2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cb2"]:
                    Sphere_Color_B = float(post_data['Sphere_cb2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_r2"]:
                    Sphere_Radius = float(post_data["Sphere_r2"])
                else:
                    flag = 0
                    return "Please input the radius of the Sphere!"
                if flag == 1:
                    object_quantity += 1
                    Sphere_Coordinates = [Sphere_x,Sphere_y,Sphere_z]
                    Sphere_Color = [Sphere_Color_R,Sphere_Color_G,Sphere_Color_B]
                    OutputFile.Add_Sphere(Sphere_Coordinates,Sphere_Radius,Sphere_Color,Transparency2)
            
            # user choose to have a Cube
            elif post_data["Object2"]=="Cube":
                if post_data["Cube_x2"]:
                    Cube_x = float(post_data['Cube_x2'])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cube!"
                if post_data["Cube_y2"]:
                    Cube_y = float(post_data['Cube_y2'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube!"
                if post_data["Cube_z2"]:
                    Cube_z = float(post_data['Cube_z2'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube!"
                if post_data["Cube_l2"]:
                    Cube_SideLength = float(post_data['Cube_l2'])
                else:
                    flag = 0
                    return "Please input value for the Cube Side Length!"
                if post_data["Cube_cr2"]:
                    Cube_Color_R = float(post_data['Cube_cr2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cg2"]:
                    Cube_Color_G = float(post_data['Cube_cg2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cb2"]:
                    Cube_Color_B = float(post_data['Cube_cb2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_rx2"]:
                    Cube_Rotate_x = float(post_data['Cube_rx2'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cube Rotation!"
                if post_data["Cube_ry2"]:
                    Cube_Rotate_y = float(post_data['Cube_ry2'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube Rotation!"
                if post_data["Cube_rz2"]:
                    Cube_Rotate_z = float(post_data['Cube_rz2'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube Rotation!"
                if flag == 1:
                    object_quantity += 1
                    Cube_Coordinates = [Cube_x,Cube_y,Cube_z]
                    Cube_Rotation = [Cube_Rotate_x,Cube_Rotate_y,Cube_Rotate_z]
                    Cube_Color = [Cube_Color_R,Cube_Color_G,Cube_Color_B]
                    OutputFile.Add_Cube(Cube_Coordinates,Cube_SideLength,Cube_Rotation,Cube_Color,Transparency2)
            
            #user choose to have a Tetrahedron
            elif post_data["Object2"]=="Tetrahedron":
                if post_data["Tetrahedron_x2"]:
                    Tetrahedron_x = float(post_data['Tetrahedron_x2'])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_y2"]:
                    Tetrahedron_y = float(post_data['Tetrahedron_y2'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_z2"]:
                    Tetrahedron_z = float(post_data['Tetrahedron_z2'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_l2"]:
                    Tetrahedron_SideLength = float(post_data['Tetrahedron_l2'])
                else:
                    flag = 0
                    return "Please input value for the Tetrahedron Side Length!"
                if post_data["Tetrahedron_cr2"]:
                    Tetrahedron_Color_R = float(post_data['Tetrahedron_cr2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cg2"]:
                    Tetrahedron_Color_G = float(post_data['Tetrahedron_cg2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cb2"]:
                    Tetrahedron_Color_B = float(post_data['Tetrahedron_cb2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_rx2"]:
                    Tetrahedron_Rotate_x = float(post_data['Tetrahedron_rx2'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_ry2"]:
                    Tetrahedron_Rotate_y = float(post_data['Tetrahedron_ry2'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_rz2"]:
                    Tetrahedron_Rotate_z = float(post_data['Tetrahedron_rz2'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Rotation!"
                if flag == 1:
                    object_quantity += 1
                    Tetrahedron_Coordinates = [Tetrahedron_x,Tetrahedron_y,Tetrahedron_z]
                    Tetrahedron_Rotation = [Tetrahedron_Rotate_x,Tetrahedron_Rotate_y,Tetrahedron_Rotate_z]
                    Tetrahedron_Color = [Tetrahedron_Color_R,Tetrahedron_Color_G,Tetrahedron_Color_B]
                    OutputFile.Add_Tetrahedron(Tetrahedron_Coordinates,Tetrahedron_SideLength,Tetrahedron_Rotation,Tetrahedron_Color,Transparency2)
            
            #user choose to have a Cylinder
            elif post_data["Object2"]=="Cylinder":
                if post_data["Cylinder_x2"]:
                    Cylinder_x = float(post_data["Cylinder_x2"])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cylinder!"
                if post_data["Cylinder_y2"]:
                    Cylinder_y = float(post_data['Cylinder_y2'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder!"
                if post_data["Cylinder_z2"]:
                    Cylinder_z = float(post_data['Cylinder_z2'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder!"
                if post_data["Cylinder_rx2"]:
                    Cylinder_Rotate_x = float(post_data['Cylinder_rx2'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_ry2"]:
                    Cylinder_Rotate_y = float(post_data['Cylinder_ry2'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_rz2"]:
                    Cylinder_Rotate_z = float(post_data['Cylinder_rz2'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_cr2"]:
                    Cylinder_Color_R = float(post_data['Cylinder_cr2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cg2"]:
                    Cylinder_Color_G = float(post_data['Cylinder_cg2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cb2"]:
                    Cylinder_Color_B = float(post_data['Cylinder_cb2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_h2"]:
                    Cylinder_Height = float(post_data['Cylinder_h2'])
                else:
                    flag = 0
                    return "Please input value for the Cylinder Height!"
                if post_data["Cylinder_r2"]:
                    Cylinder_Radius = float(post_data['Cylinder_r2'])
                else:
                    flag = 0
                    return "Please input value for the Cylinder Radius!"
                if flag == 1:
                    object_quantity += 1
                    Cylinder_Coordinates = [Cylinder_x,Cylinder_y,Cylinder_z]
                    Cylinder_Rotation = [Cylinder_Rotate_x,Cylinder_Rotate_y,Cylinder_Rotate_z]
                    Cylinder_Color = [Cylinder_Color_R,Cylinder_Color_G,Cylinder_Color_B]
                    OutputFile.Add_Cylinder(Cylinder_Coordinates,Cylinder_Height,Cylinder_Radius,Cylinder_Rotation,Cylinder_Color,Transparency2)
            
            #user choose to have a Cone
            elif post_data["Object2"]=="Cone":
                if post_data["Cone_x2"]:
                    Cone_x = float(post_data["Cone_x2"])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cone!"
                if post_data["Cone_y2"]:
                    Cone_y = float(post_data['Cone_y2'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone!"
                if post_data["Cone_z2"]:
                    Cone_z = float(post_data['Cone_z2'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone!"
                if post_data["Cone_rx2"]:
                    Cone_Rotate_x = float(post_data['Cone_rx2'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cone Rotation!"
                if post_data["Cone_ry2"]:
                    Cone_Rotate_y = float(post_data['Cone_ry2'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone Rotation!"
                if post_data["Cone_rz2"]:
                    Cone_Rotate_z = float(post_data['Cone_rz2'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone Rotation!"
                if post_data["Cone_cr2"]:
                    Cone_Color_R = float(post_data['Cone_cr2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cg2"]:
                    Cone_Color_G = float(post_data['Cone_cg2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cb2"]:
                    Cone_Color_B = float(post_data['Cone_cb2'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_h2"]:
                    Cone_Height = float(post_data['Cone_h2'])
                else:
                    flag = 0
                    return "Please input value for the Cone Height!"
                if post_data["Cone_r2"]:
                    Cone_Radius = float(post_data['Cone_r2'])
                else:
                    flag = 0
                    return "Please input value for the Cone Radius!"
                if flag == 1:
                    object_quantity += 1
                    Cone_Coordinates = [Cone_x,Cone_y,Cone_z]
                    Cone_Rotation = [Cone_Rotate_x,Cone_Rotate_y,Cone_Rotate_z]
                    Cone_Color = [Cone_Color_R,Cone_Color_G,Cone_Color_B]
                    OutputFile.Add_Cone(Cone_Coordinates,Cone_Height,Cone_Radius,Cone_Rotation,Cone_Color,Transparency2)
            else:
                return "Input did not complete!"
        elif object_quantity_web>1:
            return "Please select the second object! "


#  Third Object
        if 'Object3' in post_data:
            flag = 1 # If user fills in all the blank for this object, otherwise flag == 0.
            Transparency3 = int(post_data["Transparency3"])
            # user choose to have a Sphere
            if post_data["Object3"]=="Sphere":
                if post_data["Sphere_x3"]:
                    Sphere_x = float(post_data['Sphere_x3']) 
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Sphere!" 
                if post_data["Sphere_y3"]:
                    Sphere_y = float(post_data['Sphere_y3'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Sphere!"
                if post_data["Sphere_z3"]:
                    Sphere_z = float(post_data['Sphere_z3'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Sphere!"
                if post_data["Sphere_cr3"]:
                    Sphere_Color_R = float(post_data['Sphere_cr3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cg3"]:
                    Sphere_Color_G = float(post_data['Sphere_cg3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cb3"]:
                    Sphere_Color_B = float(post_data['Sphere_cb3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_r3"]:
                    Sphere_Radius = float(post_data["Sphere_r3"])
                else:
                    flag = 0
                    return "Please input the radius of the Sphere!"
                if flag == 1:
                    object_quantity += 1
                    Sphere_Coordinates = [Sphere_x,Sphere_y,Sphere_z]
                    Sphere_Color = [Sphere_Color_R,Sphere_Color_G,Sphere_Color_B]
                    OutputFile.Add_Sphere(Sphere_Coordinates,Sphere_Radius,Sphere_Color,Transparency3)
            
            # user choose to have a Cube
            elif post_data["Object3"]=="Cube":
                if post_data["Cube_x3"]:
                    Cube_x = float(post_data['Cube_x3'])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cube!"
                if post_data["Cube_y3"]:
                    Cube_y = float(post_data['Cube_y3'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube!"
                if post_data["Cube_z3"]:
                    Cube_z = float(post_data['Cube_z3'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube!"
                if post_data["Cube_l3"]:
                    Cube_SideLength = float(post_data['Cube_l3'])
                else:
                    flag = 0
                    return "Please input value for the Cube Side Length!"
                if post_data["Cube_cr3"]:
                    Cube_Color_R = float(post_data['Cube_cr3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cg3"]:
                    Cube_Color_G = float(post_data['Cube_cg3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cb3"]:
                    Cube_Color_B = float(post_data['Cube_cb3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_rx3"]:
                    Cube_Rotate_x = float(post_data['Cube_rx3'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cube Rotation!"
                if post_data["Cube_ry3"]:
                    Cube_Rotate_y = float(post_data['Cube_ry3'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube Rotation!"
                if post_data["Cube_rz3"]:
                    Cube_Rotate_z = float(post_data['Cube_rz3'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube Rotation!"
                if flag == 1:
                    object_quantity += 1
                    Cube_Coordinates = [Cube_x,Cube_y,Cube_z]
                    Cube_Rotation = [Cube_Rotate_x,Cube_Rotate_y,Cube_Rotate_z]
                    Cube_Color = [Cube_Color_R,Cube_Color_G,Cube_Color_B]
                    OutputFile.Add_Cube(Cube_Coordinates,Cube_SideLength,Cube_Rotation,Cube_Color,Transparency3)
            
            #user choose to have a Tetrahedron
            elif post_data["Object3"]=="Tetrahedron":
                if post_data["Tetrahedron_x3"]:
                    Tetrahedron_x = float(post_data['Tetrahedron_x3'])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_y3"]:
                    Tetrahedron_y = float(post_data['Tetrahedron_y3'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_z3"]:
                    Tetrahedron_z = float(post_data['Tetrahedron_z3'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_l3"]:
                    Tetrahedron_SideLength = float(post_data['Tetrahedron_l3'])
                else:
                    flag = 0
                    return "Please input value for the Tetrahedron Side Length!"
                if post_data["Tetrahedron_cr3"]:
                    Tetrahedron_Color_R = float(post_data['Tetrahedron_cr3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cg3"]:
                    Tetrahedron_Color_G = float(post_data['Tetrahedron_cg3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cb3"]:
                    Tetrahedron_Color_B = float(post_data['Tetrahedron_cb3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_rx3"]:
                    Tetrahedron_Rotate_x = float(post_data['Tetrahedron_rx3'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_ry3"]:
                    Tetrahedron_Rotate_y = float(post_data['Tetrahedron_ry3'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_rz3"]:
                    Tetrahedron_Rotate_z = float(post_data['Tetrahedron_rz3'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Rotation!"
                if flag == 1:
                    object_quantity += 1
                    Tetrahedron_Coordinates = [Tetrahedron_x,Tetrahedron_y,Tetrahedron_z]
                    Tetrahedron_Rotation = [Tetrahedron_Rotate_x,Tetrahedron_Rotate_y,Tetrahedron_Rotate_z]
                    Tetrahedron_Color = [Tetrahedron_Color_R,Tetrahedron_Color_G,Tetrahedron_Color_B]
                    OutputFile.Add_Tetrahedron(Tetrahedron_Coordinates,Tetrahedron_SideLength,Tetrahedron_Rotation,Tetrahedron_Color,Transparency3)
            
            #user choose to have a Cylinder
            elif post_data["Object3"]=="Cylinder":
                if post_data["Cylinder_x3"]:
                    Cylinder_x = float(post_data["Cylinder_x3"])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cylinder!"
                if post_data["Cylinder_y3"]:
                    Cylinder_y = float(post_data['Cylinder_y3'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder!"
                if post_data["Cylinder_z3"]:
                    Cylinder_z = float(post_data['Cylinder_z3'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder!"
                if post_data["Cylinder_rx3"]:
                    Cylinder_Rotate_x = float(post_data['Cylinder_rx3'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_ry3"]:
                    Cylinder_Rotate_y = float(post_data['Cylinder_ry3'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_rz3"]:
                    Cylinder_Rotate_z = float(post_data['Cylinder_rz3'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_cr3"]:
                    Cylinder_Color_R = float(post_data['Cylinder_cr3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cg3"]:
                    Cylinder_Color_G = float(post_data['Cylinder_cg3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cb3"]:
                    Cylinder_Color_B = float(post_data['Cylinder_cb3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_h3"]:
                    Cylinder_Height = float(post_data['Cylinder_h3'])
                else:
                    flag = 0
                    return "Please input value for the Cylinder Height!"
                if post_data["Cylinder_r3"]:
                    Cylinder_Radius = float(post_data['Cylinder_r3'])
                else:
                    flag = 0
                    return "Please input value for the Cylinder Radius!"
                if flag == 1:
                    object_quantity += 1
                    Cylinder_Coordinates = [Cylinder_x,Cylinder_y,Cylinder_z]
                    Cylinder_Rotation = [Cylinder_Rotate_x,Cylinder_Rotate_y,Cylinder_Rotate_z]
                    Cylinder_Color = [Cylinder_Color_R,Cylinder_Color_G,Cylinder_Color_B]
                    OutputFile.Add_Cylinder(Cylinder_Coordinates,Cylinder_Height,Cylinder_Radius,Cylinder_Rotation,Cylinder_Color,Transparency3)
            
            #user choose to have a Cone
            elif post_data["Object3"]=="Cone":
                if post_data["Cone_x3"]:
                    Cone_x = float(post_data["Cone_x3"])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cone!"
                if post_data["Cone_y3"]:
                    Cone_y = float(post_data['Cone_y3'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone!"
                if post_data["Cone_z3"]:
                    Cone_z = float(post_data['Cone_z3'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone!"
                if post_data["Cone_rx3"]:
                    Cone_Rotate_x = float(post_data['Cone_rx3'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cone Rotation!"
                if post_data["Cone_ry3"]:
                    Cone_Rotate_y = float(post_data['Cone_ry3'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone Rotation!"
                if post_data["Cone_rz3"]:
                    Cone_Rotate_z = float(post_data['Cone_rz3'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone Rotation!"
                if post_data["Cone_cr3"]:
                    Cone_Color_R = float(post_data['Cone_cr3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cg3"]:
                    Cone_Color_G = float(post_data['Cone_cg3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cb3"]:
                    Cone_Color_B = float(post_data['Cone_cb3'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_h3"]:
                    Cone_Height = float(post_data['Cone_h3'])
                else:
                    flag = 0
                    return "Please input value for the Cone Height!"
                if post_data["Cone_r3"]:
                    Cone_Radius = float(post_data['Cone_r3'])
                else:
                    flag = 0
                    return "Please input value for the Cone Radius!"
                if flag == 1:
                    object_quantity += 1
                    Cone_Coordinates = [Cone_x,Cone_y,Cone_z]
                    Cone_Rotation = [Cone_Rotate_x,Cone_Rotate_y,Cone_Rotate_z]
                    Cone_Color = [Cone_Color_R,Cone_Color_G,Cone_Color_B]
                    OutputFile.Add_Cone(Cone_Coordinates,Cone_Height,Cone_Radius,Cone_Rotation,Cone_Color,Transparency3)
            else:
                return "Input did not complete!"
        elif object_quantity_web>2:
            return "Please select the third object! "

#  Fourth Object
        if 'Object4' in post_data:
            flag = 1 # If user fills in all the blank for this object, otherwise flag == 0.
            Transparency4 = int(post_data["Transparency4"])
            # user choose to have a Sphere
            if post_data["Object4"]=="Sphere":
                if post_data["Sphere_x4"]:
                    Sphere_x = float(post_data['Sphere_x4']) 
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Sphere!"  
                if post_data["Sphere_y4"]:
                    Sphere_y = float(post_data['Sphere_y4'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Sphere!"
                if post_data["Sphere_z4"]:
                    Sphere_z = float(post_data['Sphere_z4'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Sphere!"
                if post_data["Sphere_cr4"]:
                    Sphere_Color_R = float(post_data['Sphere_cr4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cg4"]:
                    Sphere_Color_G = float(post_data['Sphere_cg4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cb4"]:
                    Sphere_Color_B = float(post_data['Sphere_cb4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_r4"]:
                    Sphere_Radius = float(post_data["Sphere_r4"])
                else:
                    flag = 0
                    return "Please input the radius of the Sphere!"
                if flag == 1:
                    object_quantity += 1
                    Sphere_Coordinates = [Sphere_x,Sphere_y,Sphere_z]
                    Sphere_Color = [Sphere_Color_R,Sphere_Color_G,Sphere_Color_B]
                    OutputFile.Add_Sphere(Sphere_Coordinates,Sphere_Radius,Sphere_Color,Transparency4)
            
            # user choose to have a Cube
            elif post_data["Object4"]=="Cube":
                if post_data["Cube_x4"]:
                    Cube_x = float(post_data['Cube_x4'])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cube!"
                if post_data["Cube_y4"]:
                    Cube_y = float(post_data['Cube_y4'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube!"
                if post_data["Cube_z4"]:
                    Cube_z = float(post_data['Cube_z4'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube!"
                if post_data["Cube_l4"]:
                    Cube_SideLength = float(post_data['Cube_l4'])
                else:
                    flag = 0
                    return "Please input value for the Cube Side Length!"
                if post_data["Cube_cr4"]:
                    Cube_Color_R = float(post_data['Cube_cr4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cg4"]:
                    Cube_Color_G = float(post_data['Cube_cg4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cb4"]:
                    Cube_Color_B = float(post_data['Cube_cb4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_rx4"]:
                    Cube_Rotate_x = float(post_data['Cube_rx4'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cube Rotation!"
                if post_data["Cube_ry4"]:
                    Cube_Rotate_y = float(post_data['Cube_ry4'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube Rotation!"
                if post_data["Cube_rz4"]:
                    Cube_Rotate_z = float(post_data['Cube_rz4'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube Rotation!"
                if flag == 1:
                    object_quantity += 1
                    Cube_Coordinates = [Cube_x,Cube_y,Cube_z]
                    Cube_Rotation = [Cube_Rotate_x,Cube_Rotate_y,Cube_Rotate_z]
                    Cube_Color = [Cube_Color_R,Cube_Color_G,Cube_Color_B]
                    OutputFile.Add_Cube(Cube_Coordinates,Cube_SideLength,Cube_Rotation,Cube_Color,Transparency4)
            
            #user choose to have a Tetrahedron
            elif post_data["Object4"]=="Tetrahedron":
                if post_data["Tetrahedron_x4"]:
                    Tetrahedron_x = float(post_data['Tetrahedron_x4'])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_y4"]:
                    Tetrahedron_y = float(post_data['Tetrahedron_y4'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_z4"]:
                    Tetrahedron_z = float(post_data['Tetrahedron_z4'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_l4"]:
                    Tetrahedron_SideLength = float(post_data['Tetrahedron_l4'])
                else:
                    flag = 0
                    return "Please input value for the Tetrahedron Side Length!"
                if post_data["Tetrahedron_cr4"]:
                    Tetrahedron_Color_R = float(post_data['Tetrahedron_cr4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cg4"]:
                    Tetrahedron_Color_G = float(post_data['Tetrahedron_cg4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cb4"]:
                    Tetrahedron_Color_B = float(post_data['Tetrahedron_cb4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_rx4"]:
                    Tetrahedron_Rotate_x = float(post_data['Tetrahedron_rx4'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_ry4"]:
                    Tetrahedron_Rotate_y = float(post_data['Tetrahedron_ry4'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_rz4"]:
                    Tetrahedron_Rotate_z = float(post_data['Tetrahedron_rz4'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Rotation!"
                if flag == 1:
                    object_quantity += 1
                    Tetrahedron_Coordinates = [Tetrahedron_x,Tetrahedron_y,Tetrahedron_z]
                    Tetrahedron_Rotation = [Tetrahedron_Rotate_x,Tetrahedron_Rotate_y,Tetrahedron_Rotate_z]
                    Tetrahedron_Color = [Tetrahedron_Color_R,Tetrahedron_Color_G,Tetrahedron_Color_B]
                    OutputFile.Add_Tetrahedron(Tetrahedron_Coordinates,Tetrahedron_SideLength,Tetrahedron_Rotation,Tetrahedron_Color,Transparency4)
            
            #user choose to have a Cylinder
            elif post_data["Object4"]=="Cylinder":
                if post_data["Cylinder_x4"]:
                    Cylinder_x = float(post_data["Cylinder_x4"])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cylinder!"
                if post_data["Cylinder_y4"]:
                    Cylinder_y = float(post_data['Cylinder_y4'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder!"
                if post_data["Cylinder_z4"]:
                    Cylinder_z = float(post_data['Cylinder_z4'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder!"
                if post_data["Cylinder_rx4"]:
                    Cylinder_Rotate_x = float(post_data['Cylinder_rx4'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_ry4"]:
                    Cylinder_Rotate_y = float(post_data['Cylinder_ry4'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_rz4"]:
                    Cylinder_Rotate_z = float(post_data['Cylinder_rz4'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_cr4"]:
                    Cylinder_Color_R = float(post_data['Cylinder_cr4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cg4"]:
                    Cylinder_Color_G = float(post_data['Cylinder_cg4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cb4"]:
                    Cylinder_Color_B = float(post_data['Cylinder_cb4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_h4"]:
                    Cylinder_Height = float(post_data['Cylinder_h4'])
                else:
                    flag = 0
                    return "Please input value for the Cylinder Height!"
                if post_data["Cylinder_r4"]:
                    Cylinder_Radius = float(post_data['Cylinder_r4'])
                else:
                    flag = 0
                    return "Please input value for the Cylinder Radius!"
                if flag == 1:
                    object_quantity += 1
                    Cylinder_Coordinates = [Cylinder_x,Cylinder_y,Cylinder_z]
                    Cylinder_Rotation = [Cylinder_Rotate_x,Cylinder_Rotate_y,Cylinder_Rotate_z]
                    Cylinder_Color = [Cylinder_Color_R,Cylinder_Color_G,Cylinder_Color_B]
                    OutputFile.Add_Cylinder(Cylinder_Coordinates,Cylinder_Height,Cylinder_Radius,Cylinder_Rotation,Cylinder_Color,Transparency4)
            
            #user choose to have a Cone
            elif post_data["Object4"]=="Cone":
                if post_data["Cone_x4"]:
                    Cylinder_x = float(post_data["Cone_x4"])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cone!"
                if post_data["Cone_y4"]:
                    Cone_y = float(post_data['Cone_y4'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone!"
                if post_data["Cone_z4"]:
                    Cone_z = float(post_data['Cone_z4'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone!"
                if post_data["Cone_rx4"]:
                    Cone_Rotate_x = float(post_data['Cone_rx4'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cone Rotation!"
                if post_data["Cone_ry4"]:
                    Cone_Rotate_y = float(post_data['Cone_ry4'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone Rotation!"
                if post_data["Cone_rz4"]:
                    Cone_Rotate_z = float(post_data['Cone_rz4'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone Rotation!"
                if post_data["Cone_cr4"]:
                    Cone_Color_R = float(post_data['Cone_cr4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cg4"]:
                    Cone_Color_G = float(post_data['Cone_cg4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cb4"]:
                    Cone_Color_B = float(post_data['Cone_cb4'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_h4"]:
                    Cone_Height = float(post_data['Cone_h4'])
                else:
                    flag = 0
                    return "Please input value for the Cone Height!"
                if post_data["Cone_r4"]:
                    Cone_Radius = float(post_data['Cone_r4'])
                else:
                    flag = 0
                    return "Please input value for the Cone Radius!"
                if flag == 1:
                    object_quantity += 1
                    Cone_Coordinates = [Cone_x,Cone_y,Cone_z]
                    Cone_Rotation = [Cone_Rotate_x,Cone_Rotate_y,Cone_Rotate_z]
                    Cone_Color = [Cone_Color_R,Cone_Color_G,Cone_Color_B]
                    OutputFile.Add_Cone(Cone_Coordinates,Cone_Height,Cone_Radius,Cone_Rotation,Cone_Color,Transparency4)
            else:
                return "Input did not complete!"
        elif object_quantity_web>3:
            return "Please select the Fourth object! "

#  Fifth Object
        if 'Object5' in post_data:
            flag = 1 # If user fills in all the blank for this object, otherwise flag == 0.
            Transparency5 = int(post_data["Transparency5"])
            # user choose to have a Sphere
            if post_data["Object5"]=="Sphere":
                if post_data["Sphere_x5"]:
                    Sphere_x = float(post_data['Sphere_x5']) 
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Sphere!"   
                if post_data["Sphere_y5"]:
                    Sphere_y = float(post_data['Sphere_y5'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Sphere!"
                if post_data["Sphere_z5"]:
                    Sphere_z = float(post_data['Sphere_z5'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Sphere!"
                if post_data["Sphere_cr5"]:
                    Sphere_Color_R = float(post_data['Sphere_cr5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cg5"]:
                    Sphere_Color_G = float(post_data['Sphere_cg5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cb5"]:
                    Sphere_Color_B = float(post_data['Sphere_cb5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_r5"]:
                    Sphere_Radius = float(post_data["Sphere_r5"])
                else:
                    flag = 0
                    return "Please input the radius of the Sphere!"
                if flag == 1:
                    object_quantity += 1
                    Sphere_Coordinates = [Sphere_x,Sphere_y,Sphere_z]
                    Sphere_Color = [Sphere_Color_R,Sphere_Color_G,Sphere_Color_B]
                    OutputFile.Add_Sphere(Sphere_Coordinates,Sphere_Radius,Sphere_Color,Transparency5)
            
            # user choose to have a Cube
            elif post_data["Object5"]=="Cube":
                if post_data["Cube_x5"]:
                    Cube_x = float(post_data['Cube_x5'])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cube!"
                if post_data["Cube_y5"]:
                    Cube_y = float(post_data['Cube_y5'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube!"
                if post_data["Cube_z5"]:
                    Cube_z = float(post_data['Cube_z5'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube!"
                if post_data["Cube_l5"]:
                    Cube_SideLength = float(post_data['Cube_l5'])
                else:
                    flag = 0
                    return "Please input value for the Cube Side Length!"
                if post_data["Cube_cr5"]:
                    Cube_Color_R = float(post_data['Cube_cr5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cg5"]:
                    Cube_Color_G = float(post_data['Cube_cg5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cb5"]:
                    Cube_Color_B = float(post_data['Cube_cb5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_rx5"]:
                    Cube_Rotate_x = float(post_data['Cube_rx5'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cube Rotation!"
                if post_data["Cube_ry5"]:
                    Cube_Rotate_y = float(post_data['Cube_ry5'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube Rotation!"
                if post_data["Cube_rz5"]:
                    Cube_Rotate_z = float(post_data['Cube_rz5'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube Rotation!"
                if flag == 1:
                    object_quantity += 1
                    Cube_Coordinates = [Cube_x,Cube_y,Cube_z]
                    Cube_Rotation = [Cube_Rotate_x,Cube_Rotate_y,Cube_Rotate_z]
                    Cube_Color = [Cube_Color_R,Cube_Color_G,Cube_Color_B]
                    OutputFile.Add_Cube(Cube_Coordinates,Cube_SideLength,Cube_Rotation,Cube_Color,Transparency5)
            
            #user choose to have a Tetrahedron
            elif post_data["Object5"]=="Tetrahedron":
                if post_data["Tetrahedron_x5"]:
                    Tetrahedron_x = float(post_data['Tetrahedron_x5'])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_y5"]:
                    Tetrahedron_y = float(post_data['Tetrahedron_y5'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_z5"]:
                    Tetrahedron_z = float(post_data['Tetrahedron_z5'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_l5"]:
                    Tetrahedron_SideLength = float(post_data['Tetrahedron_l5'])
                else:
                    flag = 0
                    return "Please input value for the Tetrahedron Side Length!"
                if post_data["Tetrahedron_cr5"]:
                    Tetrahedron_Color_R = float(post_data['Tetrahedron_cr5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cg5"]:
                    Tetrahedron_Color_G = float(post_data['Tetrahedron_cg5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cb5"]:
                    Tetrahedron_Color_B = float(post_data['Tetrahedron_cb5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_rx5"]:
                    Tetrahedron_Rotate_x = float(post_data['Tetrahedron_rx5'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_ry5"]:
                    Tetrahedron_Rotate_y = float(post_data['Tetrahedron_ry5'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_rz5"]:
                    Tetrahedron_Rotate_z = float(post_data['Tetrahedron_rz5'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Rotation!"
                if flag == 1:
                    object_quantity += 1
                    Tetrahedron_Coordinates = [Tetrahedron_x,Tetrahedron_y,Tetrahedron_z]
                    Tetrahedron_Rotation = [Tetrahedron_Rotate_x,Tetrahedron_Rotate_y,Tetrahedron_Rotate_z]
                    Tetrahedron_Color = [Tetrahedron_Color_R,Tetrahedron_Color_G,Tetrahedron_Color_B]
                    OutputFile.Add_Tetrahedron(Tetrahedron_Coordinates,Tetrahedron_SideLength,Tetrahedron_Rotation,Tetrahedron_Color,Transparency5)
            
            #user choose to have a Cylinder
            elif post_data["Object5"]=="Cylinder":
                if post_data["Cylinder_x5"]:
                    Cylinder_x = float(post_data["Cylinder_x5"])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cylinder!"
                if post_data["Cylinder_y5"]:
                    Cylinder_y = float(post_data['Cylinder_y5'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder!"
                if post_data["Cylinder_z5"]:
                    Cylinder_z = float(post_data['Cylinder_z5'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder!"
                if post_data["Cylinder_rx5"]:
                    Cylinder_Rotate_x = float(post_data['Cylinder_rx5'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_ry5"]:
                    Cylinder_Rotate_y = float(post_data['Cylinder_ry5'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_rz5"]:
                    Cylinder_Rotate_z = float(post_data['Cylinder_rz5'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_cr5"]:
                    Cylinder_Color_R = float(post_data['Cylinder_cr5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cg5"]:
                    Cylinder_Color_G = float(post_data['Cylinder_cg5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cb5"]:
                    Cylinder_Color_B = float(post_data['Cylinder_cb5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_h5"]:
                    Cylinder_Height = float(post_data['Cylinder_h5'])
                else:
                    flag = 0
                    return "Please input value for the Cylinder Height!"
                if post_data["Cylinder_r5"]:
                    Cylinder_Radius = float(post_data['Cylinder_r5'])
                else:
                    flag = 0
                    return "Please input value for the Cylinder Radius!"
                if flag == 1:
                    object_quantity += 1
                    Cylinder_Coordinates = [Cylinder_x,Cylinder_y,Cylinder_z]
                    Cylinder_Rotation = [Cylinder_Rotate_x,Cylinder_Rotate_y,Cylinder_Rotate_z]
                    Cylinder_Color = [Cylinder_Color_R,Cylinder_Color_G,Cylinder_Color_B]
                    OutputFile.Add_Cylinder(Cylinder_Coordinates,Cylinder_Height,Cylinder_Radius,Cylinder_Rotation,Cylinder_Color,Transparency5)
            
            #user choose to have a Cone
            elif post_data["Object5"]=="Cone":
                if post_data["Cone_x5"]:
                    Cone_x = float(post_data["Cone_x5"])
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cone!"
                if post_data["Cone_y5"]:
                    Cone_y = float(post_data['Cone_y5'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone!"
                if post_data["Cone_z5"]:
                    Cone_z = float(post_data['Cone_z5'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone!"
                if post_data["Cone_rx5"]:
                    Cone_Rotate_x = float(post_data['Cone_rx5'])
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cone Rotation!"
                if post_data["Cone_ry5"]:
                    Cone_Rotate_y = float(post_data['Cone_ry5'])
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone Rotation!"
                if post_data["Cone_rz5"]:
                    Cone_Rotate_z = float(post_data['Cone_rz5'])
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone Rotation!"
                if post_data["Cone_cr5"]:
                    Cone_Color_R = float(post_data['Cone_cr5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cg5"]:
                    Cone_Color_G = float(post_data['Cone_cg5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cb5"]:
                    Cone_Color_B = float(post_data['Cone_cb5'])
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_h5"]:
                    Cone_Height = float(post_data['Cone_h5'])
                else:
                    flag = 0
                    return "Please input value for the Cone Height!"
                if post_data["Cone_r5"]:
                    Cone_Radius = float(post_data['Cone_r5'])
                else:
                    flag = 0
                    return "Please input value for the Cone Radius!"
                if flag == 1:
                    object_quantity += 1
                    Cone_Coordinates = [Cone_x,Cone_y,Cone_z]
                    Cone_Rotation = [Cone_Rotate_x,Cone_Rotate_y,Cone_Rotate_z]
                    Cone_Color = [Cone_Color_R,Cone_Color_G,Cone_Color_B]
                    OutputFile.Add_Cone(Cone_Coordinates,Cone_Height,Cone_Radius,Cone_Rotation,Cone_Color,Transparency5)
            else:
                return "Input did not complete!"
        elif object_quantity_web>4:
            return "Please select the fifth object! "

    if int(object_quantity) == int(object_quantity_web):
        return "Object saved successfully!"


@app.route('/File_Generate', methods=['POST', 'GET'])
def File_Generate():
    if request.method == 'POST':
        flag = request.form["flag"]
    if flag == "1":
        global OutputFile
        # OutputFile.print_num_of_object()
        OutputFile.Generate_File()
        return "Grey_Hats"
    else:
        return "404"


if __name__ == '__main__':
    app.run()