from .vector3d import Vector3d, normalize
from .transformation3d import Transformation3d

class Ray:
    _origin: Vector3d
    _direction: Vector3d

    def __init__(self, origin: Vector3d, direction: Vector3d):
        self._origin = origin
        self._direction = normalize(direction)

    def __repr__(self):
        return f"{self.origin()} -> {self.direction()}"

    def origin(self):
        return self._origin

    def direction(self):
        return self._direction
    
    def __getitem__(self, arg):
        if isinstance(arg, (int, float)):
            return self._origin + arg * self._direction
        
        elif isinstance(arg, Vector3d):
            return self._direction.dot(arg - self._origin)

    def transform(self, t: Transformation3d):
        self._origin = t.transform_point(self._origin)
        self._direction = t.transform_direction(self._direction)
        return self

    def inverse_transform(self, t: Transformation3d):
        self._origin = t.inverse_transform_point(self._origin)
        self._direction = t.inverse_transform_direction(self._direction)
        return self

def swap(a: Ray, b: Ray):
    a._origin, b._origin = b._origin, a._origin
    a._direction, b._direction = b._direction, a._direction

def transform(r: Ray, t: Transformation3d):
    origin = r.origin()
    direction = r.direction()
    return Ray(t.transform_point(origin), t.transform_direction(direction))

def inverse_transform(r: Ray, t: Transformation3d):
    origin = r.origin()
    direction = r.direction()
    return Ray(t.inverse_transform_point(origin), t.inverse_transform_direction(direction))

    