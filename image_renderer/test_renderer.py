import threading
import tkinter as tk
from typing import List, Tuple
from image_renderer.image_renderer import ImageRenderer
import settings
from PIL import Image, ImageDraw, ImageTk

class TestRenderer(ImageRenderer):
    def __init__(self):
        # Tkinter setup
        self.root = tk.Tk()
        self.root.title("LED Panel Simulation")
        self.canvas_width = settings.MATRIX_WIDTH * settings.WINDOW_RENDER_SCALE
        self.canvas_height = settings.MATRIX_HEIGHT * settings.WINDOW_RENDER_SCALE
        self.panel = tk.Label(self.root)
        self.panel.pack()

        self._lock = threading.Lock()

    def start(self):
        self.root.mainloop()

    def render_pixels(self, pixels: List[List[Tuple[int, int, int]]]):
        with self._lock:
            img = Image.new('RGB', (settings.MATRIX_WIDTH, settings.MATRIX_HEIGHT), color=(0, 0, 0))
            draw = ImageDraw.Draw(img)

            pixel_size = settings.WINDOW_RENDER_SCALE

            for row in range(len(pixels)):
                for col in range(len(pixels[row])):
                    draw.rectangle((col * pixel_size, row * pixel_size, (col + 1) * pixel_size, (row + 1) * pixel_size), fill=pixels[row][col])
            
            
            for row in range(len(pixels)):
                for col in range(len(pixels[row])):
                    if pixels[row][col] != (0, 0, 0):
                        print('#', end='')
                    else:
                        print(' ', end='')
                print()
                    

            imgtk = ImageTk.PhotoImage(img.resize((self.canvas_width, self.canvas_height), resample=Image.NEAREST))
            self.panel.config(image=imgtk)
            self.panel.image = imgtk
