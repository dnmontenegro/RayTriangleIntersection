import math

class Vector2d:
    def __init__(self, x = 0.0, y = None):
        if y is None:
            self.vec = [x, x]
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
        x, y = self.vec
        vx, vy = v.vec
        return Vector2d(x + vx, y + vy)
    
    def __sub__(self, v):
        x, y = self.vec
        vx, vy = v.vec
        return Vector2d(x - vx, y - vy)
    
    def __mul__(self, scale):
        x, y = self.vec
        return Vector2d(x * scale, y * scale)
    
    def __rmul__(self, scale):
        return self * scale
    
    def __truediv__(self, scale):
        x, y = self.vec
        return Vector2d(x / scale, y / scale)
    
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
    
    def abs(self):
        self.vec = [abs(x) for x in self.vec]
        return self
    
    def __abs__(self):
        x, y = self.vec
        return Vector2d(abs(x), abs(y))

    def normalize(self):
        self /= self.length()
        return self
    
def normalize(v):
    return v / v.length()

def swap(a , b):
    a.vec, b.vec = b.vec, a.vec