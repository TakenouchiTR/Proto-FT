from typing import List, Tuple


class Shape:
    points: List[Tuple[int, int]] = []

    def __init__(self, points: List[Tuple[int, int]]):
        self.points = points
    
    def clone(self):
        return Shape([p for p in self.points])
    
    def rotated(self, angle: float, center: Tuple[int, int] = (0, 0)):
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
        width = self.get_width()
        left = self.left()
        offset_amount = width + left

        return Shape([(-p[0] + offset_amount, p[1]) for p in self.points])
    
    def flipped_y(self):
        height = self.get_height()
        top = self.top()
        offset_amount = height + top

        return Shape([(p[0], -p[1] + offset_amount) for p in self.points])

    
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
        if other is int or other is float:
            return Shape([(p[0] * other, p[1] * other) for p in self.points])
        if other is tuple or other is list:
            return Shape([(p[0] * other[0], p[1] * other[1]) for p in self.points])
        else:
            raise TypeError("Other must be a number, tuple, or list")
    
    def __getitem__(self, index):
        return self.points[index]

def from_json(json_data: List[List[int]]):
    return Shape([(p[0], p[1]) for p in json_data])