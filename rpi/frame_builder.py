from typing import List, Tuple

import pygame
from shape import Shape
from PIL import Image, ImageDraw
import numpy as np
import settings

class RenderSettings:
    offset = (0, 0)
    scale = 1
    rotation = 0
    rotation_center = (0, 0)
    flip_h = False
    flip_v = False
    color = (255, 255, 255)

class FrameBuilder:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.pixels: List[List[Tuple[int, int, int]]] = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
        self.canvas = pygame.Surface((settings.MATRIX_WIDTH, settings.MATRIX_HEIGHT))
    
    def draw_shape(self, shape: Shape, render_settings: RenderSettings = None):        
        color = (255, 255, 255)

        if render_settings is not None:
            if render_settings.scale != 1:
                shape *= render_settings.scale
            if render_settings.rotation != 0:
                shape = shape.rotated(render_settings.rotation, render_settings.rotation_center)
            if render_settings.flip_h:
                shape = shape.flipped_x()
            if render_settings.flip_v:
                shape = shape.flipped_y()
            if render_settings.offset != (0, 0):
                shape += render_settings.offset
            color = render_settings.color

        rendered_pixels = polygon_to_pixels(shape, padding=2)
        for x, y in rendered_pixels:
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                continue
            self.pixels[y][x] = color

    def to_bytes(self):
        arr = np.array(self.pixels, dtype=np.uint8)
        return arr.tobytes()

    def reset(self):
        self.pixels = [[(0, 0, 0) for _ in range(self.width)] for _ in range(self.height)]

def polygon_to_pixels(polygon: Shape, padding=1):
    """
    Convert a polygon (list of (x, y) floats) into a list of integer pixel (x, y) coordinates.
    
    Args:
        polygon: List of (x, y) points as floats.
        padding: Number of extra pixels added as padding around the bounding box.

    Returns:
        List of (x, y) tuples for pixels inside the polygon.
    """
    # Find bounds and shift polygon to origin for rasterization
    min_x = min(p[0] for p in polygon)
    min_y = min(p[1] for p in polygon)
    max_x = max(p[0] for p in polygon)
    max_y = max(p[1] for p in polygon)
    
    # Compute size with padding
    width = int(max_x - min_x + 2 * padding + 1)
    height = int(max_y - min_y + 2 * padding + 1)
    
    # Shift polygon to fit in image with padding
    shifted_polygon = [
        (p[0] - min_x + padding, p[1] - min_y + padding)
        for p in polygon
    ]
    
    # Create blank image and draw filled polygon
    img = Image.new("1", (width, height), 0)  # mode "1" = binary
    draw = ImageDraw.Draw(img)
    draw.polygon(shifted_polygon, fill=1)
    
    # Get pixels that are inside
    pixels = []
    for y in range(height):
        for x in range(width):
            if img.getpixel((x, y)):
                # Shift back to original coordinates
                orig_x = x + min_x - padding
                orig_y = y + min_y - padding
                pixels.append((int(orig_x), int(orig_y)))
    
    return pixels