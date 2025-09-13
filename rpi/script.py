import threading
import time
from face_shape_loader import load_face_shapes_from_file
from face_tracking.mp_tracker import MpTracker
from frame_builder import FrameBuilder, RenderSettings
from image_renderer.image_renderer import ImageRenderer
from image_renderer.test_renderer import TestRenderer
import settings

face_shapes = load_face_shapes_from_file("data/shapes.json")
face_tracker = MpTracker()
frame_builder = FrameBuilder(settings.MATRIX_WIDTH, settings.MATRIX_HEIGHT)
image_renderer: ImageRenderer

def update_frame():
    left_face_render_settings = RenderSettings()
    left_face_render_settings.flip_h = True
    left_face_render_settings.offset = (128, 0)

    while True:
        parameters = face_tracker.update()
        if parameters is None:
            time.sleep(0.01)
            continue

        face_shapes.apply_weights(parameters)
        frame_builder.reset()

        frame_builder.draw_shape(face_shapes.right_mouth.lerped_shape)
        frame_builder.draw_shape(face_shapes.left_mouth.lerped_shape, left_face_render_settings)
        frame_builder.draw_shape(face_shapes.right_eye.lerped_shape)
        frame_builder.draw_shape(face_shapes.left_eye.lerped_shape, left_face_render_settings)

        image_renderer.render_pixels(frame_builder.pixels)

        time.sleep(0.01)

if settings.WINDOW_RENDER:
    image_renderer = TestRenderer()
    threading.Thread(target=update_frame, daemon=True).start()
    image_renderer.start()
else:
    pass
