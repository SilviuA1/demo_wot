import struct
import os
import random


class Util:
    @staticmethod
    def decode_value_len(size: bytes) -> int:
        return struct.unpack('<I', size)[0]

    @staticmethod
    def decode_value(value: bytes) -> float:
        return struct.unpack('f', value)[0]

    @staticmethod
    def process_bytes(reader: int) -> float:
        size_bytes = os.read(reader, 4)
        value_bytes = os.read(reader, Util.decode_value_len(size_bytes))
        return Util.decode_value(value_bytes)

    @staticmethod
    def read_temp() -> float:
        temp_value = random.random() * 10
        return temp_value
