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
        try:
            Plane_Position_X = float(post_data['Plane_Position_X'])
            Plane_Position_Y = float(post_data['Plane_Position_Y'])
            Plane_Position_Z = float(post_data['Plane_Position_Z'])
        except:
            return "Please enter ONLY numbers for Plane Position!"
        
    #Plane Normal Vector
        try:
            Plane_Normal_X = float(post_data['Plane_Normal_X'])
            Plane_Normal_Y = float(post_data['Plane_Normal_Y'])
            Plane_Normal_Z = float(post_data['Plane_Normal_Z'])
        except:
            return "Please enter ONLY numbers for Plane Normal Vector!"
    #Plane Transparency
        Plane_Transparency = int(post_data['Plane_Transparency'])
    #Camera Coordinates
        try:
            Camera_C_X = float(post_data['Camera_C_X'])
            Camera_C_Y = float(post_data['Camera_C_Y'])
            Camera_C_Z = float(post_data['Camera_C_Z'])
        except:
            return "Please enter ONLY numbers for Camera Coordinates!"
    #Camera Looking Point
        try:
            Camera_L_X = float(post_data['Camera_C_X'])
            Camera_L_Y = float(post_data['Camera_C_Y'])
            Camera_L_Z = float(post_data['Camera_C_Z'])
        except:
            return "Please enter ONLY numbers for Camera Looking Points"
    #Light source
        try:
            Light_X = float(post_data['Light_X'])
            Light_Y = float(post_data['Light_Y'])
            Light_Z = float(post_data['Light_Z'])
        except:
            return "Please enter ONLY numbers for Camera Looking Points" 
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
                    try:
                        Sphere_x = float(post_data['Sphere_x1']) 
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Sphere!"
                if post_data["Sphere_y1"]:
                    try:
                        Sphere_y = float(post_data['Sphere_y1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Sphere!"
                if post_data["Sphere_z1"]:
                    try:
                        Sphere_z = float(post_data['Sphere_z1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Sphere!"
                if post_data["Sphere_cr1"]:
                    try:
                        Sphere_Color_R = float(post_data['Sphere_cr1'])/255
                        if Sphere_Color_R < 0 or Sphere_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cg1"]:
                    try:
                        Sphere_Color_G = float(post_data['Sphere_cg1'])/255
                        if Sphere_Color_G < 0 or Sphere_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cb1"]:
                    try:
                        Sphere_Color_B = float(post_data['Sphere_cb1'])/255
                        if Sphere_Color_B < 0 or Sphere_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_r1"]:
                    try:
                        Sphere_Radius = float(post_data["Sphere_r1"])
                    except:
                        return "Please enter ONLY numbers for the first object!"
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
                    try:
                        Cube_x = float(post_data['Cube_x1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cube!"
                if post_data["Cube_y1"]:
                    try:
                        Cube_y = float(post_data['Cube_y1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube!"
                if post_data["Cube_z1"]:
                    try:
                        Cube_z = float(post_data['Cube_z1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube!"
                if post_data["Cube_l1"]:
                    try:
                        Cube_SideLength = float(post_data['Cube_l1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for the Cube Side Length!"
                if post_data["Cube_cr1"]:
                    try:
                        Cube_Color_R = float(post_data['Cube_cr1'])/255
                        if Cube_Color_R < 0 or Cube_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cg1"]:
                    try:
                        Cube_Color_G = float(post_data['Cube_cg1'])/255
                        if Cube_Color_G < 0 or Cube_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cb1"]:
                    try:
                        Cube_Color_B = float(post_data['Cube_cb1'])/255
                        if Cube_Color_B < 0 or Cube_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_rx1"]:
                    try:
                        Cube_Rotate_x = float(post_data['Cube_rx1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cube Rotation!"
                if post_data["Cube_ry1"]:
                    try:
                        Cube_Rotate_y = float(post_data['Cube_ry1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube Rotation!"
                if post_data["Cube_rz1"]:
                    try:
                        Cube_Rotate_z = float(post_data['Cube_rz1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
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
                    try:
                        Tetrahedron_x = float(post_data['Tetrahedron_x1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_y1"]:
                    try:
                        Tetrahedron_y = float(post_data['Tetrahedron_y1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_z1"]:
                    try:
                        Tetrahedron_z = float(post_data['Tetrahedron_z1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_l1"]:
                    try:
                        Tetrahedron_SideLength = float(post_data['Tetrahedron_l1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for the Tetrahedron Side Length!"
                if post_data["Tetrahedron_cr1"]:
                    try:
                        Tetrahedron_Color_R = float(post_data['Tetrahedron_cr1'])/255
                        if Tetrahedron_Color_R < 0 or Tetrahedron_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cg1"]:
                    try:
                        Tetrahedron_Color_G = float(post_data['Tetrahedron_cg1'])/255
                        if Tetrahedron_Color_G < 0 or Tetrahedron_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cb1"]:
                    try:
                        Tetrahedron_Color_B = float(post_data['Tetrahedron_cb1'])/255
                        if Tetrahedron_Color_B < 0 or Tetrahedron_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_rx1"]:
                    try:
                        Tetrahedron_Rotate_x = float(post_data['Tetrahedron_rx1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_ry1"]:
                    try:
                        Tetrahedron_Rotate_y = float(post_data['Tetrahedron_ry1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_rz1"]:
                    try:
                        Tetrahedron_Rotate_z = float(post_data['Tetrahedron_rz1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
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
                    try:
                        Cylinder_x = float(post_data["Cylinder_x1"])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cylinder!"
                if post_data["Cylinder_y1"]:
                    try:
                        Cylinder_y = float(post_data['Cylinder_y1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder!"
                if post_data["Cylinder_z1"]:
                    try:
                        Cylinder_z = float(post_data['Cylinder_z1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder!"
                if post_data["Cylinder_rx1"]:
                    try:
                        Cylinder_Rotate_x = float(post_data['Cylinder_rx1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_ry1"]:
                    try:
                        Cylinder_Rotate_y = float(post_data['Cylinder_ry1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_rz1"]:
                    try:
                        Cylinder_Rotate_z = float(post_data['Cylinder_rz1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_cr1"]:
                    try:
                        Cylinder_Color_R = float(post_data['Cylinder_cr1'])/255
                        if Cylinder_Color_R < 0 or Cylinder_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cg1"]:
                    try:
                        Cylinder_Color_G = float(post_data['Cylinder_cg1'])/255
                        if Cylinder_Color_G < 0 or Cylinder_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cb1"]:
                    try:
                        Cylinder_Color_B = float(post_data['Cylinder_cb1'])/255
                        if Cylinder_Color_B < 0 or Cylinder_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_h1"]:
                    try:
                        Cylinder_Height = float(post_data['Cylinder_h1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for the Cylinder Height!"
                if post_data["Cylinder_r1"]:
                    try:
                        Cylinder_Radius = float(post_data['Cylinder_r1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
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
                    try:
                        Cone_x = float(post_data["Cone_x1"])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cone!"
                if post_data["Cone_y1"]:
                    try:
                        Cone_y = float(post_data['Cone_y1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone!"
                if post_data["Cone_z1"]:
                    try:
                        Cone_z = float(post_data['Cone_z1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                    flag = 0
                    return "Please input value for Z coordinate of the Cone!"
                if post_data["Cone_rx1"]:
                    try:
                        Cone_Rotate_x = float(post_data['Cone_rx1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cone Rotation!"
                if post_data["Cone_ry1"]:
                    try:
                        Cone_Rotate_y = float(post_data['Cone_ry1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone Rotation!"
                if post_data["Cone_rz1"]:
                    try:
                        Cone_Rotate_z = float(post_data['Cone_rz1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone Rotation!"
                if post_data["Cone_cr1"]:
                    try:
                        Cone_Color_R = float(post_data['Cone_cr1'])/255
                        if Cone_Color_R < 0 or Cone_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cg1"]:
                    try:
                        Cone_Color_G = float(post_data['Cone_cg1'])/255
                        if Cone_Color_G < 0 or Cone_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cb1"]:
                    try:
                        Cone_Color_B = float(post_data['Cone_cb1'])/255
                        if Cone_Color_B < 0 or Cone_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_h1"]:
                    try:
                        Cone_Height = float(post_data['Cone_h1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
                else:
                    flag = 0
                    return "Please input value for the Cone Height!"
                if post_data["Cone_r1"]:
                    try:
                        Cone_Radius = float(post_data['Cone_r1'])
                    except:
                        return "Please enter ONLY numbers for the first object!"
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
                    try:
                        Sphere_x = float(post_data['Sphere_x2']) 
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Sphere!"  
                if post_data["Sphere_y2"]:
                    try:
                        Sphere_y = float(post_data['Sphere_y2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Sphere!"
                if post_data["Sphere_z2"]:
                    try:
                        Sphere_z = float(post_data['Sphere_z2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Sphere!"
                if post_data["Sphere_cr2"]:
                    try:
                        Sphere_Color_R = float(post_data['Sphere_cr2'])/255
                        if Sphere_Color_R < 0 or Sphere_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cg2"]:
                    try:
                        Sphere_Color_G = float(post_data['Sphere_cg2'])/255
                        if Sphere_Color_G < 0 or Sphere_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cb2"]:
                    try:
                        Sphere_Color_B = float(post_data['Sphere_cb2'])/255
                        if Sphere_Color_B < 0 or Sphere_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_r2"]:
                    try:
                        Sphere_Radius = float(post_data["Sphere_r2"])
                    except:
                        return "Please enter ONLY numbers for the second object!"
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
                    try:
                        Cube_x = float(post_data['Cube_x2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cube!"
                if post_data["Cube_y2"]:
                    try:
                        Cube_y = float(post_data['Cube_y2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube!"
                if post_data["Cube_z2"]:
                    try:
                        Cube_z = float(post_data['Cube_z2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube!"
                if post_data["Cube_l2"]:
                    try:
                        Cube_SideLength = float(post_data['Cube_l2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for the Cube Side Length!"
                if post_data["Cube_cr2"]:
                    try:
                        Cube_Color_R = float(post_data['Cube_cr2'])/255
                        if Cube_Color_R < 0 or Cube_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cg2"]:
                    try:
                        Cube_Color_G = float(post_data['Cube_cg2'])/255
                        if Cube_Color_G < 0 or Cube_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cb2"]:
                    try:
                        Cube_Color_B = float(post_data['Cube_cb2'])/255
                        if Cube_Color_B < 0 or Cube_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_rx2"]:
                    try:
                        Cube_Rotate_x = float(post_data['Cube_rx2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cube Rotation!"
                if post_data["Cube_ry2"]:
                    try:
                        Cube_Rotate_y = float(post_data['Cube_ry2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube Rotation!"
                if post_data["Cube_rz2"]:
                    try:
                        Cube_Rotate_z = float(post_data['Cube_rz2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
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
                    try:
                        Tetrahedron_x = float(post_data['Tetrahedron_x2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_y2"]:
                    try:
                        Tetrahedron_y = float(post_data['Tetrahedron_y2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_z2"]:
                    try:
                        Tetrahedron_z = float(post_data['Tetrahedron_z2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_l2"]:
                    try:
                        Tetrahedron_SideLength = float(post_data['Tetrahedron_l2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for the Tetrahedron Side Length!"
                if post_data["Tetrahedron_cr2"]:
                    try:
                        Tetrahedron_Color_R = float(post_data['Tetrahedron_cr2'])/255
                        if Tetrahedron_Color_R < 0 or Tetrahedron_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cg2"]:
                    try:
                        Tetrahedron_Color_G = float(post_data['Tetrahedron_cg2'])/255
                        if Tetrahedron_Color_G < 0 or Tetrahedron_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cb2"]:
                    try:
                        Tetrahedron_Color_B = float(post_data['Tetrahedron_cb2'])/255
                        if Tetrahedron_Color_B < 0 or Tetrahedron_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_rx2"]:
                    try:
                        Tetrahedron_Rotate_x = float(post_data['Tetrahedron_rx2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_ry2"]:
                    try:
                        Tetrahedron_Rotate_y = float(post_data['Tetrahedron_ry2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_rz2"]:
                    try:
                        Tetrahedron_Rotate_z = float(post_data['Tetrahedron_rz2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
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
                    try:
                        Cylinder_x = float(post_data["Cylinder_x2"])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cylinder!"
                if post_data["Cylinder_y2"]:
                    try:
                        Cylinder_y = float(post_data['Cylinder_y2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder!"
                if post_data["Cylinder_z2"]:
                    try:
                        Cylinder_z = float(post_data['Cylinder_z2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder!"
                if post_data["Cylinder_rx2"]:
                    try:
                        Cylinder_Rotate_x = float(post_data['Cylinder_rx2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_ry2"]:
                    try:
                        Cylinder_Rotate_y = float(post_data['Cylinder_ry2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_rz2"]:
                    try:
                        Cylinder_Rotate_z = float(post_data['Cylinder_rz2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_cr2"]:
                    try:
                        Cylinder_Color_R = float(post_data['Cylinder_cr2'])/255
                        if Cylinder_Color_R < 0 or Cylinder_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cg2"]:
                    try:
                        Cylinder_Color_G = float(post_data['Cylinder_cg2'])/255
                        if Cylinder_Color_G < 0 or Cylinder_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cb2"]:
                    try:
                        Cylinder_Color_B = float(post_data['Cylinder_cb2'])/255
                        if Cylinder_Color_B < 0 or Cylinder_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_h2"]:
                    try:
                        Cylinder_Height = float(post_data['Cylinder_h2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for the Cylinder Height!"
                if post_data["Cylinder_r2"]:
                    try:
                        Cylinder_Radius = float(post_data['Cylinder_r2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
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
                    try:
                        Cone_x = float(post_data["Cone_x2"])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cone!"
                if post_data["Cone_y2"]:
                    try:
                        Cone_y = float(post_data['Cone_y2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone!"
                if post_data["Cone_z2"]:
                    try:
                        Cone_z = float(post_data['Cone_z2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone!"
                if post_data["Cone_rx2"]:
                    try:
                        Cone_Rotate_x = float(post_data['Cone_rx2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cone Rotation!"
                if post_data["Cone_ry2"]:
                    try:
                        Cone_Rotate_y = float(post_data['Cone_ry2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone Rotation!"
                if post_data["Cone_rz2"]:
                    try:
                        Cone_Rotate_z = float(post_data['Cone_rz2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone Rotation!"
                if post_data["Cone_cr2"]:
                    try:
                        Cone_Color_R = float(post_data['Cone_cr2'])/255
                        if Cone_Color_R < 0 or Cone_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cg2"]:
                    try:
                        Cone_Color_G = float(post_data['Cone_cg2'])/255
                        if Cone_Color_G < 0 or Cone_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cb2"]:
                    try:
                        Cone_Color_B = float(post_data['Cone_cb2'])/255
                        if Cone_Color_B < 0 or Cone_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_h2"]:
                    try:
                        Cone_Height = float(post_data['Cone_h2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
                else:
                    flag = 0
                    return "Please input value for the Cone Height!"
                if post_data["Cone_r2"]:
                    try:
                        Cone_Radius = float(post_data['Cone_r2'])
                    except:
                        return "Please enter ONLY numbers for the second object!"
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
                    try:
                        Sphere_x = float(post_data['Sphere_x3']) 
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Sphere!" 
                if post_data["Sphere_y3"]:
                    try:
                        Sphere_y = float(post_data['Sphere_y3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Sphere!"
                if post_data["Sphere_z3"]:
                    try:
                        Sphere_z = float(post_data['Sphere_z3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Sphere!"
                if post_data["Sphere_cr3"]:
                    try:
                        Sphere_Color_R = float(post_data['Sphere_cr3'])/255
                        if Sphere_Color_R < 0 or Sphere_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cg3"]:
                    try:
                        Sphere_Color_G = float(post_data['Sphere_cg3'])/255
                        if Sphere_Color_G < 0 or Sphere_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cb3"]:
                    try:
                        Sphere_Color_B = float(post_data['Sphere_cb3'])/255
                        if Sphere_Color_B < 0 or Sphere_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_r3"]:
                    try:
                        Sphere_Radius = float(post_data["Sphere_r3"])
                    except:
                        return "Please enter ONLY numbers for the third object!"
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
                    try:
                        Cube_x = float(post_data['Cube_x3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cube!"
                if post_data["Cube_y3"]:
                    try:
                        Cube_y = float(post_data['Cube_y3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube!"
                if post_data["Cube_z3"]:
                    try:
                        Cube_z = float(post_data['Cube_z3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube!"
                if post_data["Cube_l3"]:
                    try:
                        Cube_SideLength = float(post_data['Cube_l3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for the Cube Side Length!"
                if post_data["Cube_cr3"]:
                    try:
                        Cube_Color_R = float(post_data['Cube_cr3'])/255
                        if Cube_Color_R < 0 or Cube_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cg3"]:
                    try:
                        Cube_Color_G = float(post_data['Cube_cg3'])/255
                        if Cube_Color_G < 0 or Cube_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cb3"]:
                    try:
                        Cube_Color_B = float(post_data['Cube_cb3'])/255
                        if Cube_Color_B < 0 or Cube_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_rx3"]:
                    try:
                        Cube_Rotate_x = float(post_data['Cube_rx3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cube Rotation!"
                if post_data["Cube_ry3"]:
                    try:
                        Cube_Rotate_y = float(post_data['Cube_ry3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube Rotation!"
                if post_data["Cube_rz3"]:
                    try:
                        Cube_Rotate_z = float(post_data['Cube_rz3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
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
                    try:
                        Tetrahedron_x = float(post_data['Tetrahedron_x3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_y3"]:
                    try:
                        Tetrahedron_y = float(post_data['Tetrahedron_y3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_z3"]:
                    try:
                        Tetrahedron_z = float(post_data['Tetrahedron_z3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_l3"]:
                    try:
                        Tetrahedron_SideLength = float(post_data['Tetrahedron_l3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                    
                else:
                    flag = 0
                    return "Please input value for the Tetrahedron Side Length!"
                if post_data["Tetrahedron_cr3"]:
                    try:
                        Tetrahedron_Color_R = float(post_data['Tetrahedron_cr3'])/255
                        if Tetrahedron_Color_R < 0 or Tetrahedron_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cg3"]:
                    try:
                        Tetrahedron_Color_G = float(post_data['Tetrahedron_cg3'])/255
                        if Tetrahedron_Color_G < 0 or Tetrahedron_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cb3"]:
                    try:
                        Tetrahedron_Color_B = float(post_data['Tetrahedron_cb3'])/255
                        if Tetrahedron_Color_B < 0 or Tetrahedron_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_rx3"]:
                    try:
                        Tetrahedron_Rotate_x = float(post_data['Tetrahedron_rx3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_ry3"]:
                    try:
                        Tetrahedron_Rotate_y = float(post_data['Tetrahedron_ry3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_rz3"]:
                    try:
                        Tetrahedron_Rotate_z = float(post_data['Tetrahedron_rz3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
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
                    try:
                        Cylinder_x = float(post_data["Cylinder_x3"])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cylinder!"
                if post_data["Cylinder_y3"]:
                    try:
                        Cylinder_y = float(post_data['Cylinder_y3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder!"
                if post_data["Cylinder_z3"]:
                    try:
                        Cylinder_z = float(post_data['Cylinder_z3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder!"
                if post_data["Cylinder_rx3"]:
                    try:
                        Cylinder_Rotate_x = float(post_data['Cylinder_rx3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_ry3"]:
                    try:
                        Cylinder_Rotate_y = float(post_data['Cylinder_ry3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_rz3"]:
                    try:
                        Cylinder_Rotate_z = float(post_data['Cylinder_rz3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_cr3"]:
                    try:
                        Cylinder_Color_R = float(post_data['Cylinder_cr3'])/255
                        if Cylinder_Color_R < 0 or Cylinder_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cg3"]:
                    try:
                        Cylinder_Color_G = float(post_data['Cylinder_cg3'])/255
                        if Cylinder_Color_G < 0 or Cylinder_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cb3"]:
                    try:
                        Cylinder_Color_B = float(post_data['Cylinder_cb3'])/255
                        if Cylinder_Color_B < 0 or Cylinder_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_h3"]:
                    try:
                        Cylinder_Height = float(post_data['Cylinder_h3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for the Cylinder Height!"
                if post_data["Cylinder_r3"]:
                    try:
                        Cylinder_Radius = float(post_data['Cylinder_r3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
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
                    try:
                        Cone_x = float(post_data["Cone_x3"])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cone!"
                if post_data["Cone_y3"]:
                    try:
                        Cone_y = float(post_data['Cone_y3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone!"
                if post_data["Cone_z3"]:
                    try:
                        Cone_z = float(post_data['Cone_z3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone!"
                if post_data["Cone_rx3"]:
                    try:
                        Cone_Rotate_x = float(post_data['Cone_rx3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cone Rotation!"
                if post_data["Cone_ry3"]:
                    try:
                        Cone_Rotate_y = float(post_data['Cone_ry3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone Rotation!"
                if post_data["Cone_rz3"]:
                    try:
                        Cone_Rotate_z = float(post_data['Cone_rz3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone Rotation!"
                if post_data["Cone_cr3"]:
                    try:
                        Cone_Color_R = float(post_data['Cone_cr3'])/255
                        if Cone_Color_R < 0 or Cone_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cg3"]:
                    try:
                        Cone_Color_G = float(post_data['Cone_cg3'])/255
                        if Cone_Color_G < 0 or Cone_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cb3"]:
                    try:
                        Cone_Color_B = float(post_data['Cone_cb3'])/255
                        if Cone_Color_B < 0 or Cone_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_h3"]:
                    try:
                        Cone_Height = float(post_data['Cone_h3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
                else:
                    flag = 0
                    return "Please input value for the Cone Height!"
                if post_data["Cone_r3"]:
                    try:
                        Cone_Radius = float(post_data['Cone_r3'])
                    except:
                        return "Please enter ONLY numbers for the third object!"
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
                    try:
                        Sphere_x = float(post_data['Sphere_x4']) 
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Sphere!"  
                if post_data["Sphere_y4"]:
                    try:
                        Sphere_y = float(post_data['Sphere_y4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Sphere!"
                if post_data["Sphere_z4"]:
                    try:
                        Sphere_z = float(post_data['Sphere_z4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Sphere!"
                if post_data["Sphere_cr4"]:
                    try:
                        Sphere_Color_R = float(post_data['Sphere_cr4'])/255
                        if Sphere_Color_R < 0 or Sphere_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cg4"]:
                    try:
                        Sphere_Color_G = float(post_data['Sphere_cg4'])/255
                        if Sphere_Color_G < 0 or Sphere_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cb4"]:
                    try:
                        Sphere_Color_B = float(post_data['Sphere_cb4'])/255
                        if Sphere_Color_B < 0 or Sphere_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_r4"]:
                    try:
                        Sphere_Radius = float(post_data["Sphere_r4"])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
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
                    try:
                        Cube_x = float(post_data['Cube_x4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cube!"
                if post_data["Cube_y4"]:
                    try:
                        Cube_y = float(post_data['Cube_y4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube!"
                if post_data["Cube_z4"]:
                    try:
                        Cube_z = float(post_data['Cube_z4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube!"
                if post_data["Cube_l4"]:
                    try:
                        Cube_SideLength = float(post_data['Cube_l4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for the Cube Side Length!"
                if post_data["Cube_cr4"]:
                    try:
                        Cube_Color_R = float(post_data['Cube_cr4'])/255
                        if Cube_Color_R < 0 or Cube_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cg4"]:
                    try:
                        Cube_Color_G = float(post_data['Cube_cg4'])/255
                        if Cube_Color_G < 0 or Cube_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cb4"]:
                    try:
                        Cube_Color_B = float(post_data['Cube_cb4'])/255
                        if Cube_Color_B < 0 or Cube_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_rx4"]:
                    try:
                        Cube_Rotate_x = float(post_data['Cube_rx4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cube Rotation!"
                if post_data["Cube_ry4"]:
                    try:
                        Cube_Rotate_y = float(post_data['Cube_ry4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube Rotation!"
                if post_data["Cube_rz4"]:
                    try:
                        Cube_Rotate_z = float(post_data['Cube_rz4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
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
                    try:
                        Tetrahedron_x = float(post_data['Tetrahedron_x4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_y4"]:
                    try:
                        Tetrahedron_y = float(post_data['Tetrahedron_y4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_z4"]:
                    try:
                        Tetrahedron_z = float(post_data['Tetrahedron_z4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_l4"]:
                    try:
                        Tetrahedron_SideLength = float(post_data['Tetrahedron_l4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for the Tetrahedron Side Length!"
                if post_data["Tetrahedron_cr4"]:
                    try:
                        Tetrahedron_Color_R = float(post_data['Tetrahedron_cr4'])/255
                        if Tetrahedron_Color_R < 0 or Tetrahedron_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cg4"]:
                    try:
                        Tetrahedron_Color_G = float(post_data['Tetrahedron_cg4'])/255
                        if Tetrahedron_Color_G < 0 or Tetrahedron_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cb4"]:
                    try:
                        Tetrahedron_Color_B = float(post_data['Tetrahedron_cb4'])/255
                        if Tetrahedron_Color_B < 0 or Tetrahedron_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_rx4"]:
                    try:
                        Tetrahedron_Rotate_x = float(post_data['Tetrahedron_rx4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_ry4"]:
                    try:
                        Tetrahedron_Rotate_y = float(post_data['Tetrahedron_ry4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_rz4"]:
                    try:
                        Tetrahedron_Rotate_z = float(post_data['Tetrahedron_rz4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
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
                    try:
                        Cylinder_x = float(post_data["Cylinder_x4"])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cylinder!"
                if post_data["Cylinder_y4"]:
                    try:
                        Cylinder_y = float(post_data['Cylinder_y4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder!"
                if post_data["Cylinder_z4"]:
                    try:
                        Cylinder_z = float(post_data['Cylinder_z4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder!"
                if post_data["Cylinder_rx4"]:
                    try:
                        Cylinder_Rotate_x = float(post_data['Cylinder_rx4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_ry4"]:
                    try:
                        Cylinder_Rotate_y = float(post_data['Cylinder_ry4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_rz4"]:
                    try:
                        Cylinder_Rotate_z = float(post_data['Cylinder_rz4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_cr4"]:
                    try:
                        Cylinder_Color_R = float(post_data['Cylinder_cr4'])/255
                        if Cylinder_Color_R < 0 or Cylinder_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cg4"]:
                    try:
                        Cylinder_Color_G = float(post_data['Cylinder_cg4'])/255
                        if Cylinder_Color_G < 0 or Cylinder_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cb4"]:
                    try:
                        Cylinder_Color_B = float(post_data['Cylinder_cb4'])/255
                        if Cylinder_Color_B < 0 or Cylinder_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_h4"]:
                    try:
                        Cylinder_Height = float(post_data['Cylinder_h4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for the Cylinder Height!"
                if post_data["Cylinder_r4"]:
                    try:
                        Cylinder_Radius = float(post_data['Cylinder_r4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
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
                    try:
                        Cone_x = float(post_data["Cone_x4"])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cone!"
                if post_data["Cone_y4"]:
                    try:
                        Cone_y = float(post_data['Cone_y4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone!"
                if post_data["Cone_z4"]:
                    try:
                        Cone_z = float(post_data['Cone_z4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone!"
                if post_data["Cone_rx4"]:
                    try:
                        Cone_Rotate_x = float(post_data['Cone_rx4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cone Rotation!"
                if post_data["Cone_ry4"]:
                    try:
                        Cone_Rotate_y = float(post_data['Cone_ry4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone Rotation!"
                if post_data["Cone_rz4"]:
                    try:
                        Cone_Rotate_z = float(post_data['Cone_rz4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone Rotation!"
                if post_data["Cone_cr4"]:
                    try:
                        Cone_Color_R = float(post_data['Cone_cr4'])/255
                        if Cone_Color_R < 0 or Cone_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cg4"]:
                    try:
                        Cone_Color_G = float(post_data['Cone_cg4'])/255
                        if Cone_Color_G < 0 or Cone_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cb4"]:
                    try:
                        Cone_Color_B = float(post_data['Cone_cb4'])/255
                        if Cone_Color_B < 0 or Cone_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_h4"]:
                    try:
                        Cone_Height = float(post_data['Cone_h4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
                else:
                    flag = 0
                    return "Please input value for the Cone Height!"
                if post_data["Cone_r4"]:
                    try:
                        Cone_Radius = float(post_data['Cone_r4'])
                    except:
                        return "Please enter ONLY numbers for the fourth object!"
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
                    try:
                        Sphere_x = float(post_data['Sphere_x5']) 
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Sphere!"   
                if post_data["Sphere_y5"]:
                    try:
                        Sphere_y = float(post_data['Sphere_y5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Sphere!"
                if post_data["Sphere_z5"]:
                    try:
                        Sphere_z = float(post_data['Sphere_z5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Sphere!"
                if post_data["Sphere_cr5"]:
                    try:
                        Sphere_Color_R = float(post_data['Sphere_cr5'])/255
                        if Sphere_Color_R < 0 or Sphere_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cg5"]:
                    try:
                        Sphere_Color_G = float(post_data['Sphere_cg5'])/255
                        if Sphere_Color_G < 0 or Sphere_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_cb5"]:
                    try:
                        Sphere_Color_B = float(post_data['Sphere_cb5'])/255
                        if Sphere_Color_B < 0 or Sphere_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Sphere!"
                if post_data["Sphere_r5"]:
                    try:
                        Sphere_Radius = float(post_data["Sphere_r5"])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
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
                    try:
                        Cube_x = float(post_data['Cube_x5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cube!"
                if post_data["Cube_y5"]:
                    try:
                        Cube_y = float(post_data['Cube_y5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube!"
                if post_data["Cube_z5"]:
                    try:
                        Cube_z = float(post_data['Cube_z5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cube!"
                if post_data["Cube_l5"]:
                    try:
                        Cube_SideLength = float(post_data['Cube_l5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for the Cube Side Length!"
                if post_data["Cube_cr5"]:
                    try:
                        Cube_Color_R = float(post_data['Cube_cr5'])/255
                        if Cube_Color_R < 0 or Cube_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cg5"]:
                    try:
                        Cube_Color_G = float(post_data['Cube_cg5'])/255
                        if Cube_Color_G < 0 or Cube_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_cb5"]:
                    try:
                        Cube_Color_B = float(post_data['Cube_cb5'])/255
                        if Cube_Color_B < 0 or Cube_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cube!"
                if post_data["Cube_rx5"]:
                    try:
                        Cube_Rotate_x = float(post_data['Cube_rx5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cube Rotation!"
                if post_data["Cube_ry5"]:
                    try:
                        Cube_Rotate_y = float(post_data['Cube_ry5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cube Rotation!"
                if post_data["Cube_rz5"]:
                    try:
                        Cube_Rotate_z = float(post_data['Cube_rz5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
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
                    try:
                        Tetrahedron_x = float(post_data['Tetrahedron_x5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_y5"]:
                    try:
                        Tetrahedron_y = float(post_data['Tetrahedron_y5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_z5"]:
                    try:
                        Tetrahedron_z = float(post_data['Tetrahedron_z5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Tetrahedron Centre Point!"
                if post_data["Tetrahedron_l5"]:
                    try:
                        Tetrahedron_SideLength = float(post_data['Tetrahedron_l5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for the Tetrahedron Side Length!"
                if post_data["Tetrahedron_cr5"]:
                    try:
                        Tetrahedron_Color_R = float(post_data['Tetrahedron_cr5'])/255
                        if Tetrahedron_Color_R < 0 or Tetrahedron_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cg5"]:
                    try:
                        Tetrahedron_Color_G = float(post_data['Tetrahedron_cg5'])/255
                        if Tetrahedron_Color_G < 0 or Tetrahedron_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_cb5"]:
                    try:
                        Tetrahedron_Color_B = float(post_data['Tetrahedron_cb5'])/255
                        if Tetrahedron_Color_B < 0 or Tetrahedron_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                    
                else:
                    flag = 0
                    return "Please complete the color input of the Tetrahedron!"
                if post_data["Tetrahedron_rx5"]:
                    try:
                        Tetrahedron_Rotate_x = float(post_data['Tetrahedron_rx5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_ry5"]:
                    try:
                        Tetrahedron_Rotate_y = float(post_data['Tetrahedron_ry5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Tetrahedron Rotation!"
                if post_data["Tetrahedron_rz5"]:
                    try:
                        Tetrahedron_Rotate_z = float(post_data['Tetrahedron_rz5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
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
                    try:
                        Cylinder_x = float(post_data["Cylinder_x5"])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cylinder!"
                if post_data["Cylinder_y5"]:
                    try:
                        Cylinder_y = float(post_data['Cylinder_y5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder!"
                if post_data["Cylinder_z5"]:
                    try:
                        Cylinder_z = float(post_data['Cylinder_z5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder!"
                if post_data["Cylinder_rx5"]:
                    try:
                        Cylinder_Rotate_x = float(post_data['Cylinder_rx5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_ry5"]:
                    try:
                        Cylinder_Rotate_y = float(post_data['Cylinder_ry5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_rz5"]:
                    try:
                        Cylinder_Rotate_z = float(post_data['Cylinder_rz5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cylinder Rotation!"
                if post_data["Cylinder_cr5"]:
                    try:
                        Cylinder_Color_R = float(post_data['Cylinder_cr5'])/255
                        if Cylinder_Color_R < 0 or Cylinder_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cg5"]:
                    try:
                        Cylinder_Color_G = float(post_data['Cylinder_cg5'])/255
                        if Cylinder_Color_G < 0 or Cylinder_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_cb5"]:
                    try:
                        Cylinder_Color_B = float(post_data['Cylinder_cb5'])/255
                        if Cylinder_Color_B < 0 or Cylinder_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cylinder!"
                if post_data["Cylinder_h5"]:
                    try:
                        Cylinder_Height = float(post_data['Cylinder_h5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for the Cylinder Height!"
                if post_data["Cylinder_r5"]:
                    try:
                        Cylinder_Radius = float(post_data['Cylinder_r5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
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
                    try:
                        Cone_x = float(post_data["Cone_x5"])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return  "Please input value for X coordinate of the Cone!"
                if post_data["Cone_y5"]:
                    try:
                        Cone_y = float(post_data['Cone_y5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone!"
                if post_data["Cone_z5"]:
                    try:
                        Cone_z = float(post_data['Cone_z5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone!"
                if post_data["Cone_rx5"]:
                    try:
                        Cone_Rotate_x = float(post_data['Cone_rx5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for X coordinate of the Cone Rotation!"
                if post_data["Cone_ry5"]:
                    try:
                        Cone_Rotate_y = float(post_data['Cone_ry5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Y coordinate of the Cone Rotation!"
                if post_data["Cone_rz5"]:
                    try:
                        Cone_Rotate_z = float(post_data['Cone_rz5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for Z coordinate of the Cone Rotation!"
                if post_data["Cone_cr5"]:
                    try:
                        Cone_Color_R = float(post_data['Cone_cr5'])/255
                        if Cone_Color_R < 0 or Cone_Color_R > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cg5"]:
                    try:
                        Cone_Color_G = float(post_data['Cone_cg5'])/255
                        if Cone_Color_G < 0 or Cone_Color_G > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_cb5"]:
                    try:
                        Cone_Color_B = float(post_data['Cone_cb5'])/255
                        if Cone_Color_B < 0 or Cone_Color_B > 1:
                            return "Color should be between 0 and 255!"
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please complete the color input of the Cone!"
                if post_data["Cone_h5"]:
                    try:
                        Cone_Height = float(post_data['Cone_h5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
                else:
                    flag = 0
                    return "Please input value for the Cone Height!"
                if post_data["Cone_r5"]:
                    try:
                        Cone_Radius = float(post_data['Cone_r5'])
                    except:
                        return "Please enter ONLY numbers for the fifth object!"
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
    app.run(host='0.0.0.0')