from flask import Flask,request, render_template
from generate_output import OutputGenerator

app = Flask(__name__)
 
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

@app.route('/ObjectFeature', methods=['POST', 'GET'])
def ObjectFeature():
    OutputFile = OutputGenerator()
    if request.method == 'POST':
        if request.form["Sphere_x"]: 
        # user choose to have a sphere
            Sphere_x = float(request.form.get('Sphere_x', None))
            Sphere_y = float(request.form.get('Sphere_y', None))
            Sphere_z = float(request.form.get('Sphere_z', None))
            Sphere_Color_R = float(request.form.get('Sphere_cr', None))
            Sphere_Color_G = float(request.form.get('Sphere_cg', None))
            Sphere_Color_B = float(request.form.get('Sphere_cb', None))
            Sphere_Coordinates = [Sphere_x,Sphere_y,Sphere_z]
            Sphere_Radius = float(request.form["Sphere_r"])
            Sphere_Color = [Sphere_Color_R,Sphere_Color_G,Sphere_Color_B]
            OutputFile.Add_Sphere(Sphere_Coordinates,Sphere_Radius,Sphere_Color)

        elif request.form["Cube_x"]: 
        # user choose to have a cube
            Cube_x = float(request.form.get('Cube_x', None))
            Cube_y = float(request.form.get('Cube_y', None))
            Cube_z = float(request.form.get('Cube_z', None))
            Cube_Color_R = float(request.form.get('Cube_cr', None))
            Cube_Color_G = float(request.form.get('Cube_cg', None))
            Cube_Color_B = float(request.form.get('Cube_cb', None))
            Cube_Rotate_x = float(request.form.get('Cube_rx', None))
            Cube_Rotate_y = float(request.form.get('Cube_ry', None))
            Cube_Rotate_z = float(request.form.get('Cube_rz', None))
            Cube_Coordinates = [Cube_x,Cube_y,Cube_z]
            Cube_SideLength = float(request.form["Cube_l"])
            Cube_Rotation = [Cube_Rotate_x,Cube_Rotate_y,Cube_Rotate_z]
            Cube_Color = [Cube_Color_R,Cube_Color_G,Cube_Color_B]
            OutputFile.Add_Cube(Cube_Coordinates,Cube_SideLength,Cube_Rotation,Cube_Color)
        elif request.form["Tetrahedron_x1"]:
        #user choose to have a Tetrahedron
            Tetrahedron_x1 = request.form["Tetrahedron_x1"]
            Tetrahedron_y1 = request.form["Tetrahedron_y1"]
            Tetrahedron_z1 = request.form["Tetrahedron_z1"]
            Tetrahedron_x2 = request.form["Tetrahedron_x2"]
            Tetrahedron_y2 = request.form["Tetrahedron_y2"]
            Tetrahedron_z2 = request.form["Tetrahedron_z2"]
            Tetrahedron_x3 = request.form["Tetrahedron_x3"]
            Tetrahedron_y3 = request.form["Tetrahedron_y3"]
            Tetrahedron_z3 = request.form["Tetrahedron_z3"]
            Tetrahedron_x4 = request.form["Tetrahedron_x4"]
            Tetrahedron_y4 = request.form["Tetrahedron_y4"]
            Tetrahedron_z4 = request.form["Tetrahedron_z4"]
            Tetrahedron_Color_R = request.form["Tetrahedron_cr"]
            Tetrahedron_Color_G = request.form["Tetrahedron_cg"]
            Tetrahedron_Color_B = request.form["Tetrahedron_cb"]
            Tetrahedron_1st = [Tetrahedron_x1,Tetrahedron_y1,Tetrahedron_z1]
            Tetrahedron_2nd = [Tetrahedron_x2,Tetrahedron_y2,Tetrahedron_z2]
            Tetrahedron_3rd = [Tetrahedron_x3,Tetrahedron_y3,Tetrahedron_z3]
            Tetrahedron_4th = [Tetrahedron_x4,Tetrahedron_y4,Tetrahedron_z4]
            Tetrahedron_Color = [Tetrahedron_Color_R,Tetrahedron_Color_G,Tetrahedron_Color_B]
            OutputFile.Add_Tetrahedron(Tetrahedron_1st,Tetrahedron_2nd,Tetrahedron_3rd,Tetrahedron_4th,Tetrahedron_Color)
        elif request.form["Cylinder_x"]:
        #user choose to have a Cylinder
            Cylinder_x = request.form["Cylinder_x"]
            Cylinder_y = request.form["Cylinder_y"]
            Cylinder_z = request.form["Cylinder_z"]
            Cylinder_Rotate_x = request.form["Cylinder_rx"]
            Cylinder_Rotate_y = request.form["Cylinder_ry"]
            Cylinder_Rotate_z = request.form["Cylinder_rz"]
            Cylinder_Color_R = request.form["Cylinder_cr"]
            Cylinder_Color_G = request.form["Cylinder_cg"]
            Cylinder_Color_B = request.form["Cylinder_cb"]
            Cylinder_Coordinates = [Cylinder_x,Cylinder_y,Cylinder_z]
            Cylinder_Rotation = [Cylinder_Rotate_x,Cylinder_Rotate_y,Cylinder_Rotate_z]
            Cylinder_Color = [Cylinder_Color_R,Cylinder_Color_G,Cylinder_Color_B]
            Cylinder_Height = request.form["Cylinder_h"]
            Cylinder_Radius = request.form["Cylinder_r"]
            OutputFile.Add_Cylinder(Cylinder_Coordinates,Cylinder_Height,Cylinder_Radius,Cylinder_Rotation,Cylinder_Color)
        elif request.form["Cone_x"]:
        #user choose to have a Cone
            Cone_x = request.form["Cone_x"]
            Cone_y = request.form["Cone_y"]
            Cone_z = request.form["Cone_z"]
            Cone_Rotate_x = request.form["Cone_rx"]
            Cone_Rotate_y = request.form["Cone_ry"]
            Cone_Rotate_z = request.form["Cone_rz"]
            Cone_Color_R = request.form["Cone_cr"]
            Cone_Color_G = request.form["Cone_cg"]
            Cone_Color_B = request.form["Cone_cb"]
            Cone_Coordinates = [Cone_x,Cone_y,Cone_z]
            Cone_Rotation = [Cone_Rotate_x,Cone_Rotate_y,Cone_Rotate_z]
            Cone_Color = [Cone_Color_R,Cone_Color_G,Cone_Color_B]
            Cone_Height = request.form["Cone_h"]
            Cone_Radius = request.form["Cone_r"]
            OutputFile.Add_Cone(Cone_Coordinates,Cone_Height,Cone_Radius,Cone_Rotation,Cone_Color)
        else:
            return render_template('index.html')
        OutputFile.Generate_File()

    return render_template('ObjectFeature.html')

if __name__ == '__main__':
    app.run()