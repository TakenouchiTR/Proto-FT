from shape import Shape
from typing import Dict


class LerpShape:

    def __init__(self, base_shape: Shape):
        if isinstance(base_shape, list):
            base_shape = Shape(base_shape)
        
        self.shapes: Dict[str, Shape] = {}
        self.shape_strengths: Dict[str, float] = {}
        self._base_shape = base_shape.clone()
        self.lerped_shape = base_shape.clone()
    
    def get_shape(self, name: str):
        return self.shapes[name]
    
    def get_shape_strength(self, name: str):
        return self.shape_strengths[name]

    def add_shape(self, name: str, shape: Shape, strength: float = 0.0):
        if isinstance(shape, list):
            shape = Shape(shape)

        self.shapes[name] = shape - self._base_shape
        self.shape_strengths[name] = strength

        self.update_lerped_shape()
    
    def add_shape_as_offset(self, name: str, shape: Shape, strength: float = 0.0):
        if isinstance(shape, list):
            shape = Shape(shape)
        self.add_shape(name, shape + self._base_shape, strength)

    def update_shape_strength(self, name: str, strength: float):
        self.shape_strengths[name] = min(1.0, max(0.0, strength))
    
    def update_lerped_shape(self):
        num_points = len(self.lerped_shape.points)

        for i in range(num_points):
            x = sum(self.shape_strengths[name] * self.shapes[name][i][0] for name in self.shapes)
            y = sum(self.shape_strengths[name] * self.shapes[name][i][1] for name in self.shapes)

            x += self._base_shape[i][0]
            y += self._base_shape[i][1]

            self.lerped_shape.points[i][0] = x
            self.lerped_shape.points[i][1] = y
    
    def flip_x(self):
        self._base_shape = self._base_shape.flip_x()
        for key, shape in self.shapes.items():
            self.shapes[key] = shape.flip_x()
        return self

    def flip_y(self):
        self._base_shape = self._base_shape.flip_y()
        for key, shape in self.shapes.items():
            self.shapes[key] = shape.flip_y()
        return self

    def __add__(self, other):
        self._base_shape += other
        return self
    
    def __sub__(self, other):
        self._base_shape -= other
        return self

    def __mul__(self, other):
        self._base_shape *= other
        for key, shape in self.shapes.items():
            self.shapes[key] = shape * other
        return self
    
    def __neg__(self):
        self._base_shape = -self._base_shape
        for key, shape in self.shapes.items():
            self.shapes[key] = -shape
        return self
