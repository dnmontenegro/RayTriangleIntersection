from vector3d import Vector3d
from matrix3d import Matrix3d

class Transformation3d:
   _translation: Vector3d
   _transformation: Matrix3d
   _inverse_transformation: Matrix3d
   
   def __init__(self, translation: Vector3d = Vector3d(), transformation: Matrix3d = , inverse_transformation: Matrix3d):
        self._translation = translation
        self._transformation = transformation
        self._inverseTransformation = inverse_transformation
    
