import tkinter as tk
from image_renderer.image_renderer import RenderSettings
from shape import Shape
import settings

def TestRenderer(ImageRenderer):
    def __init__(self):
        # Tkinter setup
        self.root = tk.Tk()
        self.root.title("LED Panel Simulation")
        self.canvas_width = settings.MATRIX_WIDTH * 10
        self.canvas_height = settings.MATRIX_HEIGHT * 10
        self.panel = tk.Label(self.root)
        self.panel.pack()
        self.root.mainloop()

    def draw_shape(self, shape: Shape, settings: RenderSettings = None):
        pass