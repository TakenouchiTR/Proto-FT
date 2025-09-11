import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import cv2
from face_tracker import FaceTracker
import settings
import shape
from lerp_shape import LerpShape
import json

# Load mouth shapes
with open("shapes/mouth_closed.json", "r") as f:
    mouth_closed = shape.from_json(json.load(f))
with open("shapes/mouth_open.json", "r") as f:
    mouth_open = shape.from_json(json.load(f))
lerp_shape = LerpShape(mouth_closed)
lerp_shape.add_shape("open", mouth_open)

face_tracker = FaceTracker()

# Tkinter setup
root = tk.Tk()
root.title("LED Panel Simulation")
canvas_width = settings.MATRIX_WIDTH * 10
canvas_height = settings.MATRIX_HEIGHT * 10
panel = tk.Label(root)
panel.pack()

def update_frame():
    parameters = face_tracker.update()
    if parameters is None:
        root.after(50, update_frame)
        return

    img = Image.new('RGB', (settings.MATRIX_WIDTH, settings.MATRIX_HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    lerp_shape.update_shape_strength("open", parameters.mouth_openness)
    draw.polygon(lerp_shape.lerped_shape.points, fill=(255, 100, 100))

    # Update LED simulation
    imgtk = ImageTk.PhotoImage(img.resize((canvas_width, canvas_height), resample=Image.NEAREST))
    panel.config(image=imgtk)
    panel.image = imgtk

    root.after(1, update_frame)

# Start the loop in main thread
update_frame()
root.mainloop()
