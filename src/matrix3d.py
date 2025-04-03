from vector3d import Vector3d

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
        
    def clear(self, value):
        for i in range(3):
            for j in range(3):
                self._data[i][j] = value

    def set_diagonal(self, value): 
        for i in range(3):
            self._data[i][i] = value

    def transpose(self):
        for i in range(3):
            for j in range(i + 1, 3):
                self._data[i][j], self._data[j][i] = self._data[j][i], self._data[i][j]
        return self
    

