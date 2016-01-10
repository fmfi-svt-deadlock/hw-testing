# import gdb
import struct


class DeviceMemory:
    def __init__(self):
        self.inferior = gdb.selected_inferior()

    def __del__(self):
        del self.inferior

    def read(self, t, address):
        return struct.unpack(t[CODE], self.inferior.read_memory(address, 4))[0]

    def write(self, type, address, value):
        value_bytes = struct.pack(t[CODE], value)
        self.inferior.write_memory(address, value_bytes)

CODE = 0
LENGTH = 1


class T(object):
    uint8_t = ('B', 1)
    uint16_t = ('H', 2)
    uint32_t = ('I', 4)
    uint64_t = ('Q', 8)
    int8_t = ('b', 1)
    int16_t = ('h', 2)
    int32_t = ('i', 4)
    int64_t = ('q', 8)

TYPE = 0
OFFSET = 1


class MMPeripheral(object):
    """Memory Mapped MCU Peripheral"""

    compiled_fields = {}

    def __init__(self, address, device_memory):
        self.device_memory = device_memory
        self.address = address
        offset = 0
        for t, name in self.fields:
            if name is not None:
                self.compiled_fields[name] = (t, offset)
            offset += t[LENGTH]

    def __getattr__(self, name):
        if name in self.compiled_fields:
            return self.device_memory.read(self.compiled_fields[name][TYPE],
                                           self.address + self.compiled_fields[name][OFFSET])
        else:
            raise ValueError('This peripheral does not contain register ' + name)

    def __setattr__(self, name, value):
        if name in self.compiled_fields:
            self.device_memory.write(self.compiled_fields[name][TYPE],
                                     self.address + self.compiled_fields[name][OFFSET], value)
        else:
            super(MMPeripheral, self).__setattr__(name, value)
