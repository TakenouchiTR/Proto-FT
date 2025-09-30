from face_shape_loader import FaceShapes
from image_renderer.image_renderer import ImageRenderer
import os
import pygame
import numpy as np
import cv2

import settings


class PygameRenderer(ImageRenderer):
    def __init__(self):
        #create a window, make full screen
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        self.screen = pygame.display.set_mode((3940, 1080), pygame.NOFRAME)
        self.canvas = pygame.Surface((settings.MATRIX_WIDTH, settings.MATRIX_HEIGHT))
        self.np_buffer = np.zeros((settings.MATRIX_WIDTH, settings.MATRIX_HEIGHT, 3), dtype=np.uint8)

    def render_face(self, face: FaceShapes):
        self.np_buffer.fill(0)

        polys = [
            np.array(face.right_eye.lerped_shape.points, dtype=np.int32),
            np.array(face.right_mouth.lerped_shape.points, dtype=np.int32),
            np.array(face.left_eye.lerped_shape.points, dtype=np.int32),
            np.array(face.left_mouth.lerped_shape.points, dtype=np.int32),
        ]


        for poly in polys:
            cv2.fillPoly(self.np_buffer, [poly], (255, 255, 255))
        
        pygame.surfarray.blit_array(self.canvas, self.np_buffer.swapaxes(0, 1))
        
        stretched = pygame.transform.scale(self.canvas, self.screen.get_size())
        self.screen.blit(stretched, (0, 0))
        
        pygame.display.flip()