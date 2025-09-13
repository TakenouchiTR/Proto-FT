import threading
import tkinter as tk
from typing import List, Tuple
from image_renderer.image_renderer import ImageRenderer
import settings
from PIL import Image, ImageTk

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
        self._latest_img = None  # store latest PIL image for UI thread consumption

    def start(self):
        self.root.mainloop()

    def render_pixels(self, pixels: List[List[Tuple[int, int, int]]]):
        # Build a 1:1 image (matrix size), then scale for display.
        # Do NOT touch Tk widgets from this worker thread.
        img = Image.new('RGB', (settings.MATRIX_WIDTH, settings.MATRIX_HEIGHT), color=(0, 0, 0))

        # Fast path: flatten and putdata
        flat = []
        for row in pixels:
            flat.extend(row)
        img.putdata(flat)

        # Hand off to Tk main thread to update the UI
        with self._lock:
            self._latest_img = img
        self.root.after(0, self._update_image)

    def _update_image(self):
        # Runs on Tk main thread
        with self._lock:
            img = self._latest_img
            self._latest_img = None
        if img is None:
            return
        imgtk = ImageTk.PhotoImage(img.resize((self.canvas_width, self.canvas_height), resample=Image.NEAREST))
        self.panel.config(image=imgtk)
        self.panel.image = imgtk
