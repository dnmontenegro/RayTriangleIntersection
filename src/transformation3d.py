from .vector3d import Vector3d
from .matrix3d import Matrix3d

class Transformation3d:
    _translation: Vector3d
    _transformation: Matrix3d
    _inverse_transformation: Matrix3d
    
    def __init__(self, *args):
        # No parameters
        if(len(args) == 0):
            self._translation = Vector3d()
            self._transformation = Matrix3d(1.0)
            self._inverse_transformation = Matrix3d(1.0)

        # One vector and two matrices
        elif len(args) == 3 and isinstance(args[0], Vector3d):
            translation, transformation, inverse_transformation = args
            self._translation = translation
            self._transformation = transformation
            self._inverse_transformation = inverse_transformation
            
    def __repr__(self):
        return f"Translation = {self._translation}, Transformation = {self._transformation}, Inverse Transformation = {self._inverse_transformation}"
    
    def __mul__(self, t):
        return Transformation3d(self.transform_point(t._translation), self._transformation * t._transformation, t._inverse_transformation * self._inverse_transformation)
       
    def __imul__(self, t):
        self._translation = self.transform_point(t._translation)
        self._transformation = self._transformation * t._transformation
        self._inverse_transformation = t._inverse_transformation * self._inverse_transformation
        return self

    def invert(self):
        self._translation = self._inverse_transformation * (-self._translation)
        self._transformation, self._inverse_transformation = self._inverse_transformation, self._transformation
        return self
    
    def transform_point(self, p: Vector3d):
        transformed = self._transformation * p
        transformed += self._translation
        return transformed

    def transform_direction(self, d: Vector3d):
        transformed = self._transformation * d
        return transformed.normalize()

    def transform_normal(self, n: Vector3d):
        transformed = n * self._inverse_transformation
        return transformed.normalize()

    def inverse_transform_point(self, p: Vector3d):
        transformed = p - self._translation
        transformed = self._inverse_transformation * transformed
        return transformed

    def inverse_transform_direction(self, d: Vector3d):
        transformed = self._inverse_transformation * d
        return transformed.normalize()

    def inverse_transform_normal(self, n: Vector3d):
        transformed = n * self._transformation
        return transformed.normalize()

def swap(a: Transformation3d, b: Transformation3d):
    a._translation, b._translation = b._translation, a._translation
    a._transformation, b._transformation = b._transformation, a._transformation
    a._inverse_transformation, b._inverse_transformation = b._inverse_transformation, a._inverse_transformation

def inverse(t: Transformation3d):
    return Transformation3d(t._inverse_transformation * (-t._translation), t._inverse_transformation, t._transformation)