import math

class Vector3d:
    def __init__(self, *args):
        # No parameters
        if(len(args) == 0):
            self.vec = [0.0, 0.0, 0.0]
        
        # One value
        elif len(args) == 1:
            x = args[0]
            self.vec = [x, x, x]

        # Three values
        elif len(args) == 3:
            x, y, z = args
            self.vec = [x, y, z]

    def __repr__(self):
        return f"{self.vec}"
    
    @staticmethod
    def size():
        return 3
    
    def __iter__(self):
        return iter(self.vec)

    def __getitem__(self, index):
        if not 0 <= index < 3:
            raise IndexError("Index out of range")
        return self.vec[index]
    
    def __setitem__(self, index, value):
        if not 0 <= index < 3:
            raise IndexError("Index out of range")
        self.vec[index] = value
    
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
        if not isinstance(v, Vector3d):
            raise TypeError("Type error")
        x, y, z = self.vec
        vx, vy, vz = v.vec
        return Vector3d(x + vx, y + vy, z + vz)
    
    def __sub__(self, v):
        if not isinstance(v, Vector3d):
            raise TypeError("Type error")
        x, y, z = self.vec
        vx, vy, vz = v.vec
        return Vector3d(x - vx, y - vy, z - vz)
    
    def __mul__(self, scale):
        if not isinstance(scale, (int, float)):
            return NotImplemented
        x, y, z = self.vec
        return Vector3d(x * scale, y * scale, z * scale)
    
    def __rmul__(self, scale):
        if not isinstance(scale, (int, float)):
            raise TypeError("Type error")
        return self * scale
    
    def __truediv__(self, scale):
        if not isinstance(scale, (int, float)):
            raise TypeError("Type error")
        x, y, z = self.vec
        return Vector3d(x / scale, y / scale, z / scale)
    
    def __iadd__(self, v):
        if not isinstance(v, Vector3d):
            raise TypeError("Type error")
        self.vec = [sum(x) for x in zip(self.vec, v.vec)]
        return self

    def __isub__(self, v):
        if not isinstance(v, Vector3d):
            raise TypeError("Type error")
        self.vec = [a - b for a, b in zip(self.vec, v.vec)]
        return self

    def __imul__(self, scale):
        if not isinstance(scale, (int, float)):
            raise TypeError("Type error")
        self.vec = [x * scale for x in self.vec]
        return self

    def __itruediv__(self, scale):
        if not isinstance(scale, (int, float)):
            raise TypeError("Type error")
        self.vec = [x / scale for x in self.vec]
        return self

    # Dot product
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
    
    # Cross product
    def cross(self, v):
        x, y, z = self.vec
        vx, vy, vz = v.vec
        return Vector3d(y * vz - z * vy, z * vx - x * vz, x * vy - y * vx)
    
    # Absolute value
    def abs(self):
        self.vec = [abs(x) for x in self.vec]
        return self
    
    def __abs__(self):
        x, y, z = self.vec
        return Vector3d(abs(x), abs(y), abs(z))

    def clamp(self, lower = 0.0, upper = 1.0):
        self.vec = [max(lower, min(x, upper)) for x in self.vec]
        return self

    def normalize(self):
        self /= self.length()
        return self
    
def normalize(v: Vector3d):
    return v / v.length()

def swap(a: Vector3d, b: Vector3d):
    a.vec, b.vec = b.vec, a.vec

def clamp(v: Vector3d, lower = 0.0, upper = 1.0):
    x, y, z = v.vec
    return Vector3d(max(lower, min(x, upper)), max(lower, min(y, upper)), max(lower, min(z, upper)))
