from .vector3d import Vector3d

class Color:
    def __init__(self, *args):
        # No parameters
        if(len(args) == 0):
            self.data = [0.0, 0.0, 0.0]
        
        # One value
        elif len(args) == 1:
            r = args[0]
            self.data = [r, r, r]

        # Three values
        elif len(args) == 3:
            r, g, b = args
            self.data = [r, g, b]

    def __repr__(self):
        return f"({self.data[0]}, {self.data[1]}, {self.data[2]})"
    
    def __getitem__(self, index):
        if not 0 <= index < 3:
            raise IndexError("Index out of range")
        return self.data[index]
    
    def __setitem__(self, index, value):
        if not 0 <= index < 3:
            raise IndexError("Index out of range")
        self.data[index] = value

    def size():
        return 3

    def __iter__(self):
        return iter(self.data)
    
    def to_vec3d(self):
        return Vector3d(self.data[0], self.data[1], self.data[2])
    
    def __eq__(self, col):
        if not isinstance(col, Color):
            return False
        r, g, b = self.data
        colr, colg, colb = col.data
        return (r == colr and g == colg and b == colb)

    def __add__(self, col):
        if not isinstance(col, Color):
            raise TypeError("Type error")
        r, g, b = self.data
        colr, colg, colb = col.data
        return Color(r + colr, g + colg, b + colb)
    
    def __sub__(self, col):
        if not isinstance(col, Color):
            raise TypeError("Type error")
        r, g, b = self.data
        colr, colg, colb = col.data
        return Color(r - colr, g - colg, b - colb)
    
    def __mul__(self, other):
        if isinstance(other, Color):
            r, g, b = self.data
            colr, colg, colb = other.data
            return Color(r * colr, g * colg, b * colb)
        
        elif isinstance(other, (int, float)):
            r, g, b = self.data
            return Color(r * other, g * other, b * other)
    
    def __rmul__(self, scale):
        if not isinstance(scale, (int, float)):
            raise TypeError("Type error")
        return self * scale
    
    def __truediv__(self, other):
        if isinstance(other, Color):
            r, g, b = self.data
            colr, colg, colb = other.data
            return Color(r / colr, g / colg, b / colb)
        
        elif isinstance(other, (int, float)):
            r, g, b = self.data
            return Color(r / other, g / other, b / other)
    
    def __iadd__(self, col):
        if not isinstance(col, Color):
            raise TypeError("Type error")
        self.data = [sum(x) for x in zip(self.data, col.data)]
        return self

    def __isub__(self, col):
        if not isinstance(col, Color):
            raise TypeError("Type error")
        self.data = [a - b for a, b in zip(self.data, col.data)]
        return self

    def __imul__(self, other):
        if isinstance(other, Color):
            self.data = [a * b for a, b in zip(self.data, other.data)]
            return self
        
        elif isinstance(other, (int, float)):
            self.data = [x * other for x in self.data]
            return self

    def __itruediv__(self, other):
        if isinstance(other, Color):
            self.data = [a / b for a, b in zip(self.data, other.data)]
            return self
        
        elif isinstance(other, (int, float)):
            self.data = [x / other for x in self.data]
            return self
        
    def abs(self):
        self.data = [abs(x) for x in self.data]
        return self
    
    def __abs__(self):
        r, g, b = self.data
        return Color(abs(r), abs(g), abs(b))
    
    def clamp(self, lower = 0.0, upper = 1.0):
        self.data = [max(lower, min(x, upper)) for x in self.data]
        return self
    
def swap(a: Color, b: Color):
    a.data, b.data = b.data, a.data

def clamp(col: Color, lower = 0.0, upper = 1.0):
    r, g, b = col.data
    return Color(max(lower, min(r, upper)), max(lower, min(g, upper)), max(lower, min(b, upper)))