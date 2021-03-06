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
import json
import math

class PositionType:
	IN, OUT = 1, -1

class ray():

    origin = None
    direction = None

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def trace_ray(self, scene):
        # Find first point of intersection with the scene.
        t = np.inf
        for i, obj in enumerate(scene):
            t_obj = intersect(self.origin, self.direction, obj)
            if t_obj < t:
                t, obj_idx = t_obj, i
        # Return None if the ray does not intersect any object.
        if t == np.inf:
            return
        # Find the object.
        obj = scene[obj_idx]
        # Find the point of intersection on the object.
        M =  self.origin + self.direction * t
        # Find properties of the object.
        N = get_normal(obj, M, self.origin)
        color = get_color(obj, M)
        toL = normalize(L - M)
        toO = normalize(self.origin - M)
        # Shadow: find if the point is shadowed or not.
        transparent_ratio = 1
        for k, obj_sh in enumerate(scene):
            if k != obj_idx:
                if intersect(M + N * .001, toL, obj_sh) < np.inf:
                    transparent_ratio *= 1- scene[k].get("reflection")

        #l = [intersect(M + N * .0001, toL, obj_sh)
        #for k, obj_sh in enumerate(scene) if k != obj_idx]
        #if l and min(l) < np.inf:
        #    return

        # Start computing the color.
        col_ray = ambient
        # Lambert shading (diffuse).
        col_ray += obj.get('diffuse_c', diffuse_c) * max(np.dot(N, toL), 0) * color
        # Blinn-Phong shading (specular).
        col_ray += obj.get('specular_c', specular_c) * max(np.dot(N, normalize(toL + toO)), 0) ** specular_k * color_light

        col_ray *= transparent_ratio**2

        return obj, M, N, col_ray

class triangle_plane():
    point_1 = None
    point_2 = None
    point_3 = None
    normal_vector = None

    def __init__(self, point_1, point_2, point_3):
        self.point_1 = point_1
        self.point_2 = point_2
        self.point_3 = point_3
        self.normal_vector = normalize(np.cross(point_2 - point_1, point_3 - point_1))

    def getReflectedNormalVector(self, raySource):
        if np.dot(self.point_1 - raySource, self.normal_vector) < 0:
            return self.normal_vector
        else:
            return -1 * self.normal_vector

    def intersection(self, O, D):
        dist = intersect_plane(O, D, self.point_1, self.normal_vector)
        if dist != np.inf:
            if PointinTriangle(self.point_1, self.point_2, self.point_3, O + D * dist):
                return dist
        return np.inf

    def check_on_plane(self, point):
        if abs(np.dot(point - self.point_1, self.normal_vector)) < 0.00000000001:
            if PointinTriangle(self.point_1, self.point_2, self.point_3, point):
                return True

        return False


class cube():
    position = None
    length = None
    rotation_angle = None
    triangle_planes = None

    def __init__(self, position, length, rotation_angle):

        self.position = position
        self.length = length
        self.rotation_angle = rotation_angle

        square = [[], [], [], [], [], []]
        self.triangle_planes = []

        x_n_vector = rotation_vector(np.array([1, 0, 0]) * self.length / 2, rotation_angle)
        y_n_vector = rotation_vector(np.array([0, 1, 0]) * self.length / 2, rotation_angle)
        z_n_vector = rotation_vector(np.array([0, 0, 1]) * self.length / 2, rotation_angle)

        # find 6 square plane of cube
        for i, x in enumerate([x_n_vector, -1 * x_n_vector]):
            for j, y in enumerate([y_n_vector, -1 * y_n_vector]):
                for k, z in enumerate([z_n_vector, -1 * z_n_vector]):
                    node = self.position + x + y + z
                    if i == 0:
                        square[0].append(node)
                    if i == 1:
                        square[1].append(node)
                    if j == 0:
                        square[2].append(node)
                    if j == 1:
                        square[3].append(node)
                    if k == 0:
                        square[4].append(node)
                    if k == 1:
                        square[5].append(node)

        # split each square plane to triangle plane
        for i, s in enumerate(square):
            self.triangle_planes = self.triangle_planes + split_square_to_triangle(s)

        for i, plane in enumerate(self.triangle_planes):
            if  np.dot(plane.point_1 - self.position, plane.normal_vector) < 0:
                self.triangle_planes[i].normal_vector *=-1

    def intersection(self, O, D):
        if intersect_sphere(O, D, self.position, np.sqrt(3) * self.length / 2) != np.inf:
            return intersect_TriangleSet(O, D, self.triangle_planes)
        else:
            return np.inf

    def getNormalVector(self, M):
        for i, triangle_plane in enumerate(self.triangle_planes):
            if abs(np.dot(M - triangle_plane.point_1,triangle_plane.normal_vector)) < 0.00000000001:
                return triangle_plane.normal_vector


class circle_plane():
    position = None
    radius = None
    normal_vector = None

    def __init__(self, position, radius, normal_vector):
        self.position = position
        self.radius = radius
        self.normal_vector = normal_vector

    def check_on_plane(self, point):

        if abs(np.dot(point - self.position, self.normal_vector)) < 0.00000000001:
            if (np.linalg.norm(point - self.position)) < self.radius:
                return True

        return False


class cylinder():
    type = 'cylinder'
    position = None
    height = None
    radius = None
    normal_vector = None
    color = None
    top_bottom_plane = None
    reflection = 0.5

    def __init__(self, position, height, radius, rotation_angle, color):
        self.position = np.array(position)
        self.height = height
        self.radius = radius
        self.normal_vector = rotation_vector(np.array([0, 1, 0]), np.array(rotation_angle))

        top_plane = circle_plane(self.position + self.normal_vector * (height / 2), radius, self.normal_vector)
        bottom_plane = circle_plane(self.position - self.normal_vector * (height / 2), radius, -1 * self.normal_vector)
        self.top_bottom_plane = [top_plane, bottom_plane]

    def intersection(self, O, D):
        dist = np.inf
        p = np.dot(D, self.normal_vector) * self.normal_vector - D
        q = self.position - O - np.dot(self.position - O, self.normal_vector) * self.normal_vector
        a = np.dot(p, p)
        b = 2 * np.dot(p, q)
        c = np.dot(q, q) - (self.radius) ** 2

        if a == 0:
            if b != 0:
                t0 = -1 * c / b
                if t0 > 0:
                    dist = t0
        else:
            disc = b * b - 4 * a * c
            if disc > 0:
                distSqrt = np.sqrt(disc)
                t0 = (-b - distSqrt) / 2.0 / a
                t1 = (-b + distSqrt) / 2.0 / a
                t0, t1 = min(t0, t1), max(t0, t1)
                if t1 >= 0:
                    if t0 < 0:
                        if (np.linalg.norm(O + D * t1 - self.position)) ** 2 < self.radius ** 2 + (
                                self.height / 2) ** 2:
                            dist = t1
                    else:
                        if (np.linalg.norm(O + D * t0 - self.position)) ** 2 < self.radius ** 2 + (
                                self.height / 2) ** 2:
                            dist = t0

        for i, plane in enumerate(self.top_bottom_plane):
            tmp_dist = intersect_plane(O, D, plane.position, plane.normal_vector)
            if tmp_dist < dist:
                if np.linalg.norm(O + tmp_dist * D - plane.position) <= plane.radius:
                    dist = tmp_dist

        return dist

    def getNormalVector(self, intersected_point):

        for i, cycle_palne in enumerate(self.top_bottom_plane):
            if cycle_palne.check_on_plane(intersected_point):
                return cycle_palne.normal_vector

        project_point = self.position - np.dot((self.position - intersected_point),
                                               self.normal_vector) * self.normal_vector
        return normalize(intersected_point - project_point)

class cone():
    type = 'cone'
    position = None
    height = None
    radius = None
    normal_vector = None
    color = None
    top_bottom_plane = None
    angel= None
    reflection = 0.5

    def __init__(self, position, height, radius, rotation_angle, color):
        self.position = np.array(position)
        self.height = height
        self.radius = radius
        self.angel = math.atan(radius / (height/2))
        self.normal_vector = rotation_vector(np.array([0, 1, 0]), np.array(rotation_angle))

        top_plane = circle_plane(self.position + self.normal_vector * (height / 2), 0.1, self.normal_vector)
        bottom_plane = circle_plane(self.position - self.normal_vector * (height / 2), radius, -1 * self.normal_vector)
        self.top_bottom_plane = [top_plane, bottom_plane]

    def intersection(self, O, D):
        dist = np.inf
        p = np.dot(D, self.normal_vector) * self.normal_vector - D
        q = self.position - O - np.dot(self.position - O, self.normal_vector) * self.normal_vector
        a = math.cos(self.angel)**2 *np.dot(p, p) - math.sin(self.angel)**2 * (np.dot(D, self.normal_vector)**2)
        b = 2 * math.cos(self.angel)**2 * np.dot(p, q) - 2* math.sin(self.angel)**2 * np.dot(D,self.normal_vector)*np.dot((self.position-O),self.normal_vector)
        c = math.cos(self.angel)**2 * np.dot(q, q) -  math.sin(self.angel)**2 * (np.dot(self.position-O,self.normal_vector)**2)

        if a == 0:
            if b != 0:
                t0 = -1 * c / b
                if t0 > 0:
                    dist = t0
        else:
            disc = b * b - 4 * a * c
            if disc > 0:
                distSqrt = np.sqrt(disc)
                t0 = (-b - distSqrt) / 2.0 / a
                t1 = (-b + distSqrt) / 2.0 / a
                t0, t1 = min(t0, t1), max(t0, t1)
                if t1 >= 0:
                    if t0 < 0:
                        if (np.linalg.norm(O + D * t1 - self.position)) ** 2 < self.radius ** 2 + (
                                self.height / 2) ** 2:
                            dist = t1
                    else:
                        if (np.linalg.norm(O + D * t0 - self.position)) ** 2 < self.radius ** 2 + (
                                self.height / 2) ** 2:
                            dist = t0

        for i, plane in enumerate(self.top_bottom_plane):
            tmp_dist = intersect_plane(O, D, plane.position, plane.normal_vector)
            if tmp_dist < dist:
                if np.linalg.norm(O + tmp_dist * D - plane.position) <= plane.radius:
                    dist = tmp_dist

        return dist

    def getNormalVector(self, intersected_point):

        for i, cycle_palne in enumerate(self.top_bottom_plane):
            if cycle_palne.check_on_plane(intersected_point):
                return cycle_palne.normal_vector

        project_point = self.position - np.dot((self.position - intersected_point),
                                               self.normal_vector) * self.normal_vector
        return normalize(intersected_point - project_point)


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


def intersect_TriangleSet(O, D, triangle_planes):
    dist = np.inf
    for i, triangle_plane in enumerate(triangle_planes):
        dist = min(dist, triangle_plane.intersection(O, D))
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
    if u < 0 or u > 1:  # if u out of range, return directly
        return False

    v = ((dot00 * dot12) - (dot01 * dot02)) * inverDeno
    if v < 0 or v > 1:  # if v out of range, return directly
        return False
    return u + v <= 1


def intersect(O, D, obj):
    if obj['type'] == 'plane':
        return intersect_plane(O, D, obj['position'], obj['normal'])
    elif obj['type'] == 'sphere':
        return intersect_sphere(O, D, obj['position'], obj['radius'])
    elif obj['type'] == 'cylinder':
        return obj['obj'].intersection(O, D)
    elif obj['type'] == 'cone':
        return obj['obj'].intersection(O, D)
    elif obj['type'] == 'cube':
        return obj['obj'].intersection(O, D)
    else:
        return intersect_TriangleSet(O, D, obj['triangle_planes'])


def get_normal(obj, M, O):

    # Find normal.
    if obj['type'] == 'sphere':
        N = normalize(M - obj['position'])
    elif obj['type'] == 'plane':
        N = obj['normal']
    elif obj['type'] == 'cylinder':
        N = obj['obj'].getNormalVector(M)
    elif obj['type'] == 'cone':
        N = obj['obj'].getNormalVector(M)
    elif obj['type'] == 'cube':
        N = obj['obj'].getNormalVector(M)
    else:
        for i, triangle_plane in enumerate(obj['triangle_planes']):
            if abs(np.dot(M - triangle_plane.point_1, triangle_plane.normal_vector)) < 0.00000000001:
                N = triangle_plane.getReflectedNormalVector(O)
    return N


def check_normal_direction(O, N, P):
    if np.dot(P - O, N) < 0:
        return N
    else:
        return N * -1


def get_color(obj, M):
    color = obj['color']
    if not hasattr(color, '__len__'):
        color = color(M)
    return color

def add_sphere(position, radius, color):
    return dict(type='sphere', position=np.array(position),
                radius=np.array(radius), color=np.array(color), reflection=.5, refractive_indices= 1.1)


def add_plane(position, normal):
    return dict(type='plane', position=np.array(position),
                normal=np.array(normal),
                color=lambda M: (color_plane0
                                 if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2) else color_plane1),
                diffuse_c=.75, specular_c=.5, reflection=.25, refractive_indices= 4)


# determine a triangl by giving the position of 4 nodes and color
def add_tetrahedron(position, color):
    # 3 nodes determine a plane, total 4 planes
    triangle_planes = [triangle_plane(np.array(position[0]), np.array(position[1]), np.array(position[2])),
                       triangle_plane(np.array(position[0]), np.array(position[1]), np.array(position[3])),
                       triangle_plane(np.array(position[0]), np.array(position[2]), np.array(position[3])),
                       triangle_plane(np.array(position[1]), np.array(position[2]), np.array(position[3])), ]

    return dict(type='tetrahedron', triangle_planes=triangle_planes,
                color=np.array(color), reflection=0.5, refractive_indices= 1.1)


# determine a cube by giving the centre position, length, rotation angle, and
# color
# split cube to 12 triangle_plane
def add_cube(position, length, rotation_angle, color):
    return dict(type='cube', obj=cube(np.array(position), length, np.array(rotation_angle)),
                color=np.array(color), reflection=0.5, refractive_indices= 1.05)


def add_cylinder(poisition, height, radius, rotation_angle, color):
    return dict(type='cylinder', obj=cylinder(poisition, height, radius, rotation_angle, color),
                color=np.array(color), reflection=0.5, refractive_indices= 1.05)

def add_cone(poisition, height, radius, rotation_angle, color):
    return dict(type='cone', obj=cone(poisition, height, radius, rotation_angle, color),
                color=np.array(color), reflection=0.5, refractive_indices= 1.05)

# split square plane to two triangle plane
def split_square_to_triangle(square_vertex):
    triangle_vertex = np.zeros((2, 3, 3))

    # choose first three nodes as first triangle plane
    triangle_plane_1 = triangle_plane(np.array(square_vertex[0]), np.array(square_vertex[1]),
                                      np.array(square_vertex[2]))

    max_dis = 0
    max_index = 0
    tmp_vertex = []

    for i in range(3):
        dis = np.linalg.norm(square_vertex[i] - square_vertex[3])
        if dis > max_dis:
            max_dis = dis
            max_index = i

    # choose forth node and other two closer nodes as second triangle plane
    for i in range(4):
        if i != max_index:
            tmp_vertex.append(square_vertex[i])

    triangle_plane_2 = triangle_plane(np.array(tmp_vertex[0]), np.array(tmp_vertex[1]), np.array(tmp_vertex[2]))

    return [triangle_plane_1, triangle_plane_2]


# rotate a node base on given center node with specific x-axis, y-asix, z-axis
# angle
def rotation(node, r_centre, r_angle):
    angle = r_angle * np.pi / 180
    r_x = np.matrix([[1, 0, 0], [0, np.cos(angle[0]), np.sin(angle[0] * -1)], [0, np.sin(angle[0]), np.cos(angle[0])]])
    r_y = np.matrix([[np.cos(angle[1]), 0, np.sin(angle[1])], [0, 1, 0], [np.sin(angle[1]) * -1, 0, np.cos(angle[1])]])
    r_z = np.matrix([[np.cos(angle[2]), np.sin(angle[2]) * -1, 0], [np.sin(angle[2]), np.cos(angle[2]), 0], [0, 0, 1]])

    tmp_node = node - r_centre
    r_node = np.matmul(r_z, np.matmul(r_y, np.matmul(r_x, (np.matrix([[tmp_node[0]], [tmp_node[1]], [tmp_node[2]]])))))

    return np.array([r_node.item(0), r_node.item(1), r_node.item(2)]) + r_centre


def rotation_vector(vector, r_angle):
    return rotation(vector, np.array([0, 0, 0]), r_angle)


#trace ray of pixel in given area
def trace_ray_main(result_queue,x_start,x_end,y_start,y_end, scene_input):
    img = np.zeros((h, w, 3))
    scene = analyse_input(scene_input)
    for i, x in enumerate(x_project[np.where(x_project == x_start)[0][0]:np.where(x_project == x_end)[0][0] + 1]):
        for j, y in enumerate(y_project[np.where(y_project == y_start)[0][0]:np.where(y_project == y_end)[0][0] + 1]):
            col = np.zeros(3)
            col[:] = 0
            Q = np.array([0., 0., 0.])  # Camera pointing to.
            Q[:2] = (x, y)
            D = normalize(Q - O)
            depth = 0
            primaryRay = ray(O, D)

            col = reflect_and_refract(primaryRay, scene, PositionType.OUT, depth, 1,i,j)

            img[h - np.where(y_project == y)[0][0] - 1, np.where(x_project == x)[0][0], :] = np.clip(col, 0, 1)
    result_queue.put(img)

def reflect_and_refract(primaryRay, scene, positionType, depth, pathLoss, i,j):

    traced = primaryRay.trace_ray(scene)

    if not traced:
        return 0. * np.zeros(3)

    obj, M, N, col_ray = traced

    if np.dot(primaryRay.direction, N) < 0:
        positionType = PositionType.OUT
        col = pathLoss * col_ray
        n1 = 1
        n2 = obj.get('refractive_indices')
        newNormal = N
    else:
        positionType = PositionType.IN
        newNormal = N * -1
        col = np.zeros(3)
        n2 = 1
        n1 = obj.get('refractive_indices')

    # Reflection Ray
    reflectAmount = fresnel (n1, n2, newNormal, primaryRay.direction)

    reflectRay = ray( M + newNormal * .001, normalize(primaryRay.direction - 2 * np.dot(primaryRay.direction, newNormal) * newNormal))

    if depth+1 < depth_max:
        col+= reflect_and_refract(reflectRay, scene, positionType, depth+1, pathLoss*reflectAmount, i,j)

    refractionAmount = 1 - reflectAmount

    # Refraction Ray
    if depth+1 < depth_max and refractionAmount > 0:
            refractionRay = refraction(primaryRay, positionType, newNormal, obj, M)
            if refractionRay is not None:
                col+= reflect_and_refract(refractionRay, scene, positionType, depth+1, pathLoss*refractionAmount, i,j)

    return col

def refraction(primaryRay, positionType, normal, refraction_obj, refraction_point):

    r = 1 / refraction_obj.get('refractive_indices')

    if  positionType == PositionType.IN:
        r = 1/r

    c1 = abs(np.dot(normal, primaryRay.direction))
    t = 1- r**2 * (1-c1**2)

    if t < 0:
        return None
    else:
        c2 = np.sqrt(t)

    T = normalize(r * primaryRay.direction + (r*c1 - c2) * normal)

    refraction_ray = ray(refraction_point + 0.001 * normal * -1, T)

    return refraction_ray

def fresnel(n1, n2, normal, incident) :

    cosi = abs(np.dot(incident, normal))
    # Compute sini using Snell's law

    sint = n1 / n2 * np.sqrt(1 - cosi **2)
    # Total internal reflection
    if sint >= 1 :
        kr = 1;

    else :
        cost = np.sqrt(1 - sint * sint)
        Rs = ((n2 * cosi) - (n1 * cost)) / ((n2 * cosi) + (n1 * cost))
        Rp = ((n1 * cosi) - (n2 * cost)) / ((n1 * cosi) + (n2 * cost))
        kr = (Rs * Rs + Rp * Rp) / 2

    return kr

def analyse_input(scene_input):

    data = json.loads(scene_input)
    scene = []

    for key in data.keys():
        if key == 'tetrahedron':
            for _ in range(len(data[key])):
                position1 = data[key][_]['position1']
                position2 = data[key][_]['position2']
                position3 = data[key][_]['position3']
                position4 = data[key][_]['position4']
                position = tuple()
                position = tuple((position1,)) + (position2,) + (position3,) + (position4,)
                color = data[key][_]['color']
                scene.append(add_tetrahedron(position, color))

        elif key == 'cube':
            for _ in range(len(data[key])):
                position = data[key][_]['position']
                length = data[key][_]['length']
                rotation_angle = data[key][_]['rotation_angle']
                color = data[key][_]['color']
                scene.append(add_cube(position,length,rotation_angle,color))

        elif key == 'cylinder':
            for _ in range(len(data[key])):
                position = data[key][_]['position']
                height = data[key][_]['height']
                radius = data[key][_]['radius']
                color = data[key][_]['color']
                scene.append(add_cylinder(position, height, radius, rotation_angle, color))

        elif key == 'cone':
            for _ in range(len(data[key])):
                position = data[key][_]['position']
                height = data[key][_]['height']
                radius = data[key][_]['radius']
                color = data[key][_]['color']
                scene.append(add_cone(position, height, radius, rotation_angle, color))

        elif key == 'sphere':
            for _ in range(len(data[key])):
                position = data[key][_]['position']
                radius = data[key][_]['radius']
                color = data[key][_]['color']
                scene.append(add_sphere(position, radius, color))

        elif key == 'plane':
            for _ in range(len(data[key])):
                position = data[key][_]['position']
                normal = data[key][_]['normal']
                scene.append(add_plane(position, normal))

    return scene

w = 400
h = 300

# List of objects.
color_plane0 = 1. * np.ones(3)
color_plane1 = 0. * np.ones(3)

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


if __name__ == '__main__':

    with open('data.json', 'r') as inputFile:
        scene_input = inputFile.read()

    # divide project plane to multiple smaller plane
    processes_divided = 8

    # find divided point
    processes_x = x_project[0:len(x_project):round(len(x_project) / processes_divided)]
    processes_y = y_project[0:len(y_project):round(len(y_project) / processes_divided)]

    if processes_x[len(processes_x) - 1] != x_project[len(x_project) - 1]:
        processes_x = np.append(processes_x, x_project[len(x_project) - 1])

    if processes_y[len(processes_y) - 1] != y_project[len(y_project) - 1]:
        processes_y = np.append(processes_y, y_project[len(y_project) - 1])

    result_queue = mp.Queue()
    ps = []

    # Create new processes to trace ray on given area
    for i in range(0, len(processes_x) - 1):
        for j in range(0, len(processes_y) - 1):
            x_start = processes_x[i] if i == 0 else x_project[np.where(x_project == processes_x[i])[0][0] + 1]
            x_end = processes_x[i + 1]
            y_start = processes_y[j] if j == 0 else y_project[np.where(y_project == processes_y[j])[0][0] + 1]
            y_end = processes_y[j + 1]
            ps.append(mp.Process(target=trace_ray_main, args=(result_queue, x_start, x_end, y_start, y_end, scene_input, )))

    img = np.zeros((h, w, 3))

    # start processes
    for p in ps:
        p.start()

    for i in range(len(ps)):
        img = img + result_queue.get()
        print((i + 1) / len(ps) * 100, '%')

    # for debug
    #trace_ray_main(result_queue,S[0], S[2],S[1], S[3], scene_input)
    #img = img + result_queue.get()

    plt.imsave('Fiigure.png', img)
