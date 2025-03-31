from vector3d import Vector3d
from vector3d import normalize

class Ray:
    _origin: Vector3d
    _direction: Vector3d

    def __init__(self, origin: Vector3d, direction: Vector3d):
        self._origin = origin
        self._direction = normalize(direction)

    def origin(self):
        return self._origin

    def direction(self):
        return self._direction

    def __call__(self, t):
        return self._origin + t * self._direction

    def __call__(self, point: Vector3d):
        return self._direction.dot(point - self._origin)

    def transform(self, t):
        return self

    def inverse_transform(self, t):
        return self

    