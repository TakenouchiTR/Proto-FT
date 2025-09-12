import threading
import time
from face_tracker import FaceTracker
from frame_builder import FrameBuilder
from image_renderer.image_renderer import ImageRenderer
from image_renderer.test_renderer import TestRenderer
import settings
import shape
from lerp_shape import LerpShape
import json

# Load mouth shapes
with open("shapes/mouth_closed.json", "r") as f:
    mouth_closed = shape.from_json(json.load(f))
with open("shapes/mouth_open.json", "r") as f:
    mouth_open = shape.from_json(json.load(f))
with open("shapes/eye_closed.json", "r") as f:
    eye_closed = shape.from_json(json.load(f))
with open("shapes/eye_open.json", "r") as f:
    eye_open = shape.from_json(json.load(f))

right_mouth_lerp_shape = LerpShape(mouth_closed)
right_mouth_lerp_shape.add_shape("open", mouth_open)

right_eye_lerp_shape = LerpShape(eye_closed)
right_eye_lerp_shape.add_shape_as_offset("open", eye_open)

face_tracker = FaceTracker()
frame_builder = FrameBuilder(settings.MATRIX_WIDTH, settings.MATRIX_HEIGHT)
image_renderer: ImageRenderer

def update_frame():
    while True:
        parameters = face_tracker.update()
        if parameters is None:
            time.sleep(0.1)
            continue

        right_mouth_lerp_shape.update_shape_strength("open", parameters.mouth_openness)
        right_eye_lerp_shape.update_shape_strength("open", parameters.mouth_openness)

        frame_builder.reset()

        frame_builder.draw_shape(right_mouth_lerp_shape.lerped_shape)
        frame_builder.draw_shape(right_eye_lerp_shape.lerped_shape)

        pixels = frame_builder.pixels
        image_renderer.render_pixels(pixels)

        time.sleep(0.01)

if settings.WINDOW_RENDER:
    image_renderer = TestRenderer()
    threading.Thread(target=update_frame, daemon=True).start()
    image_renderer.start()
else:
    pass
