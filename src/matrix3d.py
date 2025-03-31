from vector3d import Vector3d

class Matrix3d:
    def __init__(self, diag=None, X=None, Y=None, Z=None):
        if diag is not None:
            self._data = np.diag([diag, diag, diag])
        elif X is not None and Y is not None and Z is not None:
            self._data = np.array([X, Y, Z]).T
        else:
            self._data = np.zeros((3, 3))
