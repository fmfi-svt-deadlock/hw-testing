import gdb
import struct


class T(object):
    FORMAT_CHAR = 0
    LENGTH = 1

    uint8_t = ('B', 1)
    uint16_t = ('H', 2)
    uint32_t = ('I', 4)
    uint64_t = ('Q', 8)
    int8_t = ('b', 1)
    int16_t = ('h', 2)
    int32_t = ('i', 4)
    int64_t = ('q', 8)


class DeviceMemory:

    ENDIANITY = '<'

    def __init__(self):
        self.inferior = gdb.selected_inferior()

    def read(self, t, address):
        return struct.unpack(DeviceMemory.ENDIANITY + t[T.FORMAT_CHAR],
                             self.inferior.read_memory(address, t[T.LENGTH]))[0]

    def write(self, t, address, value):
        value_bytes = struct.pack(DeviceMemory.ENDIANITY + t[T.FORMAT_CHAR], value)
        self.inferior.write_memory(address, value_bytes)


class MMPeripheral(object):
    """Memory Mapped MCU Peripheral"""

    TYPE = 0
    OFFSET = 1

    compiled_fields = {}

    def __init__(self, address, memory):
        self.memory = memory
        self.address = address
        offset = 0
        for t, name in self.fields:
            if name is not None:
                self.compiled_fields[name] = (t, offset)
            offset += t[T.LENGTH]

    def __getattr__(self, name):
        if name in self.compiled_fields:
            return self.memory.read(self.compiled_fields[name][MMPeripheral.TYPE],
                                    (self.address +
                                     self.compiled_fields[name][MMPeripheral.OFFSET]))
        else:
            raise ValueError('This peripheral does not contain register ' + name)

    def __setattr__(self, name, value):
        if name in self.compiled_fields:
            self.memory.write(self.compiled_fields[name][MMPeripheral.TYPE],
                              self.address + self.compiled_fields[name][MMPeripheral.OFFSET],
                              value)
        else:
            super(MMPeripheral, self).__setattr__(name, value)
