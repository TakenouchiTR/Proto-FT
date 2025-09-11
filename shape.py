from typing import List, Tuple


class Shape:
    points: List[Tuple[int, int]] = []

    def __init__(self, points: List[Tuple[int, int]]):
        self.points = points
    
    def clone(self):
        return Shape([p for p in self.points])
    
    def __add__(self, other):
        return Shape([(p[0] + other.points[i][0], p[1] + other.points[i][1]) for i, p in enumerate(self.points)])

    def __sub__(self, other):
        return Shape([(p[0] - other.points[i][0], p[1] - other.points[i][1]) for i, p in enumerate(self.points)])
    
    def __getitem__(self, index):
        return self.points[index]

def from_json(json_data: List[List[int]]):
    return Shape([(p[0], p[1]) for p in json_data])