from shape import Shape
from typing import Dict


class LerpShape:

    def __init__(self, base_shape: Shape):
        if isinstance(base_shape, list):
            base_shape = Shape(base_shape)
        
        self.shapes: Dict[str, Shape] = {}
        self.shape_strengths: Dict[str, float] = {}
        self._base_shape = base_shape.clone()
        self.lerped_shape = Shape([])
    
    def get_shape(self, name: str):
        return self.shapes[name]
    
    def get_shape_strength(self, name: str):
        return self.shape_strengths[name]

    def add_shape(self, name: str, shape: Shape, strength: float = 1.0):
        if isinstance(shape, list):
            shape = Shape(shape)
        if not self.shapes:
            self.lerped_shape = shape.clone()

        self.shapes[name] = shape - self._base_shape
        self.shape_strengths[name] = strength

        self.update_lerped_shape()
    
    def add_shape_as_offset(self, name: str, shape: Shape, strength: float = 1.0):
        if isinstance(shape, list):
            shape = Shape(shape)
        if not self.shapes:
            self.lerped_shape = shape.clone()
        self.add_shape(name, shape + self._base_shape, strength)

    def update_shape_strength(self, name: str, strength: float):
        self.shape_strengths[name] = min(1.0, max(0.0, strength))

        self.update_lerped_shape()
    
    def update_lerped_shape(self):
        new_points = []
        num_points = len(self.lerped_shape.points)

        for i in range(num_points):
            x = sum(self.shape_strengths[name] * self.shapes[name][i][0] for name in self.shapes)
            y = sum(self.shape_strengths[name] * self.shapes[name][i][1] for name in self.shapes)

            x += self._base_shape[i][0]
            y += self._base_shape[i][1]

            new_points.append((int(x), int(y)))
        
        self.lerped_shape = Shape(new_points)
    
    def __add__(self, other):
        for key, shape in self.shapes.items():
            self.shapes[key] = shape + other
        return self
    
    def __sub__(self, other):
        for key, shape in self.shapes.items():
            self.shapes[key] = shape - other
        return self

    def __mul__(self, other):
        for key, shape in self.shapes.items():
            self.shapes[key] = shape * other
        return self
    
    def __neg__(self):
        for key, shape in self.shapes.items():
            self.shapes[key] = -shape
        return self
