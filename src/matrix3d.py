from .vector3d import Vector3d

class Matrix3d:
    def __init__(self, *args):
        # No parameters
        if(len(args) == 0):
            self._data = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        
        # One diagonal value
        elif len(args) == 1:
            diag = args[0]
            self._data = [[diag, 0.0, 0.0], [0.0, diag, 0.0], [0.0, 0.0, diag]]

        # Three vertices
        elif len(args) == 3 and all(isinstance(arg, Vector3d) for arg in args):
            X, Y, Z = args
            self._data = [[X[0], Y[0], Z[0]], [X[1], Y[1], Z[1]], [X[2], Y[2], Z[2]]]

    def __repr__(self):
        return f"{self._data}"

    @staticmethod
    def width():
        return 3
    
    @staticmethod
    def height():
        return 3
    
    @staticmethod
    def size():
        return 9

    def __iter__(self):
        return iter(self._data)
        
    def clear(self, value = 0.0):
        for i in range(3):
            for j in range(3):
                self._data[i][j] = value

    def set_diagonal(self, value = 1.0): 
        for i in range(3):
            self._data[i][i] = value

    def transpose(self):
        for i in range(3):
            for j in range(i + 1, 3):
                self._data[i][j], self._data[j][i] = self._data[j][i], self._data[i][j]
        return self
    
    def __getitem__(self, index):
        if not 0 <= index < 3:
            raise IndexError("Index out of range")
        return self._data[index]
    
    def __setitem__(self, index, value):
        if not 0 <= index < 3:
            raise IndexError("Index out of range")
        self._data[index] = value
    
    def __add__(self, m):
        if not isinstance(m, Matrix3d):
            raise TypeError("Type error")
        result = Matrix3d()
        for i in range(3):
            for j in range(3):
                result._data[i][j] = self._data[i][j] + m._data[i][j]
        return result

    def __sub__(self, m):
        if not isinstance(m, Matrix3d):
            raise TypeError("Type error")
        result = Matrix3d()
        for i in range(3):
            for j in range(3):
                result._data[i][j] = self._data[i][j] - m._data[i][j]
        return result

    def __mul__(self, other):
        # Matrix multiplication
        if isinstance(other, Matrix3d):
            result = Matrix3d()
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        result._data[i][j] += self._data[i][k] * other._data[k][j]
            return result
        
        # Vector-matrix multiplication
        elif isinstance(other, Vector3d): 
            result = Vector3d()
            for i in range(3):
                for j in range(3):
                    result[i] += self._data[i][j] * other[j]
            return result
        
        # Scalar multiplication
        elif isinstance(other, (int, float)):
            result = Matrix3d()
            for i in range(3):
                for j in range(3):
                    result._data[i][j] = self._data[i][j] * other
            return result
        
    def __rmul__(self, other):
        if isinstance(other, Vector3d):
            result = Vector3d()
            for i in range(3):
                for j in range(3):
                    result[j] += self._data[i][j] * other[i]
            return result
        
        else:
            return self * other
    
    def __truediv__(self, scale):
        if not isinstance(scale, (int, float)):
            raise TypeError("Type error")
        result = Matrix3d()
        for i in range(3):
            for j in range(3):
                result._data[i][j] = self._data[i][j] / scale
        return result

    def __iadd__(self, m):
        if not isinstance(m, Matrix3d):
            raise TypeError("Type error")
        for i in range(3):
            for j in range(3):
                self._data[i][j] += m._data[i][j]
        return self

    def __isub__(self, m):
        if not isinstance(m, Matrix3d):
            raise TypeError("Type error")
        for i in range(3):
            for j in range(3):
                self._data[i][j] -= m._data[i][j]
        return self

    def __imul__(self, other):
        # Matrix multiplication
        if isinstance(other, Matrix3d): 
            result = Matrix3d()
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        result._data[i][j] += self._data[i][k] * other._data[k][j]
            self._data = result._data
            return self
        
        # Scalar multiplication
        elif isinstance(other, (int, float)):
            for i in range(3):
                for j in range(3):
                    self._data[i][j] *= other
            return self

    def __idiv__(self, scale):
        if not isinstance(scale, (int, float)):
            raise TypeError("Type error")
        for i in range(3):
            for j in range(3):
                self._data[i][j] /= scale
        return self

def swap(a: Matrix3d , b: Matrix3d):
    a._data, b._data = b._data, a._data

def transpose(m: Matrix3d):
    result = Matrix3d()
    for i in range(3):
        for j in range(3):
            result._data[i][j] = m._data[j][i]
    return result