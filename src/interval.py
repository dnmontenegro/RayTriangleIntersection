class Interval:
    _lower: float
    _upper: float

    def __init__(self, lower: float, upper: float):
        self._lower = lower
        self._upper = upper
        if self._upper < self._lower:
            self._lower, self._upper = self._upper, self._lower

    def __repr__(self):
        return f"{self.lower()}, {self.upper()}"
    
    def __add__(self, v: float):
        return Interval(self._lower + v, self._upper + v)

    def __sub__(self, v: float):
        return Interval(self._lower - v, self._upper - v)

    def __mul__(self, v: float):
        return Interval(self._lower * v, self._upper * v)

    def __truediv__(self, v: float):
        return Interval(self._lower / v, self._upper / v)

    def __iadd__(self, v: float):
        self._lower += v
        self._upper += v
        return self

    def __isub__(self, v: float):
        self._lower -= v
        self._upper -= v
        return self

    def __imul__(self, v: float):
        self._lower *= v
        self._upper *= v
        if self._upper < self._lower:
            self._lower, self._upper = self._upper, self._lower
        return self

    def __itruediv__(self, v: float):
        self._lower /= v
        self._upper /= v
        if self._upper < self._lower:
            self._lower, self._upper = self._upper, self._lower
        return self

    def lower(self):
        return self._lower

    def upper(self):
        return self._upper
    
    def empty(self):
        return (self._upper - self._lower) < 10e-6
    
    def intersect(self, i):
        self._lower = max(self._lower, i._lower)
        self._upper = min(self._upper, i._upper)

def swap(a: Interval, b: Interval):
    a._lower, b._lower = b._lower , a._lower 
    a._upper, b._upper = b._upper , a._upper