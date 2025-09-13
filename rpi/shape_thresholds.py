class ShapeThreshold:
    minimum = 0.0
    maximum = 1.0

    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum
    
    def lerp(self, value, clamp = True):
        if clamp:
            value = max(min(value, self.maximum), self.minimum)
        return (value - self.minimum) / (self.maximum - self.minimum)

MOUTH_OPENNESS = ShapeThreshold(0.03, 0.25)
MOUTH_SMILE = ShapeThreshold(0.00, 0.09)
MOUTH_POG = ShapeThreshold(0.50, 1.40)
EYE_OPENNESS = ShapeThreshold(0.82, 0.90)