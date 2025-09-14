from serial import Serial


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

        print(f'reading {length} bytes')
        data = self.serial.read(length)
        self.serial.flush()

        return command, data