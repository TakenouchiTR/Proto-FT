from serial import Serial

import settings

frame_data_size = settings.MATRIX_WIDTH * settings.MATRIX_HEIGHT * 3

class SerialReader():

    def __init__(self):
        self.serial: Serial

    def read_serial(self):
        
        instructions = self.serial.read(5)
        print(f"Got instructions: {instructions}")

        if len(instructions) < 5:
            print(f"not enough data: {len(instructions)}")
            return -1, None

        command = instructions[0]
        length = int.from_bytes(instructions[1:])
        
        if command == 0 and length > frame_data_size:
            print(f"frame too large: {length}. Flushing buffer...")
            self.serial.reset_input_buffer()

        print(f'reading {length} bytes')
        data = self.serial.read(length)
        self.serial.flush()

        return command, data