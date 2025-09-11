from shape import Shape

class RenderSettings:
    offset = (0, 0)
    scale = 1
    rotation = 0
    flip_h = False
    flip_v = False
    color = (255, 255, 255)

class ImageRenderer:
    def draw_shape(self, shape: Shape, settings: RenderSettings = None):
        pass

class TestRenderer(ImageRenderer):
    def draw_shape(self, shape: Shape, settings: RenderSettings = None):
        pass

    def reset(self):
        pass