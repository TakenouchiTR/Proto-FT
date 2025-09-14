import serial
from serial_writer.serial_writer import SerialWriter


class TestWriter(SerialWriter):
    def __init__(self):
        self.serial = serial.Serial("COM5", baudrate=115200, timeout=1)
        self.serial.reset_output_buffer()