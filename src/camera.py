from .vector3d import Vector3d, normalize
import math
from .ray import Ray
from .boundingbox import BoundingBox

class Camera:
    _eye: Vector3d
    _view: Vector3d
    _up: Vector3d
    _fov: float
    _width: int
    _height: int

    def __init__(self, *args):
        # No parameters
        if(len(args) == 0):
            self._eye = Vector3d()
            self._view = Vector3d(0.0, 0.0, -1.0)
            self._up = Vector3d(0.0, 1.0, 0.0)
            self._fov = 60.0
            self._width = self._height = 256
        
        elif len(args) == 6:
            eye, viewDirection, up, fov, xres, yres = args
            self._eye = eye
            self._view = normalize(viewDirection)
            self._up = normalize(up)
            self._fov = fov
            self._width = xres
            self._height = yres

            right = self._view.cross(up).normalize()
            self._up = right.cross(self._view).normalize()
    
    def __repr__(self):
        return f"Camera: {{eye = {self._eye}, view = {self._view}, up = {self._up}}}, fov = {self._fov}, resolution = [{self._width}x{self._height}]"

    def __call__(self, x: float, y:float):
        right = self._view.cross(self._up).normalize()
        aspect = float(self._height) / float(self._width)
        tan_fov = math.tan(self._fov / 180.0 * 3.14159265359)
        center = self._eye + self._view
        U = 2.0 * tan_fov * right
        V = -2.0 * tan_fov * aspect * self._up
        p = center + (x / float(self._width) - 0.5) * U + (y / float(self._height) - 0.5) * V
        return Ray(self._eye, p - self._eye)
    
    def width(self):
        return self._width

    def height(self):
        return self._height
    
    def frame_bounding_box(self, bb: BoundingBox):
        right = self._view.cross(self._up).normalize()
        self._eye = 0.5 * (bb.corner(True, True, True) + bb.corner(False, False, False))
        max_right = -10e10
        max_up = -10e10
        max_depth = -10e10

        for i in range(8):
            c = bb.corner((i & 1) == 1, (i & 2) == 2, (i & 4) == 4) - self._eye
    
            r = abs(c.dot(right))
            u = abs(c.dot(self._up))
            d = abs(c.dot(self._view))

            max_right = max(max_right, r)
            max_up = max(max_up, u)
            max_depth = max(max_depth, d)
        
        aspect = float(self._height) / float(self._width)
        tan_fov = math.tan(self._fov / 180.0 * 3.14159265359)
        opt_dist_up = abs(max_up / tan_fov)
        opt_dist_right = abs(max_right / (tan_fov * aspect))
        self._eye -= self._view * (max(opt_dist_up, opt_dist_right) + max_depth)
    
def swap(a: Camera, b: Camera):
    a._eye, b._eye = b._eye, a._eye
    a._view, b._view = b._view, a._view
    a._up, b._up = b._up, a._up
    a._fov, b._fov = b._fov, a._fov
    a._width, b._width = b._width, a._width
    a._height, b._height = b._height, a._height
    