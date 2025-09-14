import threading
from image_renderer.image_renderer import ImageRenderer
from image_renderer.test_renderer import TestRenderer
from serial_reader.serial_reader import SerialReader
from serial_reader.test_reader import TestReader
import settings

image_renderer: ImageRenderer
serial_reader: SerialReader

def updateFrame():
    frame_data_size = settings.MATRIX_WIDTH * settings.MATRIX_HEIGHT * 3

    while True:
        command, data = serial_reader.read_serial()

        match command:
            case 0:
                if (len(data) != frame_data_size):
                    continue
                
                image_renderer.render_bytes(data)

if settings.WINDOW_RENDER:
    image_renderer = TestRenderer()
    serial_reader = TestReader()
    threading.Thread(target=updateFrame, daemon=True).start()
    image_renderer.start()
else:
    pass