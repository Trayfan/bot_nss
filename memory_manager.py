import pymem
import pymem.process

class MemoryManager:
    def __init__(self, process_name):
        self.pm = pymem.Pymem(process_name)
        self.base_address = pymem.process.module_from_name(self.pm.process_handle, process_name).lpBaseOfDll

    def read_memory(self, address):
        return self.pm.read_int(address)

    def write_memory(self, address, value):
        self.pm.write_int(address, value)
