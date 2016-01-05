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
        value_bytes = struct.pack('I', value)
        self.inferior.write_memory(address, value_bytes)


def create_memory_reg(offset, name):
    def reg_getter(self):
        return self.device_memory.read(self.address + offset)

    def reg_setter(self, value):
        self.device_memory.write(self.address + offset, value)

    return property(reg_getter, reg_setter, None, name)


def create_mem_struct(name, registers):
    structure_fields = {}

    for register, offset in registers:
        structure_fields[register] = create_memory_reg(offset, register)

    def memory_structure_init(self, address, device_memory):
        self.address = address
        self.device_memory = device_memory

    structure_fields['__init__'] = memory_structure_init

    return type(name, (object,), structure_fields)
