from serial_reader.serial_reader import SerialReader
import settings
import usb_cdc

frame_data_size = settings.MATRIX_WIDTH * settings.MATRIX_HEIGHT * 3

class UsbCdcReader(SerialReader):
    def __init__(self):
        usb_cdc.data.timeout = 0
        usb_cdc.data.read()  # clear buffer

    def read_serial(self):
        instructions = usb_cdc.data.read(5)
        print(f"Got instructions: {instructions}")

        if len(instructions) < 5:
            print(f"not enough data: {len(instructions)}")
            return -1, None

        command = instructions[0]
        length = int.from_bytes(instructions[1:], 'big')

        if command == 0 and length != frame_data_size:
            print(f"frame wrong size: {length}. Flushing buffer...")
            usb_cdc.data.read()  # clear buffer

        print(f'reading {length} bytes')
        data = usb_cdc.data.read(length)

        return command, data