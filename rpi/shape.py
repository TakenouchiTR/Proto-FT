from typing import List


class Shape:
    points: List[List[int, int]] = []

    def __init__(self, points: List[List[int, int]]):
        self.points = points
    
    def clone(self):
        return Shape([p for p in self.points])
    
    def rotated(self, angle: float, center: List[int, int] = (0, 0)):
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
    
    def flipped_x(self):
        return Shape([(-p[0], p[1]) for p in self.points])
    
    def flipped_y(self):
        return Shape([(p[0], -p[1]) for p in self.points])

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
            return Shape([(p[0] + other.points[i][0], p[1] + other.points[i][1]) for i, p in enumerate(self.points)])
        elif isinstance(other, (tuple, list)):
            return Shape([(p[0] + other[0], p[1] + other[1]) for p in self.points])
        else:
            raise TypeError("Other must be a Shape, tuple, or list")

    def __sub__(self, other):
        return Shape([(p[0] - other.points[i][0], p[1] - other.points[i][1]) for i, p in enumerate(self.points)])

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Shape([(p[0] * other, p[1] * other) for p in self.points])
        if isinstance(other, list) or isinstance(other, tuple):
            return Shape([(p[0] * other[0], p[1] * other[1]) for p in self.points])
        else:
            raise TypeError("Other must be a number, tuple, or list")

    def __neg__(self):
        return self * -1
    
    def __getitem__(self, index):
        return self.points[index]

def from_json(json_data: List[List[int]]):
    return Shape([(p[0], p[1]) for p in json_data])