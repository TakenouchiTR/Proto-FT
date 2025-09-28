import time
from face_shape_loader import load_face_shapes_from_file
from face_tracking.mp_tracker import MpTracker
from frame_builder import FrameBuilder, RenderSettings
from image_renderer.image_renderer import ImageRenderer
from image_renderer.pygame_renderer import PygameRenderer
from serial_writer.serial_writer import SerialWriter
from serial_writer.test_writer import TestWriter
import settings

face_shapes = load_face_shapes_from_file("data/shapes.json")
face_tracker = MpTracker()
frame_builder = FrameBuilder(settings.MATRIX_WIDTH, settings.MATRIX_HEIGHT)
serial_writer: SerialWriter
image_renderer: ImageRenderer

def update_frame():
    left_face_render_settings = RenderSettings()
    left_face_render_settings.flip_h = True
    left_face_render_settings.offset = (128, 0)

    prev_time = time.time()

    while True:
        new_time = time.time()
        print(new_time - prev_time)
        prev_time = new_time

        parameters = face_tracker.update()
        if parameters is None:
            time.sleep(0.01)
            continue


        # face_shapes.apply_weights(parameters)

        # image_renderer.render_face(face_shapes)
        # frame_builder.reset()

        # frame_builder.draw_shape(face_shapes.right_mouth.lerped_shape)
        # frame_builder.draw_shape(face_shapes.left_mouth.lerped_shape, left_face_render_settings)
        # frame_builder.draw_shape(face_shapes.right_eye.lerped_shape)
        # frame_builder.draw_shape(face_shapes.left_eye.lerped_shape, left_face_render_settings)

        # payload = frame_builder.to_bytes()
        # serial_writer.write_bytes(0, payload)

        time.sleep(0.01)

if __name__ == "__main__":
    # serial_writer = TestWriter()
    image_renderer = PygameRenderer()
    update_frame()