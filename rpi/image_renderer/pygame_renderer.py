from face_shape_loader import FaceShapes
from image_renderer.image_renderer import ImageRenderer
import os
import pygame

import settings


class PygameRenderer(ImageRenderer):
    def __init__(self):
        #create a window, make full screen
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        self.screen = pygame.display.set_mode((3940, 1080), pygame.NOFRAME)
        self.canvas = pygame.Surface((settings.MATRIX_WIDTH, settings.MATRIX_HEIGHT))

        pass

    def render_face(self, face: FaceShapes):
        self.screen.fill((0, 0, 0))
        self.canvas.fill((0, 0, 0))

        pygame.draw.polygon(self.canvas, (255, 255, 255), face.right_eye.lerped_shape.points, 0)
        pygame.draw.polygon(self.canvas, (255, 255, 255), face.right_mouth.lerped_shape.points, 0)
        pygame.draw.polygon(self.canvas, (255, 255, 255), face.left_mouth.lerped_shape.points, 0)
        pygame.draw.polygon(self.canvas, (255, 255, 255), face.left_eye.lerped_shape.points, 0)

        
        stretched = pygame.transform.scale(self.canvas, self.screen.get_size())
        self.screen.blit(stretched, (0, 0))
        
        pygame.display.flip()