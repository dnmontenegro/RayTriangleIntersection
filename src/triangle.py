from .vector3d import Vector3d, normalize
from .vector2d import Vector2d
from .ray import Ray
from .boundingbox import BoundingBox
import math

class Triangle:
    def __init__(self, *args):
        # No parameters
        if(len(args) == 0):
            self._vertex_idx = [None] * 3
            self._normal_idx = [None] * 3
            self._texture_coord_idx = [None] * 3
            self._vertex_list = None
            self._normal_list = None
            self._texture_coord_list = None
        
        # Three vertices
        elif len(args) == 3 and all(isinstance(arg, Vector3d) for arg in args):
            self._vertex_idx = [0, 1, 2]
            self._normal_idx = [None] * 3
            self._texture_coord_idx = [None] * 3
            self._vertex_list = [args[0], args[1], args[2]]
            self._normal_list = None
            self._texture_coord_list = None

        # Three indices and a vertex list
        elif len(args) == 4 and isinstance(args[3], list):
            v1_idx, v2_idx, v3_idx, vertex_list = args
            self._vertex_idx = [v1_idx, v2_idx, v3_idx]
            self._normal_idx = [None] * 3
            self._texture_coord_idx = [None] * 3
            self._vertex_list = vertex_list
            self._normal_list = None
            self._texture_coord_list = None

        # Three vertices and three normals
        elif len(args) == 6 and all(isinstance(arg, Vector3d) for arg in args):
            v1, v2, v3, n1, n2, n3 = args
            self._vertex_idx = [0, 1, 2]
            self._normal_idx = [0, 1, 2]
            self._texture_coord_idx = [None] * 3
            self._vertex_list = [v1, v2, v3]
            self._normal_list = [n1, n2, n3]
            self._texture_coord_list = None

        # Three vertex indices and a vertex list and three normal indices and a normal list
        elif len(args) == 8 and isinstance(args[7], list) and all(isinstance(arg, Vector3d) for arg in args[7]):
            v1_idx, v2_idx, v3_idx, vertex_list, n1_idx, n2_idx, n3_idx, normal_list = args
            self._vertex_idx = [v1_idx, v2_idx, v3_idx]
            self._normal_idx = [n1_idx, n2_idx, n3_idx]
            self._texture_coord_idx = [None] * 3
            self._vertex_list = vertex_list
            self._normal_list = normal_list
            self._texture_coord_list = None

        # Three vertices and three texture coordinates
        elif len(args) == 6 and all(isinstance(arg, Vector3d) for arg in args[:3]) and all(isinstance(arg, Vector2d) for arg in args[3:]):
            v1, v2, v3, t1, t2, t3 = args
            self._vertex_idx = [0, 1, 2]
            self._normal_idx = [None] * 3
            self._texture_coord_idx = [0, 1, 2]
            self._vertex_list = [v1, v2, v3]
            self._normal_list = None
            self._texture_coord_list = [t1, t2, t3]

        # Three vertex indices and a vertex list and three texture coordinate indices and a texture coordinate list
        elif len(args) == 8 and isinstance(args[7], list) and all(isinstance(arg, Vector2d) for arg in args[7]):
            v1_idx, v2_idx, v3_idx, vertex_list, t1_idx, t2_idx, t3_idx, texture_coord_list = args
            self._vertex_idx = [v1_idx, v2_idx, v3_idx]
            self._normal_idx = [None] * 3
            self._texture_coord_idx = [t1_idx, t2_idx, t3_idx]
            self._vertex_list = vertex_list
            self._normal_list = None
            self._texture_coord_list = texture_coord_list

        # Three vertices and three normals and three texture coordinates
        elif len(args) == 9 and all(isinstance(arg, Vector3d) for arg in args[:6]) and all(isinstance(arg, Vector2d) for arg in args[6:]):
            v1, v2, v3, n1, n2, n3, t1, t2, t3 = args
            self._vertex_idx = [0, 1, 2]
            self._normal_idx = [0, 1, 2]
            self._texture_coord_idx = [0, 1, 2]
            self._vertex_list = [v1, v2, v3]
            self._normal_list = [n1, n2, n3]
            self._texture_coord_list = [t1, t2, t3]

        # Three vertex indices and a vertex list and three normal indices and a normal list and three texture coordinate indices and a texture coordinate list
        elif len(args) == 12 and isinstance(args[11], list):
            v1_idx, v2_idx, v3_idx, vertex_list, n1_idx, n2_idx, n3_idx, normal_list, t1_idx, t2_idx, t3_idx, texture_coord_list = args
            self._vertex_idx = [v1_idx, v2_idx, v3_idx]
            self._normal_idx = [n1_idx, n2_idx, n3_idx]
            self._texture_coord_idx = [t1_idx, t2_idx, t3_idx]
            self._vertex_list = vertex_list
            self._normal_list = normal_list
            self._texture_coord_list = texture_coord_list

    def __repr__(self):
        result = f"Triangle: v = ({self.vertex(0)}, {self.vertex(1)}, {self.vertex(2)})"

        if self._normal_list:
            result += f", n = ({self.normal(0)}, {self.normal(1)}, {self.normal(2)})"

        if self._texture_coord_list:
            result += f", t = ({self.texture_coordinate(0)}, {self.texture_coordinate(1)}, {self.texture_coordinate(2)})"

        return result

    def vertex(self, index):
        if self._vertex_list is None or index >= 3:
            raise IndexError("Index out of range")
        return self._vertex_list[self._vertex_idx[index]]

    def normal(self, index):
        if self._normal_list is None or index >= 3:
            raise IndexError("Index out of range")
        return self._normal_list[self._normal_idx[index]]

    def texture_coordinate(self, index):
        if self._texture_coord_list is None or index >= 3:
            raise IndexError("Index out of range")
        return self._texture_coord_list[self._texture_coord_idx[index]]

    def has_per_vertex_normals(self):
        return self._normal_list is not None

    def has_per_vertex_texture_coordinates(self):
        return self._texture_coord_list is not None
    
    def intersect(self, r: Ray, barycentric_coord: list, t: list):
        V = r.direction()
        N = self.normal_of_triangle()
        
        if abs(V.dot(N)) < 10e-6:
            return False
        
        P_0 = r.origin()
        d = -N.dot(self.vertex(0))
        t[0] = -(P_0.dot(N) + d) / (V.dot(N))
        
        P = r[t[0]]
        A1 = ((self.vertex(1) - P).cross(self.vertex(2) - P)).dot(N)
        A2 = ((self.vertex(2) - P).cross(self.vertex(0) - P)).dot(N)
        A3 = ((self.vertex(0) - P).cross(self.vertex(1) - P)).dot(N)
        
        alpha = A1 / abs(A1 + A2 + A3)
        beta = A2 / abs(A1 + A2 + A3)
        gamma = 1.0 - alpha - beta
        
        if t[0] >= 0 and alpha >= 0 and beta >= 0 and gamma >= 0:
            barycentric_coord[0] = Vector3d(alpha, beta, gamma)
            return True
        else:
            return False

    def boundingbox(self):
        bb = BoundingBox()
        for i in range(3):
            bb += self.vertex(i)
        return bb

    def vertex_barycentric(self, barycentric_coord: Vector3d):
        result = Vector3d()
        for i in range(3):
            result += self.vertex(i) * barycentric_coord[i]
        return result

    def normal_of_triangle(self):
        e1 = self.vertex(1) - self.vertex(0)
        e2 = self.vertex(2) - self.vertex(0)
        return e1.cross(e2).normalize()

    def shading_axis(self):
        if not self._texture_coord_list:
            return normalize(self.vertex(1) - self.vertex(0))

        v1 = self.vertex(1) - self.vertex(0)
        v2 = self.vertex(2) - self.vertex(0)
        t1 = self.texture_coordinate(1) - self.texture_coordinate(0)
        t2 = self.texture_coordinate(2) - self.texture_coordinate(0)

        if abs(t1[1]) < 10e-6:
            return normalize(t1[0] * v1)
        
        if abs(t2[1]) < 10e-6:
            return normalize(t2[0] * v2)

        inv_delta_beta = t1[0] - t1[1] * t2[0] / t2[1]

        if abs(inv_delta_beta) < 10e-6:
            return normalize(v1)

        delta_beta = 1.0 / inv_delta_beta
        delta_gamma = -delta_beta * t1[1] / t2[1]

        return normalize(delta_beta * v1 + delta_gamma * v2)

    def normal_barycentric(self, barycentric_coord: Vector3d):
        if not self.has_per_vertex_normals():
            return self.normal_of_triangle()
        
        result = Vector3d()
        for i in range(3):
            result += self.normal(i) * barycentric_coord[i]
        return result.normalize()

    def texture_coordinate_barycentric(self, barycentric_coord: Vector3d):
        if not self.has_per_vertex_texture_coordinates:
            return Vector2d()

        result = Vector2d()
        for i in range(3):
            result += self.texture_coordinate(i) * barycentric_coord[i]
        return result

    def area(self):
        e1 = self.vertex(1) - self.vertex(0)
        e2 = self.vertex(2) - self.vertex(0)
        return 0.5 * e1.cross(e2).length()

    def sample(self, r1: float, r2: float, barycentric_coord: list, pdf: list):
        r2 = math.sqrt(r2)

        barycentric_coord[0][0] = r1 * r2
        barycentric_coord[0][1] = 1.0 - r2
        barycentric_coord[0][2] = 1.0 - barycentric_coord[0][0] - barycentric_coord[0][1]

        pdf[0] = 1.0 / self.area()

        return self.vertex_barycentric(barycentric_coord[0])

def swap(a: Triangle, b: Triangle):
    a._vertex_idx, b._vertex_idx = b._vertex_idx, a._vertex_idx
    a._normal_idx, b._normal_idx = b._normal_idx, a._normal_idx
    a._texture_coord_idx, b._texture_coord_idx = b._texture_coord_idx, a._texture_coord_idx
    a._vertex_list, b._vertex_list = b._vertex_list, a._vertex_list
    a._normal_list, b._normal_list = b._normal_list, a._normal_list
    a._texture_coord_list, b._texture_coord_list = b._texture_coord_list, a._texture_coord_list