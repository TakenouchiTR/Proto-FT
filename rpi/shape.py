from typing import List


class Shape:
    points: List[List[int]] = []

    def __init__(self, points: List[List[int]]):
        # Deep-copy to avoid aliasing external lists (e.g., JSON data)
        # and to ensure each Shape instance owns its own mutable points.
        self.points = [list(p) for p in points]
    
    def clone(self):
        # Deep-clone the points to avoid sharing inner lists
        return Shape([p[:] for p in self.points])
    
    def rotated(self, angle: float, center: List[int] = (0, 0)):
        return Shape([(p[0] * angle + center[0], p[1] * angle + center[1]) for p in self.points])
    
    def centered(self):
        center = self.get_center()
        return Shape([(p[0] - center[0], p[1] - center[1]) for p in self.points])

    
    def get_width(self):
        return max(p[0] for p in self.points) - min(p[0] for p in self.points)
    
    def get_height(self):
        return max(p[1] for p in self.points) - min(p[1] for p in self.points)
    
    def get_center(self):
        return (sum(p[0] for p in self.points) / len(self.points), sum(p[1] for p in self.points) / len(self.points))
    
    def get_area(self):
        return self.get_width() * self.get_height()
    
    def get_height(self):
        return max(p[1] for p in self.points) - min(p[1] for p in self.points)
    
    def left(self):
        return min(p[0] for p in self.points)
    
    def right(self):
        return max(p[0] for p in self.points)
    
    def top(self):
        return min(p[1] for p in self.points)
    
    def bottom(self):
        return max(p[1] for p in self.points)
    
    def flip_x(self):
        for point in self.points:
            point[0] *= -1
        return self
    
    def flip_y(self):
        for point in self.points:
            point[1] *= -1
        return self

    def copy_from(self, other: 'Shape'):
        if len(self.points) != len(other.points):
            self.points = other.points[:]
            for i in range(len(self.points)):
                self.points[i] = self.points[i][:]
            return
        
        for i in range(len(self.points)):
            self.points[i] = other.points[i][:]
    
    def __len__(self):
        return len(self.points)
    
    def __iter__(self):
        return iter(self.points)
    
    def __getitem__(self, index):
        return self.points[index]
    
    def __add__(self, other):
        if isinstance(other, Shape):
            if len(self.points) != len(other.points):
                raise ValueError("Shapes must have the same number of points")
            for i, point in enumerate(self.points):
                point[0] += other.points[i][0]
                point[1] += other.points[i][1]
            return self
        elif isinstance(other, (tuple, list)):
            for i, point in enumerate(self.points):
                point[0] += other[0]
                point[1] += other[1]
            return self
        else:
            raise TypeError("Other must be a Shape, tuple, or list")

    def __sub__(self, other):
        if isinstance(other, Shape):
            if len(self.points) != len(other.points):
                raise ValueError("Shapes must have the same number of points")
            for i, point in enumerate(self.points):
                point[0] -= other.points[i][0]
                point[1] -= other.points[i][1]
            return self
        elif isinstance(other, (tuple, list)):
            for i, point in enumerate(self.points):
                point[0] -= other[0]
                point[1] -= other[1]
            return self
        else:
            raise TypeError("Other must be a Shape, tuple, or list")
        

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            for i, point in enumerate(self.points):
                point[0] *= other
                point[1] *= other
            return self
        if isinstance(other, (list, tuple)):
            for i, point in enumerate(self.points):
                point[0] *= other[0]
                point[1]*= other[1]
            return self
        else:
            raise TypeError("Other must be a number, tuple, or list")

    def __neg__(self):
        return self * -1
    
    def __getitem__(self, index):
        return self.points[index]

def from_json(json_data: List[List[int]]):
    return Shape([(p[0], p[1]) for p in json_data])
