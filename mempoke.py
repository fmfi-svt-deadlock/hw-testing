import gdb
import struct


class DeviceMemory:

    def __init__(self):
        self.inferior = gdb.selected_inferior()

    def __del__(self):
        del self.inferior

    def read(self, address):
        return struct.unpack('I', self.inferior.read_memory(address, 4))[0]

    def write(self, address, value):
        value_bytes = bytes(struct.unpack('4B', struct.pack('I', value)))
        self.inferior.write_memory(address, value_bytes, 4)
