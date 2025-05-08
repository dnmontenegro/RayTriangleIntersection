from .vector3d import Vector3d
import copy
from .ray import Ray
from .interval import Interval
from .transformation3d import Transformation3d

class BoundingBox:
    _lfb: Vector3d
    _rbt: Vector3d

    def __init__(self, *args):
        # No parameters
        if(len(args) == 0):
            self._lfb = Vector3d(10e10)
            self._rbt = Vector3d(-10e10)
        
        # Two vectices
        elif len(args) == 2:
            self._lfb = args[0]
            self._rbt = args[1]
            for i in range(Vector3d.size()):
                if self._rbt[i] < self._lfb[i]:
                     self._lfb[i], self._rbt[i] = self._rbt[i], self._lfb[i]

    def __repr__(self):
        return f"{self._lfb} - {self._rbt}"

    def __iadd__(self, other):
        if isinstance(other, BoundingBox): 
            for i in range(Vector3d.size()):
                if self._lfb[i] > other._lfb[i]:
                    self._lfb[i] = other._lfb[i]
                if self._rbt[i] < other._rbt[i]:
                    self._rbt[i] = other._rbt[i]
            return self

        elif isinstance(other, Vector3d):
            for i in range(Vector3d.size()):
                if self._lfb[i] > (other[i] - 10e-6):
                    self._lfb[i] = other[i] - 10e-6
                if self._rbt[i] < (other[i] + 10e-6):
                    self._rbt[i] = other[i] + 10e-6
            return self

    def __add__(self, bb):
        result = BoundingBox(copy.copy(self._lfb), copy.copy(self._rbt))
        result += bb
        return result
    
    def is_hit(self, r: Ray):
        box_interval = Interval(0, 10e10)

        for i in range(Vector3d.size()):
            slab = Interval(self._lfb[i], self._rbt[i])
            slab -= r.origin()[i]

            if abs(r.direction()[i]) < 10e-6:
                if (slab.lower() < 0.0) == (slab.upper() < 0.0):
                    return False
                continue
            else:
                slab /= r.direction()[i]

            box_interval.intersect(slab)
            if box_interval.empty():
                return False
            
        return True
    
    def center(self):
        return 0.5 * (self._lfb + self._rbt)

    def corner(self, left: bool, front: bool, bottom: bool):
        return Vector3d(self._lfb.vec[0] if left else self._rbt.vec[0], self._lfb.vec[1] if front else self._rbt.vec[1], self._lfb.vec[2] if bottom else self._rbt.vec[2])

    def size(self):
        s = (self._rbt - self._lfb)
        if s[0] < 0 or s[1] < 0 or s[2] < 0:
            return Vector3d()
        else:
            return s

    def transform(self, t: Transformation3d):
        result = BoundingBox()
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    result += t.transform_point(self.corner(i, j, k))
        self._lfb, result._lfb = result._lfb, self._lfb
        self._rbt, result._rbt = result._rbt, self._rbt
        return self

    def inverse_transform(self, t: Transformation3d):
        result = BoundingBox()
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    result += t.inverse_transform_point(self.corner(i, j, k))
        self._lfb, result._lfb = result._lfb, self._lfb
        self._rbt, result._rbt = result._rbt, self._rbt
        return self

def swap(a: BoundingBox, b: BoundingBox):
    a._lfb, b._lfb = b._lfb, a._lfb
    a._rbt, b._rbt = b._rbt, a._rbt

def transform(bb: BoundingBox, t: Transformation3d):
    result = BoundingBox()
    for i in range(2):
        for j in range(2):
            for k in range(2):
                result += t.transform_point(bb.corner(i, j, k))
    return result

def inverse_transform(bb: BoundingBox, t: Transformation3d):
    result = BoundingBox()
    for i in range(2):
        for j in range(2):
            for k in range(2):
                result += t.transform_point(bb.corner(i, j, k))
    return result
