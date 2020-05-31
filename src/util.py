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
    def process_bytes(reader: int) -> bytes:
        size_bytes = os.read(reader, 4)
        value_bytes = os.read(reader, Util.decode_value_len(size_bytes))
        return value_bytes

    @staticmethod
    def read_temp() -> float:
        temp_value = random.random() * 10
        return temp_value

    @staticmethod
    def encode_msg_size(size: int) -> bytes:
        return struct.pack('<I', size)

    @staticmethod
    def create_msg(content: bytes) -> bytes:
        dim = len(content)
        return Util.encode_msg_size(dim) + content

    @staticmethod
    def create_get_msg(content) -> bytes:
        return Util.create_msg(content)

    @staticmethod
    def create_response_msg(content):
        return Util.create_msg(bytearray(struct.pack('f', content)))
