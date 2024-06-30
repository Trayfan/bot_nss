import pymem
import ctypes

class MemoryManager:
    def __init__(self, process_name):
        self.process_name = process_name
        self.process = pymem.Pymem(process_name)
        self.base_address = self.get_base_address()

    def get_base_address(self):
        module = pymem.process.module_from_name(self.process.process_handle, self.process_name)
        print(f"Base address of {self.process_name}: {hex(module.lpBaseOfDll)}")
        return module.lpBaseOfDll

    def read_memory(self, base_address, offsets):
        address = base_address
        for offset in offsets[:-1]:
            address = self.read_int(address + offset)
        return self.read_float(address + offsets[-1])

    def read_int(self, address):
        value = ctypes.c_int()
        bytesRead = ctypes.c_size_t()
        if not ctypes.windll.kernel32.ReadProcessMemory(self.process.process_handle, ctypes.c_void_p(address), ctypes.byref(value), ctypes.sizeof(value), ctypes.byref(bytesRead)):
            print(f"Failed to read int memory at address {address}")
        return value.value

    def read_float(self, address):
        value = ctypes.c_float()
        bytesRead = ctypes.c_size_t()
        if not ctypes.windll.kernel32.ReadProcessMemory(self.process.process_handle, ctypes.c_void_p(address), ctypes.byref(value), ctypes.sizeof(value), ctypes.byref(bytesRead)):
            print(f"Failed to read float memory at address {address}")
        return value.value
