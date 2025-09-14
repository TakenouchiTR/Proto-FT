import serial

from serial_reader.serial_reader import SerialReader


class TestReader(SerialReader):
    def __init__(self):
        self.serial = serial.serial_for_url("COM4", baudrate=115200, timeout=1)
        self.serial.reset_input_buffer()