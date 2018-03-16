import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
import json
import math

class PositionType:
	IN, OUT = 1, -1

class camera():
    
    def __init__(self, position, point_to):
        self.position = np.array(position)
        self.point_to = np.array(point_to)
        self.project_plane_normal = normalize(self.point_to - self.position)
        self.project_centre = self.position + self.project_plane_normal
        self.project_blocks = []
        self.x_project_size = 2.0
        self.y_project_size = 2.0

        self.rotation = self.findRotation()
        x = np.matmul(self.rotation,np.array([1,0,0]))
        y = np.matmul(self.rotation,np.array([0,1,0]))
        self.x_coordinate_vector = np.array([x.item(0),x.item(1),x.item(2)])
        self.y_coordinate_vector = np.array([y.item(0),y.item(1),y.item(2)])

        self.project_start = self.project_centre - self.x_project_size / 2.0 * self.x_coordinate_vector - self.y_project_size / 2.0 * self.y_coordinate_vector

        self.x_project_size_pre_pixel = self.x_project_size / w
        self.y_project_size_pre_pixel = self.x_project_size / h

        x_project_size_pre_block = self.x_project_size / processes_divided
        y_project_size_pre_block = self.y_project_size / processes_divided    

        self.x_pixel_pre_block = int(w / processes_divided)
        self.y_pixel_pre_block = int(h / processes_divided)
        
        for i in range(processes_divided):
            for j in range(processes_divided):
                self.project_blocks.append(project_block(self.project_start + x_project_size_pre_block * i * self.x_coordinate_vector + y_project_size_pre_block * j * self.y_coordinate_vector,
                    self.x_pixel_pre_block * i,
                    self.y_pixel_pre_block * j))

    def findRotation(self):
     
        a = np.array([0.0,0.0,1.0])
        b = self.project_plane_normal

        v = np.cross(a,b)

        vx = np.matrix([[0,-1 * v[2],v[1]],[v[2],0,-1 * v[0]],[-1 * v[1],v[0],0]])

        s = np.linalg.norm(v)

        c = np.dot(a,b)

        r = np.identity(3) + vx + np.matmul(vx,vx) / (1 + c)
    
        return r

class project_block():

    def __init__(self, start, x_pixel_start_index, y_pixel_start_index):
        self.start = start
        self.x_pixel_start_index = x_pixel_start_index
        self.y_pixel_start_index = y_pixel_start_index

class ray():

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def trace_ray(self, scene):
        # Find first point of intersection with the scene.
        t = np.inf
        for i, obj in enumerate(scene):
            t_obj = obj.intersect(self)
            if t_obj < t:
                t, obj_idx = t_obj, i
        # Return None if the ray does not intersect any object.
        if t == np.inf:
            return
        # Find the object.
        obj = scene[obj_idx]
        # Find the point of intersection on the object.
        M = self.origin + self.direction * t
        # Find properties of the object.
        N = obj.getNormalVector(M)  
        
        if obj.type == 'plane':
            color = obj.getColor(M)
        else:
            color = obj.color

        toL = normalize(L - M)
        toO = normalize(self.origin - M)
        # Shadow: find if the point is shadowed or not.
        transparent_ratio = 1.0
        for k, obj_sh in enumerate(scene): 
            if k != obj_idx:
                if obj_sh.intersect(ray(M + N * .001, toL)) < np.inf:
                    transparent_ratio *= obj_sh.simple_refractive

        # Start computing the color.
        col_ray = ambient
        # Lambert shading (diffuse).
        col_ray += diffuse_c * max(np.dot(N, toL), 0) * color
        # Blinn-Phong shading (specular).
        col_ray += specular_c * max(np.dot(N, normalize(toL + toO)), 0) ** specular_k * color_light
        
        col_ray *= transparent_ratio ** 2
        
        return obj, M, N, col_ray

class plane():

    def __init__(self, point, normal_vector, transparency_level, color_type=0, color_1=np.ones(3), color_2=np.zeros(3)):
        self.point = np.array(point)
        self.normal_vector = np.array(normal_vector) / np.linalg.norm(np.array(normal_vector))
        self.color_type = color_type
        self.color_1 = np.array(color_1)
        self.color_2 = np.array(color_2)
        self.rotation = self.findRotation()
        self.refractive_indices = getRefractiveIndices(transparency_level)
        self.simple_refractive = getSimpleRefractive(transparency_level)
        self.type = 'plane'

        x = np.matmul(self.rotation,np.array([1,0,0]))
        z = np.matmul(self.rotation,np.array([0,0,1]))
        self.x_coordinate = np.array([x.item(0),x.item(1),x.item(2)])
        self.z_coordinate = np.array([z.item(0),z.item(1),z.item(2)])

    def getColor(self,postion):
        
        if self.color_type == 1:
            return self.color_1
        else:

            d_to_x = np.linalg.norm((self.point - postion) - np.dot((self.point - postion), self.x_coordinate) * self.x_coordinate)
            d_to_z = np.linalg.norm((self.point - postion) - np.dot((self.point - postion), self.z_coordinate) * self.z_coordinate)

            if (int(d_to_x) % 2) == (int(d_to_z * 2) % 2):
                return self.color_1
            else:
                return self.color_2

    def intersect(self, ray):
        return intersect_plane(ray, self.point, self.normal_vector)            

    def findRotation(self):
     
        a = np.array([0.0,1.0,0.0])
        b = self.normal_vector

        v = np.cross(a,b)

        vx = np.matrix([[0,-1 * v[2],v[1]],[v[2],0,-1 * v[0]],[-1 * v[1],v[0],0]])

        s = np.linalg.norm(v)

        c = np.dot(a,b)

        r = np.identity(3) + vx + np.matmul(vx,vx) / (1 + c)
    
        return r

    def getNormalVector(self, intersected_point):
        return self.normal_vector

class sphere():

    def __init__(self, position, radius, color, transparency_level):
        self.position = np.array(position)
        self.radius = radius
        self.color = np.array(color)
        self.refractive_indices = getRefractiveIndices(transparency_level)
        self.simple_refractive = getSimpleRefractive(transparency_level)
        self.type = 'sphere'

    def intersect(self, ray):
        return intersect_sphere(ray, self.position, self.radius)

    def getNormalVector(self, intersected_point):
        return normalize(intersected_point - self.position)

class triangle_plane():

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

    def intersect(self, ray):
        dist = intersect_plane(ray, self.point_1, self.normal_vector)
        if dist != np.inf:
            if PointinTriangle(self.point_1, self.point_2, self.point_3, ray.origin + ray.direction * dist):
                return dist
        return np.inf

    def check_on_plane(self, point):
        if abs(np.dot(point - self.point_1, self.normal_vector)) < 0.00000000001:
            if PointinTriangle(self.point_1, self.point_2, self.point_3, point):
                return True

        return False

class tetrahedron():

    def __init__(self, position, length, rotation_angle, color, transparency_level):

        self.position = np.array(position)
        self.length = length * 1.0
        self.rotation_angle = np.array(rotation_angle)
        self.type = 'tetrahedron'
        self.refractive_indices = getRefractiveIndices(transparency_level)
        self.simple_refractive = getSimpleRefractive(transparency_level)
        self.color = np.array(color)

        self.point_1 = self.position + rotation_vector(np.array([0, np.sqrt(3.0/8), 0]) * self.length, self.rotation_angle)
        self.point_2 = self.position + rotation_vector(np.array([-1.0/2, -1.0/np.sqrt(24), 1.0/np.sqrt(12)]) * self.length, self.rotation_angle)
        self.point_3 = self.position + rotation_vector(np.array([1.0/2, -1.0/np.sqrt(24), 1.0/np.sqrt(12)]) * self.length, self.rotation_angle)
        self.point_4 = self.position + rotation_vector(np.array([0, -1.0/np.sqrt(24), -1.0/np.sqrt(3)]) * self.length, self.rotation_angle)

        self.triangle_planes = [triangle_plane(self.point_1, self.point_2, self.point_3),
                    triangle_plane(self.point_1, self.point_2, self.point_4),
                    triangle_plane(self.point_1, self.point_3, self.point_4),
                    triangle_plane(self.point_2, self.point_3, self.point_4)]

        for i, plane in enumerate(self.triangle_planes):
            if  np.dot(plane.point_1 - self.position, plane.normal_vector) < 0:
                self.triangle_planes[i].normal_vector *=-1.0

    def intersect(self, ray):
        if intersect_sphere(ray, self.position, np.sqrt(3.0/8) * self.length) != np.inf:
            return intersect_TriangleSet(ray, self.triangle_planes)
        else:
            return np.inf

    def getNormalVector(self, intersected_point):
        for i, triangle_plane in enumerate(self.triangle_planes):
            if abs(np.dot(intersected_point - triangle_plane.point_1, triangle_plane.normal_vector)) < 0.00000000001:
                return triangle_plane.normal_vector


class cube():

    def __init__(self, position, length, rotation_angle, color, transparency_level):
        self.position = np.array(position)
        self.length = length * 1.0
        self.rotation_angle = np.array(rotation_angle)
        self.color = np.array(color)
        self.refractive_indices = getRefractiveIndices(transparency_level)
        self.simple_refractive = getSimpleRefractive(transparency_level)
        self.type = 'cube'

        square = [[], [], [], [], [], []]
        self.triangle_planes = []

        x_n_vector = rotation_vector(np.array([1.0, 0.0, 0.0]) * self.length / 2.0, self.rotation_angle)
        y_n_vector = rotation_vector(np.array([0.0, 1.0, 0.0]) * self.length / 2.0, self.rotation_angle)
        z_n_vector = rotation_vector(np.array([0.0, 0.0, 1.0]) * self.length / 2.0, self.rotation_angle)

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
                self.triangle_planes[i].normal_vector *=-1.0

    def intersect(self, ray):
        if intersect_sphere(ray, self.position, np.sqrt(3) * self.length / 2.0) != np.inf:
            return intersect_TriangleSet(ray, self.triangle_planes)
        else:
            return np.inf

    def getNormalVector(self, intersected_point):
        for i, triangle_plane in enumerate(self.triangle_planes):
            if abs(np.dot(intersected_point - triangle_plane.point_1,triangle_plane.normal_vector)) < 0.00000000001:
                return triangle_plane.normal_vector


class circle_plane():

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

    def __init__(self, position, height, radius, rotation_angle, color, transparency_level):
        self.position = np.array(position)
        self.height = height
        self.radius = radius
        self.normal_vector = rotation_vector(np.array([0.0, 1.0, 0.0]), np.array(rotation_angle))
        self.color = np.array(color)
        self.refractive_indices = getRefractiveIndices(transparency_level)
        self.simple_refractive = getSimpleRefractive(transparency_level)
        self.type = 'cylinder'

        top_plane = circle_plane(self.position + self.normal_vector * (height / 2.0), radius, self.normal_vector)
        bottom_plane = circle_plane(self.position - self.normal_vector * (height / 2.0), radius, -1.0 * self.normal_vector)
        self.top_bottom_plane = [top_plane, bottom_plane]

    def intersect(self, ray):
        dist = np.inf
        p = np.dot(ray.direction, self.normal_vector) * self.normal_vector - ray.direction
        q = self.position - ray.origin - np.dot(self.position - ray.origin, self.normal_vector) * self.normal_vector
        a = np.dot(p, p)
        b = 2.0 * np.dot(p, q)
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
                        if (np.linalg.norm(ray.origin + ray.direction * t1 - self.position)) ** 2 < self.radius ** 2 + (self.height / 2.0) ** 2:
                            dist = t1
                    else:
                        if (np.linalg.norm(ray.origin + ray.direction * t0 - self.position)) ** 2 < self.radius ** 2 + (self.height / 2.0) ** 2:
                            dist = t0

        for i, plane in enumerate(self.top_bottom_plane):
            tmp_dist = intersect_plane(ray, plane.position, plane.normal_vector)
            if tmp_dist < dist:
                if np.linalg.norm(ray.origin + tmp_dist * ray.direction - plane.position) <= plane.radius:
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

    def __init__(self, position, height, radius, rotation_angle, color, transparency_level):
        self.position = np.array(position)
        self.height = height
        self.radius = radius
        self.angel = math.atan(radius / (height / 2.0))
        self.normal_vector = rotation_vector(np.array([0.0, 1.0, 0.0]), np.array(rotation_angle))
        self.color = np.array(color)
        self.refractive_indices = getRefractiveIndices(transparency_level)
        self.simple_refractive = getSimpleRefractive(transparency_level)
        self.type = 'cone'

        top_plane = circle_plane(self.position + self.normal_vector * (height / 2.0), radius, self.normal_vector)
        bottom_plane = circle_plane(self.position - self.normal_vector * (height / 2.0), radius, -1 * self.normal_vector)
        self.top_bottom_plane = [top_plane, bottom_plane]

    def intersect(self, ray):
        dist = np.inf
        p = ray.direction - np.dot(ray.direction, self.normal_vector) * self.normal_vector
        q = ray.origin - self.position - np.dot(ray.origin - self.position, self.normal_vector) * self.normal_vector
        a = math.cos(self.angel) ** 2 * np.dot(p, p) - math.sin(self.angel) ** 2 * (np.dot(ray.direction, self.normal_vector) ** 2)
        b = 2.0 * math.cos(self.angel) ** 2 * np.dot(p, q) - 2 * math.sin(self.angel) ** 2 * np.dot(ray.direction,self.normal_vector) * np.dot((ray.origin - self.position),self.normal_vector)
        c = math.cos(self.angel) ** 2 * np.dot(q, q) - math.sin(self.angel) ** 2 * (np.dot(ray.origin - self.position,self.normal_vector) ** 2)

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
                        if (np.linalg.norm(ray.origin + ray.direction * t1 - self.position)) ** 2 < self.radius ** 2 + (self.height / 2.0) ** 2:
                            dist = t1
                    else:
                        if (np.linalg.norm(ray.origin + ray.direction * t0 - self.position)) ** 2 < self.radius ** 2 + (self.height / 2.0) ** 2:
                            dist = t0


        for i, plane in enumerate(self.top_bottom_plane):
            tmp_dist = intersect_plane(ray, plane.position, plane.normal_vector)
            if tmp_dist < dist:
                if np.linalg.norm(ray.origin + tmp_dist * ray.direction - plane.position) <= plane.radius:
                    dist = tmp_dist

        return dist

    def getNormalVector(self, intersected_point):

        for i, cycle_palne in enumerate(self.top_bottom_plane):
            if cycle_palne.check_on_plane(intersected_point):
                return cycle_palne.normal_vector

        project_point = self.position - np.dot((self.position - intersected_point),
                                               self.normal_vector) * self.normal_vector


        p = project_point + (project_point - self.position) * (self.radius / (self.height / 2.0))**2

        return normalize(intersected_point - p)


def normalize(x):
    x /= np.linalg.norm(x)
    return x


def intersect_plane(ray, P, N):
    # Return the distance from O to the intersection of the ray (O, D) with the
    # plane (P, N), or +inf if there is no intersection.
    # O and P are 3D points, D and N (normal) are normalized vectors.
    denom = np.dot(ray.direction, N)
    if np.abs(denom) < 1e-6:
        return np.inf
    d = np.dot(P - ray.origin, N) / denom
    if d < 0:
        return np.inf
    return d


def intersect_sphere(ray, S, R):
    # Return the distance from O to the intersection of the ray (O, D) with the
    # sphere (S, R), or +inf if there is no intersection.
    # O and S are 3D points, D (direction) is a normalized vector, R is a
    # scalar.
    a = np.dot(ray.direction, ray.direction)
    OS = ray.origin - S
    b = 2 * np.dot(ray.direction, OS)
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


def intersect_TriangleSet(ray, triangle_planes):
    dist = np.inf
    for i, triangle_plane in enumerate(triangle_planes):
        dist = min(dist, triangle_plane.intersect(ray))
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

    inverDeno = 1.0 / ((dot00 * dot11) - (dot01 * dot01))
    u = ((dot11 * dot02) - (dot01 * dot12)) * inverDeno
    if u < 0 or u > 1:  # if u out of range, return directly
        return False

    v = ((dot00 * dot12) - (dot01 * dot02)) * inverDeno
    if v < 0 or v > 1:  # if v out of range, return directly
        return False
    return u + v <= 1


def add_sphere(position, radius, color, transparency_level):
    return sphere(position, radius, color, transparency_level)

def add_plane(position, normal, transparency_level):
    return plane(position, normal, transparency_level)

def add_tetrahedron(position, length, rotation_angle, color, transparency_level):
    return tetrahedron(position, length, rotation_angle, color, transparency_level)

def add_cube(position, length, rotation_angle, color, transparency_level):
    return cube(position, length, rotation_angle, color, transparency_level)

def add_cylinder(poisition, height, radius, rotation_angle, color, transparency_level):
    return cylinder(poisition, height, radius, rotation_angle, color, transparency_level)

def add_cone(poisition, height, radius, rotation_angle, color, transparency_level):
    return cone(poisition, height, radius, rotation_angle, color, transparency_level)

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
    angle = r_angle * np.pi / 180.0
    r_x = np.matrix([[1, 0, 0], [0, np.cos(angle[0]), np.sin(angle[0] * -1)], [0, np.sin(angle[0]), np.cos(angle[0])]])
    r_y = np.matrix([[np.cos(angle[1]), 0, np.sin(angle[1])], [0, 1, 0], [np.sin(angle[1]) * -1, 0, np.cos(angle[1])]])
    r_z = np.matrix([[np.cos(angle[2]), np.sin(angle[2]) * -1, 0], [np.sin(angle[2]), np.cos(angle[2]), 0], [0, 0, 1]])

    tmp_node = node - r_centre
    r_node = np.matmul(r_z, np.matmul(r_y, np.matmul(r_x, (np.matrix([[tmp_node[0]], [tmp_node[1]], [tmp_node[2]]])))))

    return np.array([r_node.item(0), r_node.item(1), r_node.item(2)]) + r_centre


def rotation_vector(vector, r_angle):
    return rotation(vector, np.array([0, 0, 0]), r_angle)

#trace ray of pixel in given area
def trace_ray_main(result_queue, project_block_index, scene_input):
    img = np.zeros((h, w, 3))
    camera_seeting, scene = analyse_input(scene_input)
    current_project_block = camera_seeting.project_blocks[project_block_index]

    for i in range(camera_seeting.x_pixel_pre_block):
        for j in range(camera_seeting.y_pixel_pre_block):
            col = np.zeros(3)
            col[:] = 0
            Q = current_project_block.start + i * camera_seeting.x_project_size_pre_pixel * camera_seeting.x_coordinate_vector + j * camera_seeting.y_project_size_pre_pixel * camera_seeting.y_coordinate_vector
            D = normalize(Q - camera_seeting.position)
            depth = 0
            primaryRay = ray(camera_seeting.position, D)
            col = reflect_and_refract(primaryRay, scene, PositionType.OUT, depth, 1,i,j)
            img[h - (current_project_block.y_pixel_start_index + j) - 1, current_project_block.x_pixel_start_index + i, :] = np.clip(col, 0, 1)
    result_queue.put(img) 

def reflect_and_refract(primaryRay, scene, positionType, depth, pathLoss, i,j):

    traced = primaryRay.trace_ray(scene)
    
    if not traced:
        return 0. * np.zeros(3)

    obj, M, N, col_ray = traced

    if np.dot(primaryRay.direction, N) < 0:
        positionType = PositionType.OUT
        col = pathLoss * col_ray
        n1 = 1.0
        n2 = obj.refractive_indices
        newNormal = N
    else:
        positionType = PositionType.IN
        newNormal = N * -1
        col = np.zeros(3)
        n2 = 1.0
        n1 = obj.refractive_indices

    # Reflection Ray
    reflectAmount = fresnel(n1, n2, newNormal, primaryRay.direction)

    reflectRay = ray(M + newNormal * .001, normalize(primaryRay.direction - 2 * np.dot(primaryRay.direction, newNormal) * newNormal))

    if depth + 1 < depth_max:
        col+= reflect_and_refract(reflectRay, scene, positionType, depth + 1, pathLoss * reflectAmount, i,j)

    refractionAmount = 1 - reflectAmount

    # Refraction Ray
    if depth + 1 < depth_max and refractionAmount > 0:
            refractionRay = refraction(primaryRay, positionType, newNormal, obj, M)
            if refractionRay is not None:
                col+= reflect_and_refract(refractionRay, scene, positionType, depth + 1, pathLoss * refractionAmount, i,j)

    return col

def refraction(primaryRay, positionType, normal, refraction_obj, refraction_point):

    r = 1.0 / refraction_obj.refractive_indices

    if  positionType == PositionType.IN:
        r = 1.0 / r

    c1 = abs(np.dot(normal, primaryRay.direction))    
    t = 1 - r ** 2 * (1 - c1 ** 2)    

    if t < 0:
        return None
    else:
        c2 = np.sqrt(t)

    T = normalize(r * primaryRay.direction + (r * c1 - c2) * normal)

    refraction_ray = ray(refraction_point + 0.001 * normal * -1, T)

    return refraction_ray

def fresnel(n1, n2, normal, incident) :
 
    cosi = abs(np.dot(incident, normal))
    # Compute sini using Snell's law

    sint = n1 / n2 * np.sqrt(1 - cosi ** 2)
    # Total internal reflection
    if sint >= 1 : 
        kr = 1 
    
    else : 
        cost = np.sqrt(1 - sint * sint)
        Rs = ((n2 * cosi) - (n1 * cost)) / ((n2 * cosi) + (n1 * cost)) 
        Rp = ((n1 * cosi) - (n2 * cost)) / ((n1 * cosi) + (n2 * cost))
        kr = (Rs * Rs + Rp * Rp) / 2.0

    return kr


def getRefractiveIndices(level):

    if level == 0:
        return 10.0
    elif level == 1:
        return 8.0
    elif level == 2:
        return 5.0
    elif level == 3:
        return 2.0
    elif level == 4:
        return 1.3
    elif level == 5:
        return 1.1

def getSimpleRefractive(level):

    if level == 0:
        return 0.0
    elif level == 1:
        return 0.2
    elif level == 2:
        return 0.4
    elif level == 3:
        return 0.6
    elif level == 4:
        return 0.8
    elif level == 5:
        return 0.9

def analyse_input(scene_input):

    data = json.loads(scene_input)
    scene = []
    camera_position = [0, 0.35, -1]
    camera_point_to = [0,0.35,0]
    global L

    if data.get("light") is not None:
        L = np.array(data.get("light"))

    if data.get("camera_position") is not None:
        camera_position = data.get("camera_position")

    if data.get("camera_point_to") is not None:
        camera_point_to = data.get("camera_point_to")

    camera_seeting = camera(camera_position, camera_point_to)

    objTetrahedron = data.get("tetrahedron")
    if objTetrahedron is not None:
        for i, obj in enumerate(objTetrahedron):
            scene.append(add_tetrahedron(obj['position'], obj['length'], obj['rotation_angle'], obj['color'], obj['transparency_level']))

    objCube = data.get("cube")
    if objCube is not None:
        for i, obj in enumerate(objCube):
            scene.append(add_cube(obj['position'], obj['length'], obj['rotation_angle'], obj['color'], obj['transparency_level']))

    objCylinder = data.get("cylinder")
    if objCylinder is not None:
        for i, obj in enumerate(objCylinder):
            scene.append(add_cylinder(obj['position'], obj['height'], obj['radius'], obj['rotation_angle'], obj['color'],obj['transparency_level']))
 
    objCone = data.get("cone")
    if objCone is not None:
        for i, obj in enumerate(objCone):
            scene.append(add_cone(obj['position'], obj['height'], obj['radius'], obj['rotation_angle'], obj['color'],obj['transparency_level']))

    objSphere = data.get("sphere")
    if objSphere is not None:
        for i, obj in enumerate(objSphere):
            scene.append(add_sphere(obj['position'], obj['radius'], obj['color'],obj['transparency_level']))

    objPlane = data.get("plane")
    if objPlane is not None:
        for i, obj in enumerate(objPlane):
            scene.append(add_plane(obj['position'], obj['normal'],obj['transparency_level']))

    return camera_seeting, scene

w = 400
h = 400

# Light position and color.
L = np.array([5., 5., -10.])
color_light = np.ones(3)

# Default light and material parameters.
ambient = .05
diffuse_c = 1.
specular_c = 1.
specular_k = 50

depth_max = 4  # Maximum number of light reflections.
processes_divided = 8

if __name__ == '__main__':

    with open('data.json', 'r') as inputFile:
        scene_input = inputFile.read()  

    result_queue = mp.Queue()
    ps = []

    for i in range(processes_divided**2):
        ps.append(mp.Process(target=trace_ray_main, args=(result_queue, i,
        scene_input, )))

    img = np.zeros((h, w, 3))

    # start processes
    for p in ps:
        p.start()

    for i in range(len(ps)):
        img = img + result_queue.get()
        print(i + 1) *  1.0  / len(ps) * 100, '%'

    # for debug
    #processes_divided = 1
    #trace_ray_main(result_queue, 0, scene_input)
    #img = img + result_queue.get()

    plt.imsave('fig.png', img)
