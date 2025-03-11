import math

class Vector3d:
    def __init__(self, x, y, z):
        self.vec = [x, y, z]

    def __repr__(self):
        return f"{self.vec}"
    
    def __len__(self):
        return 3

    def __getitem__(self, index):
        if not 0 <= index < 3:
            raise IndexError("Index out of range")
        return self.vec[index]
    
    def __iter__(self):
        return iter(self.vec)
    
    def __eq__(self, v):
        if not isinstance(v, Vector3d):
            return False
        x, y, z = self.vec
        vx, vy, vz = v.vec
        return (x == vx and y == vy and z == vz)
    
    def __neg__(self):
        x, y, z = self.vec
        return Vector3d(-x, -y, -z)

    def __add__(self, v):
        x, y, z = self.vec
        vx, vy, vz = v.vec
        return Vector3d(x + vx, y + vy, z + vz)
    
    def __sub__(self, v):
        x, y, z = self.vec
        vx, vy, vz = v.vec
        return Vector3d(x - vx, y - vy, z - vz)
    
    def __mul__(self, scale):
        x, y, z = self.vec
        return Vector3d(x * scale, y * scale, z * scale)
    
    def __rmul__(self, scale):
        return self * scale
    
    def __truediv__(self, scale):
        x, y, z = self.vec
        return Vector3d(x / scale, y / scale, z / scale)
    
    def __iadd__(self, v):
        self.vec = [sum(x) for x in zip(self.vec, v.vec)]
        return self

    def __isub__(self, v):
        self.vec = [a - b for a, b in zip(self.vec, v.vec)]
        return self

    def __imul__(self, scale):
        self.vec = [x * scale for x in self.vec]
        return self

    def __itruediv__(self, scale):
        self.vec = [x / scale for x in self.vec]
        return self

    def dot(self, v):
        x, y, z = self.vec
        vx, vy, vz = v.vec
        return x * vx + y * vy + z * vz
    
    def squared_length(self):
        return self.dot(self)
    
    def length(self):
        return math.sqrt(self.squared_length())
    
    def squared_distance(self, v):
        return (self - v).squared_length()
    
    def distance(self, v):
        return math.sqrt(self.squared_distance(v))
    
    def cross(self, v):
        x, y, z = self.vec
        vx, vy, vz = v.vec
        return Vector3d(y * vz - z * vy, z * vx - x * vz, x * vy - y * vx)
    
    def abs(self):
        self.vec = [abs(x) for x in self.vec]
        return self
    
    def __abs__(self):
        x, y, z = self.vec
        return Vector3d(abs(x), abs(y), abs(z))

    def clamp(self, lower, upper):
        self.vec = [max(lower, min(x, upper)) for x in self.vec]
        return self

    def normalize(self):
        self /= self.length()
        return self
    
def normalize(v):
    return v / v.length()

def swap(a , b):
    a.vec, b.vec = b.vec, a.vec

def clamp(v, lower=0.0, upper=1.0):
    x, y, z = v.vec
    return Vector3d(max(lower, min(x, upper)), max(lower, min(y, upper)), max(lower, min(z, upper)))
