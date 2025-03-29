import vector3d, vector2d, math

class Triangle:
    def __init__(self, *args):
        # No parameters
        if(len(args) == 0):
            self.vertex_idx = [None] * 3
            self.normal_idx = [None] * 3
            self.texture_coord_idx = [None] * 3
            self.vertex_list = None
            self.normal_list = None
            self.texture_coord_list = None
        
        # Three vertices
        elif len(args) == 3 and all(isinstance(arg, vector3d) for arg in args):
            self.vertex_idx = [0, 1, 2]
            self.normal_idx = [None] * 3
            self.texture_coord_idx = [None] * 3
            self.vertex_list = [args[0], args[1], args[2]]
            self.normal_list = None
            self.texture_coord_list = None

        # Three indices and a vertex list
        elif len(args) == 4 and isinstance(args[3], list):
            v1_idx, v2_idx, v3_idx, vertex_list = args
            self.vertex_idx = [v1_idx, v2_idx, v3_idx]
            self.normal_idx = [None] * 3
            self.texture_coord_idx = [None] * 3
            self.vertex_list = vertex_list
            self.normal_list = None
            self.texture_coord_list = None

        # Three vertices and three normals
        elif len(args) == 6 and all(isinstance(arg, vector3d) for arg in args):
            v1, v2, v3, n1, n2, n3 = args
            self.vertex_idx = [0, 1, 2]
            self.normal_idx = [0, 1, 2]
            self.texture_coord_idx = [None] * 3
            self.vertex_list = [v1, v2, v3]
            self.normal_list = [n1, n2, n3]
            self.texture_coord_list = None

        # Three vertex indices and a vertex list and three normal indices and a normal list
        elif len(args) == 8 and isinstance(args[7], list) and all(isinstance(arg, vector3d) for arg in args[7]):
            v1_idx, v2_idx, v3_idx, vertex_list, n1_idx, n2_idx, n3_idx, normal_list = args
            self.vertex_idx = [v1_idx, v2_idx, v3_idx]
            self.normal_idx = [n1_idx, n2_idx, n3_idx]
            self.texture_coord_idx = [None] * 3
            self.vertex_list = vertex_list
            self.normal_list = normal_list
            self.texture_coord_list = None

        # Three vertices and three texture coordinates
        elif len(args) == 6 and all(isinstance(arg, vector3d) for arg in args[:3]) and all(isinstance(arg, vector2d) for arg in args[3:]):
            v1, v2, v3, t1, t2, t3 = args
            self.vertex_idx = [0, 1, 2]
            self.normal_idx = [None] * 3
            self.texture_coord_idx = [0, 1, 2]
            self.vertex_list = [v1, v2, v3]
            self.normal_list = None
            self.texture_coord_list = [t1, t2, t3]

        # Three vertex indices and a vertex list and three texture coordinate indices and a texture coordinate list
        elif len(args) == 8 and isinstance(args[7], list) and all(isinstance(arg, vector2d) for arg in args[7]):
            v1_idx, v2_idx, v3_idx, vertex_list, t1_idx, t2_idx, t3_idx, texture_coord_list = args
            self.vertex_idx = [v1_idx, v2_idx, v3_idx]
            self.normal_idx = [None] * 3
            self.texture_coord_idx = [t1_idx, t2_idx, t3_idx]
            self.vertex_list = vertex_list
            self.normal_list = None
            self.texture_coord_list = texture_coord_list

        # Three vertices and three normals and three texture coordinates
        elif len(args) == 9 and all(isinstance(arg, vector3d) for arg in args[:6]) and all(isinstance(arg, vector2d) for arg in args[6:]):
            v1, v2, v3, n1, n2, n3, t1, t2, t3 = args
            self.vertex_idx = [0, 1, 2]
            self.normal_idx = [0, 1, 2]
            self.texture_coord_idx = [0, 1, 2]
            self.vertex_list = [v1, v2, v3]
            self.normal_list = [n1, n2, n3]
            self.texture_coord_list = [t1, t2, t3]

        # Three vertex indices and a vertex list and three normal indices and a normal list and three texture coordinate indices and a texture coordinate list
        elif len(args) == 12 and isinstance(args[11], list):
            v1_idx, v2_idx, v3_idx, vertex_list, n1_idx, n2_idx, n3_idx, normal_list, t1_idx, t2_idx, t3_idx, texture_coord_list = args
            self.vertex_idx = [v1_idx, v2_idx, v3_idx]
            self.normal_idx = [n1_idx, n2_idx, n3_idx]
            self.texture_coord_idx = [t1_idx, t2_idx, t3_idx]
            self.vertex_list = vertex_list
            self.normal_list = normal_list
            self.texture_coord_list = texture_coord_list

    def vertex(self, index):
        if self.vertex_list is None or index >= 3:
            raise IndexError("Index out of range")
        return self.vertex_list[self.vertex_idx[index]]

    def normal(self, index):
        if self.normal_list is None or index >= 3:
            raise IndexError("Index out of range")
        return self.normal_list[self.normal_idx[index]]

    def texture_coordinate(self, index):
        if self.texture_coord_list is None or index >= 3:
            raise IndexError("Index out of range")
        return self.texture_coord_list[self.texture_coord_idx[index]]

    def has_per_vertex_normals(self):
        return self.normal_list is not None

    def has_per_vertex_texture_coordinates(self):
        return self.texture_coord_list is not None
    
    def intersect(self, r, barycentric_coord, t):
        V = r.direction()
        N = self.normal()
        
        if abs(V.dot(N)) < EPSILON:
            return False
        
        P_0 = r.origin()
        d = -N.dot(self.vertex(0))
        t = -(P_0.dot(N) + d) / (V.dot(N))
        
        P = P_0 + t * V
        A1 = 0.5 * ((self.vertex(1) - P).cross(self.vertex(2) - P)).dot(N)
        A2 = 0.5 * ((self.vertex(2) - P).cross(self.vertex(0) - P)).dot(N)
        A3 = 0.5 * ((self.vertex(0) - P).cross(self.vertex(1) - P)).dot(N)
        
        alpha = A1 / abs(A1 + A2 + A3)
        beta = A2 / abs(A1 + A2 + A3)
        gamma = 1.0 - alpha - beta
        
        if t >= 0 and alpha >= 0 and beta >= 0 and gamma >= 0:
            barycentricCoord = Vector3D(alpha, beta, gamma)
            return True
        else:
            return False

    def boundingbox(self):
        bb = BoundingBox()
        for i in range(3):
            bb += self.vertex(i)
        return bb


    def vertex_barycentric(self, barycentric_coord):
        result = Vector3D(0.0, 0.0, 0.0)
        for i in range(3):
            result += self.vertex(i) * barycentricCoord[i]
        return result

    def normal_of_triangle(self):
        e1 = self.vertex(1) - self.vertex(0)
        e2 = self.vertex(2) - self.vertex(0)
        return e1.cross(e2).normalize()

    def shading_axis(self):

    def normal_barycentric(self, barycentric_coord):
        if not self.hasPerVertexNormals():
            return self.normal()
        
        result = Vector3D(0.0, 0.0, 0.0)
        for i in range(3):
            result += self.normal(i) * barycentricCoord[i]
        return result.normalize()

    def texture_coordinate_barycentric(self, barycentric_coord):
        if not self.hasPerVertexTextureCoordinates():
            return Vector2D()

        result = Vector2D(0.0, 0.0)
        for i in range(3):
            result += self.textureCoordinate(i) * barycentricCoord[i]
        return result

    def area(self):
        e1 = self.vertex(1) - self.vertex(0)
        e2 = self.vertex(2) - self.vertex(0)
        return 0.5 * e1.cross(e2).length()

    def sample(self, r1, r2, barycentric_coord, pdf):
        r2 = math.sqrt(r2)

        barycentric_coord.x = r1 * r2
        barycentric_coord.y = 1.0 - r2
        barycentric_coord.z = 1.0 - barycentric_coord.x - barycentric_coord.y

        pdf = 1.0 / self.area()

        return self.vertex_barycentric(barycentric_coord)

def swap(a , b):
    a.vertex_idx, b.vertex_idx = b.vertex_idx, a.vertex_idx
    a.normal_idx, b.normal_idx = b.normal_idx, a.normal_idx
    a.texture_coord_idx, b.texture_coord_idx = b.texture_coord_idx, a.texture_coord_idx
    a.vertex_list, b.vertex_list = b.vertex_list, a.vertex_list
    a.normal_list, b.normal_list = b.normal_list, a.normal_list
    a.texture_coord_list, b.texture_coord_list = b.texture_coord_list, a.texture_coord_list