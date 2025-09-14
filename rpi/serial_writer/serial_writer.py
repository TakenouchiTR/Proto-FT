from serial import Serial

class SerialWriter():
    def __init__(self):
        self.serial: Serial

    def write_bytes(self, instruction: int, data: bytes):
        instruction = instruction.to_bytes(1)
        payload_length = len(data).to_bytes(4)

        payload = instruction + payload_length + data

        self.serial.write(payload)