
from image_renderer.image_renderer import ImageRenderer
import hub75
import settings


class Hub75Renderer(ImageRenderer):
    def __init__(self):
        super().__init__()
        width = settings.MATRIX_WIDTH
        height = settings.MATRIX_HEIGHT
        self.matrix = hub75.Hub75(width, height)
    
    def render_pixels(self, pixels: list[list[tuple[int, int, int]]]):
        self.matrix.set_pixels(pixels)
