from image_renderer.image_renderer import ImageRenderer
from serial_reader.serial_reader import SerialReader
import settings

image_renderer: ImageRenderer
serial_reader: SerialReader

def updateFrame():
    frame_data_size = settings.MATRIX_WIDTH * settings.MATRIX_HEIGHT * 3

    while True:
        command, data = serial_reader.read_serial()

        if command == -1:
            continue
        if command == 0:
            if (len(data) != frame_data_size):
                continue
            
            image_renderer.render_bytes(data)

if settings.LOCAL_DEVELOPMENT:
    try:
        import threading
        from serial_reader.test_reader import TestReader
        from image_renderer.test_renderer import TestRenderer
    except:
        pass
    image_renderer = TestRenderer()
    serial_reader = TestReader()
    threading.Thread(target=updateFrame, daemon=True).start()
    image_renderer.start()
else:
    from serial_reader.usb_cdc_reader import UsbCdcReader
    from image_renderer.hub75_renderer import Hub75Renderer
    image_renderer = Hub75Renderer()
    serial_reader = UsbCdcReader()
    updateFrame()