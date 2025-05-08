from .color import Color

class Image:
    _width: int
    _height: int

    def __init__(self, *args):
        # No parameters
        if(len(args) == 0):
            self._width = 0
            self._height = 0
            self._data = []
        
        # Width and height
        elif len(args) == 2:
            self._width = args[0]
            self._height = args[1]
            self._data = [None] * (self._width * self._height) 

        # Width, height, and color
        elif len(args) == 3:
            self._width = args[0]
            self._height = args[1]
            self._data = [args[2]] * (self._width * self._height)  

    def __repr__(self):
        return f"Image: ({self._width}, {self._height})"
    
    def __iter__(self):
        return iter(self._data)
    
    def width(self):
        return self._width

    def height(self):
        return self._height
    
    def size(self):
        return self.width() * self.height()
    
    def __getitem__(self, index):
        x, y = index

        if not (0 <= x < self.width()):
            raise IndexError("Index out of range")
        
        if not (0 <= y < self.height()):
            raise IndexError("Index out of range")
        
        return self._data[y * self._width + x]

    def __setitem__(self, index, value):
        x, y = index
        
        if not (0 <= x < self.width()):
            raise IndexError("Index out of range")
        
        if not (0 <= y < self.height()):
            raise IndexError("Index out of range")
        
        self._data[y * self._width + x] = value

def swap(a: Image, b: Image):
    a._width, b._width = b._width, a._width
    a._height, b._height = b._height, a._height
    a._data, b._data = b._data, a._data