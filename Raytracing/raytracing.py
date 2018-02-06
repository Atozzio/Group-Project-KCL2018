"""
MIT License

Copyright (c) 2017 Cyrille Rossant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp

def normalize(x):
    x /= np.linalg.norm(x)
    return x

def intersect_plane(O, D, P, N):
    # Return the distance from O to the intersection of the ray (O, D) with the
    # plane (P, N), or +inf if there is no intersection.
    # O and P are 3D points, D and N (normal) are normalized vectors.
    denom = np.dot(D, N)
    if np.abs(denom) < 1e-6:
        return np.inf
    d = np.dot(P - O, N) / denom
    if d < 0:
        return np.inf
    return d

def intersect_sphere(O, D, S, R):
    # Return the distance from O to the intersection of the ray (O, D) with the
    # sphere (S, R), or +inf if there is no intersection.
    # O and S are 3D points, D (direction) is a normalized vector, R is a
    # scalar.
    a = np.dot(D, D)
    OS = O - S
    b = 2 * np.dot(D, OS)
    c = np.dot(OS, OS) - R * R
    disc = b * b - 4 * a * c
    if disc > 0:
        distSqrt = np.sqrt(disc)
        q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
        t0 = (-b - distSqrt) / 2.0 / a
        t1 = (-b + distSqrt) / 2.0 / a
        t0, t1 = min(t0, t1), max(t0, t1)
        if t1 >= 0:
            return t1 if t0 < 0 else t0
    return np.inf

def intersect_triangle(O, D, PS):
        dist = np.inf
        for i, plane in enumerate(PS):
            p_dist = intersect_plane(O, D, plane[0], plane[3])
            if p_dist != np.inf:
                if PointinTriangle(plane[0], plane[1], plane[2], O + D * p_dist):
                    dist = min(dist,p_dist)
        return dist

def PointinTriangle(point_1, point_2, point_3, M):
        v0 = point_3 - point_1 
        v1 = point_2 - point_1 
        v2 = M - point_1

        dot00 = np.dot(v0, v0) 
        dot01 = np.dot(v0, v1)
        dot02 = np.dot(v0, v2)
        dot11 = np.dot(v1, v1)
        dot12 = np.dot(v1, v2)

        inverDeno = 1 / ((dot00 * dot11) - (dot01 * dot01))
        u = ((dot11 * dot02) - (dot01 * dot12)) * inverDeno
        if u < 0 or u > 1: # if u out of range, return directly
            return False 

        v = ((dot00 * dot12) - (dot01 * dot02)) * inverDeno
        if v < 0 or v > 1: # if v out of range, return directly
            return False 
        return u + v <= 1

def intersect(O, D, obj):
    if obj['type'] == 'plane':
        return intersect_plane(O, D, obj['position'], obj['normal'])
    elif obj['type'] == 'sphere':
        return intersect_sphere(O, D, obj['position'], obj['radius'])
    elif obj['type'] == 'triangle':
        return intersect_triangle(O, D, obj['triangle_plane'])

def get_normal(obj, M):
    # Find normal.
    if obj['type'] == 'sphere':
        N = normalize(M - obj['position'])
    elif obj['type'] == 'plane':
        N = obj['normal']
    elif obj['type'] == 'triangle':
        for i, plane in enumerate(obj['triangle_plane']):
            if abs(np.dot(M - plane[0],plane[3])) < 0.000000000000001:
                N = plane[3]
    return N
    
def check_normal_direction(O,N,P):

    if  np.dot(P - O, N) < 0:
        return N
    else:
        return N * -1

def get_color(obj, M):
    color = obj['color']
    if not hasattr(color, '__len__'):
        color = color(M)
    return color

def trace_ray(rayO, rayD):
    # Find first point of intersection with the scene.
    t = np.inf
    for i, obj in enumerate(scene):
        t_obj = intersect(rayO, rayD, obj)
        if t_obj < t:
            t, obj_idx = t_obj, i
    # Return None if the ray does not intersect any object.
    if t == np.inf:
        return
    # Find the object.
    obj = scene[obj_idx]
    # Find the point of intersection on the object.
    M = rayO + rayD * t
    # Find properties of the object.
    N = get_normal(obj, M)
    color = get_color(obj, M)
    toL = normalize(L - M)
    toO = normalize(O - M)
    # Shadow: find if the point is shadowed or not.
    l = [intersect(M + N * .0001, toL, obj_sh) 
            for k, obj_sh in enumerate(scene) if k != obj_idx]
    if l and min(l) < np.inf:
        return
    # Start computing the color.
    col_ray = ambient
    # Lambert shading (diffuse).
    col_ray += obj.get('diffuse_c', diffuse_c) * max(np.dot(N, toL), 0) * color
    # Blinn-Phong shading (specular).
    col_ray += obj.get('specular_c', specular_c) * max(np.dot(N, normalize(toL + toO)), 0) ** specular_k * color_light
    return obj, M, N, col_ray

def add_sphere(position, radius, color):
    return dict(type='sphere', position=np.array(position), 
        radius=np.array(radius), color=np.array(color), reflection=.5)
    
def add_plane(position, normal):
    return dict(type='plane', position=np.array(position), 
        normal=np.array(normal),
        color=lambda M: (color_plane0 
            if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2) else color_plane1),
        diffuse_c=.75, specular_c=.5, reflection=.25)
    
#determine a triangl by giving the position of 4 nodes and color
def add_triangle(position, color):
    
    triangle_plane = np.zeros((4,4,3))

    # 3 nodes determine a plane
    triangle_plane[0,0] = np.array(position[0])
    triangle_plane[0,1] = np.array(position[1])
    triangle_plane[0,2] = np.array(position[2])
    # normal vector of plane
    triangle_plane[0,3] = check_normal_direction(np.array(position[0]),normalize(np.cross(np.array(position[1]) - np.array(position[0]), 
                                                    np.array(position[2]) - np.array(position[0]))),np.array(position[3]))

    triangle_plane[1,0] = np.array(position[0])
    triangle_plane[1,1] = np.array(position[1])
    triangle_plane[1,2] = np.array(position[3])
    triangle_plane[1,3] = check_normal_direction(np.array(position[0]),normalize(np.cross(np.array(position[1]) - np.array(position[0]), 
                                                    np.array(position[3]) - np.array(position[0]))),np.array(position[2]))
    triangle_plane[2,0] = np.array(position[0])
    triangle_plane[2,1] = np.array(position[2])
    triangle_plane[2,2] = np.array(position[3])
    triangle_plane[2,3] = check_normal_direction(np.array(position[0]),normalize(np.cross(np.array(position[2]) - np.array(position[0]), 
                                                    np.array(position[3]) - np.array(position[0]))),np.array(position[1]))

    triangle_plane[3,0] = np.array(position[1])
    triangle_plane[3,1] = np.array(position[2])
    triangle_plane[3,2] = np.array(position[3])
    triangle_plane[3,3] = check_normal_direction(np.array(position[1]),normalize(np.cross(np.array(position[2]) - np.array(position[1]), 
                                                    np.array(position[3]) - np.array(position[1]))),np.array(position[0]))

    return dict(type='triangle', triangle_plane=triangle_plane, 
                color=np.array(color), reflection = 0.5)


def trace_ray_main(result_queue,x_start,x_end,y_start,y_end):
    img = np.zeros((h, w, 3))
    for i, x in enumerate(x_project[np.where(x_project == x_start)[0][0]:np.where(x_project == x_end)[0][0] + 1]):
        if i % 10 == 0:
            print(i / float(w) * 100, "%")
        for j, y in enumerate(y_project[np.where(y_project == y_start)[0][0]:np.where(y_project == y_end)[0][0] + 1]):
            col = np.zeros(3)
            col[:] = 0
            Q = np.array([0., 0., 0.])  # Camera pointing to.
            Q[:2] = (x, y)
            D = normalize(Q - O)
            depth = 0
            rayO, rayD = O, D
            reflection = 1.
            # Loop through initial and secondary rays.
            while depth < depth_max:
                traced = trace_ray(rayO, rayD)
                if not traced:
                    break
                obj, M, N, col_ray = traced
                # Reflection: create a new ray.
                rayO, rayD = M + N * .0001, normalize(rayD - 2 * np.dot(rayD, N) * N)
                depth += 1
                col += reflection * col_ray
                reflection *= obj.get('reflection', 1.)
            img[h - np.where(y_project == y)[0][0] - 1, np.where(x_project == x)[0][0], :] = np.clip(col, 0, 1)
    result_queue.put(img) 


w = 400
h = 300

# List of objects.
color_plane0 = 1. * np.ones(3)
color_plane1 = 0. * np.ones(3)
scene = [add_triangle(([0, -.5, 1.5],[0.8,-.5,1.5],[0.25,-.5,0.8],[0.25,0.4,0.75]), 
                        [1, 0.3, 0.25]),
            add_sphere([-.75, .1, 2.25], .6, [.5, .223, .5]),
            add_sphere([-2.75, .1, 3.5], .6, [1., .572, .184]),
            add_plane([0., -.5, 0.], [0., 1., 0.]),]

# Light position and color.
L = np.array([5., 5., -10.])
color_light = np.ones(3)

# Default light and material parameters.
ambient = .05
diffuse_c = 1.
specular_c = 1.
specular_k = 50

depth_max = 5  # Maximum number of light reflections.
col = np.zeros(3)  # Current color.
O = np.array([0., 0.35, -1.])  # Camera.
r = float(w) / h
# Screen coordinates: x0, y0, x1, y1.
S = (-1., -1. / r + .25, 1., 1. / r + .25)

x_project = np.linspace(S[0], S[2], w)

y_project = np.linspace(S[1], S[3], h)

processes_divided = 8
processes_x = x_project[0:len(x_project):round(len(x_project) / processes_divided)]
processes_y = y_project[0:len(y_project):round(len(y_project) / processes_divided)]

if processes_x[len(processes_x) - 1] != x_project[len(x_project) - 1]:
    processes_x = np.append(processes_x,x_project[len(x_project) - 1])

if processes_y[len(processes_y) - 1] != y_project[len(y_project) - 1]:
    processes_y = np.append(processes_y,y_project[len(y_project) - 1])

result_queue = mp.Queue()
ps = []

# Loop through all pixels.
for i in range(0, len(processes_x) - 1):
    #if i % 10 == 0:
        #print(i / float(w) * 100, "%")
    for j in range(0, len(processes_y) - 1):
        #trace_ray_main(i,x,j,y)
        # Create new threads
        x_start = processes_x[i] if i == 0 else x_project[np.where(x_project == processes_x[i])[0][0] + 1]
        x_end = processes_x[i + 1]
        y_start = processes_y[j] if j == 0 else y_project[np.where(y_project == processes_y[j])[0][0] + 1]
        y_end = processes_y[j + 1]
        ps.append(mp.Process(target=trace_ray_main,args=(result_queue,x_start,x_end,y_start,y_end,)))

if __name__ == '__main__':

    img = np.zeros((h, w, 3))
    l = []

    for p in ps:
            p.start()

    for i in range(len(ps)):
       img = img + result_queue.get()

    plt.imsave('fig.png', img)