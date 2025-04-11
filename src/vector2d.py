import math

class Vector2d:
    def __init__(self, *args):
        # No parameters
        if(len(args) == 0):
            self.vec = [0.0, 0.0]
        
        # One value
        elif len(args) == 1:
            x = args[0]
            self.vec = [x, x]

        # Three values
        elif len(args) == 2:
            x, y = args
            self.vec = [x, y]

    def __repr__(self):
        return f"{self.vec}"
    
    @staticmethod
    def size():
        return 2
    
    def __iter__(self):
        return iter(self.vec)

    def __getitem__(self, index):
        if not 0 <= index < 2:
            raise IndexError("Index out of range")
        return self.vec[index]
    
    def __setitem__(self, index, value):
        if not 0 <= index < 2:
            raise IndexError("Index out of range")
        self.vec[index] = value
    
    def __eq__(self, v):
        if not isinstance(v, Vector2d):
            return False
        x, y = self.vec
        vx, vy = v.vec
        return (x == vx and y == vy)
    
    def __neg__(self):
        x, y = self.vec
        return Vector2d(-x, -y)

    def __add__(self, v):
        if not isinstance(v, Vector2d):
            raise TypeError("Type error")
        x, y = self.vec
        vx, vy = v.vec
        return Vector2d(x + vx, y + vy)
    
    def __sub__(self, v):
        if not isinstance(v, Vector2d):
            raise TypeError("Type error")
        x, y = self.vec
        vx, vy = v.vec
        return Vector2d(x - vx, y - vy)
    
    def __mul__(self, scale):
        if not isinstance(scale, (int, float)):
            return NotImplemented
        x, y = self.vec
        return Vector2d(x * scale, y * scale)
    
    def __rmul__(self, scale):
        if not isinstance(scale, (int, float)):
            raise TypeError("Type error")
        return self * scale
    
    def __truediv__(self, scale):
        if not isinstance(scale, (int, float)):
            raise TypeError("Type error")
        x, y = self.vec
        return Vector2d(x / scale, y / scale)
    
    def __iadd__(self, v):
        if not isinstance(v, Vector2d):
            raise TypeError("Type error")
        self.vec = [sum(x) for x in zip(self.vec, v.vec)]
        return self

    def __isub__(self, v):
        if not isinstance(v, Vector2d):
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
        x, y = self.vec
        vx, vy = v.vec
        return x * vx + y * vy
    
    def squared_length(self):
        return self.dot(self)
    
    def length(self):
        return math.sqrt(self.squared_length())
    
    def squared_distance(self, v):
        return (self - v).squared_length()
    
    def distance(self, v):
        return math.sqrt(self.squared_distance(v))
    
    # Absolute value
    def abs(self):
        self.vec = [abs(x) for x in self.vec]
        return self
    
    def __abs__(self):
        x, y = self.vec
        return Vector2d(abs(x), abs(y))

    def normalize(self):
        self /= self.length()
        return self
    
def normalize(v: Vector2d):
    return v / v.length()

def swap(a: Vector2d, b: Vector2d):
    a.vec, b.vec = b.vec, a.vec