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


class MMPeripheral(object):
    """Memory Mapped MCU Peripheral"""

    def __init__(self, address, device_memory):
        self.device_memory = device_memory
        self.address = address

    def __getattr__(self, name):
        if name in self.fields:
            return self.device.read(self.address + self.fields[name])
        else:
            raise ValueError('This peripheral does not contain register ' + name)

    def __setattr__(self, name, value):
        if name in self.fields:
            self.device.write(self.address + self.fields[name], value)
        else:
            super(MMPeripheral, self).__setattr__(name, value)
