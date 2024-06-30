import psutil
import ctypes

class MemoryManager:
    def __init__(self, process_name):
        self.process_name = process_name
        self.process = self.get_process_by_name(process_name)
        self.process_handle = self.open_process(self.process.pid)
        self.base_address = self.get_base_address()

    def get_process_by_name(self, process_name):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                return proc
        raise Exception(f"Process '{process_name}' not found")

    def open_process(self, pid):
        PROCESS_ALL_ACCESS = 0x1F0FFF
        return ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

    def get_base_address(self):
        for module in self.process.memory_maps(grouped=False):
            if self.process_name in module.path:
                return int(module.addr.split('-')[0], 16)
        raise Exception(f"Base address for '{self.process_name}' not found")

    def read_memory(self, address, value_type=ctypes.c_float):
        value = value_type()
        bytesRead = ctypes.c_ulonglong()
        result = ctypes.windll.kernel32.ReadProcessMemory(self.process_handle, ctypes.c_void_p(address), ctypes.byref(value), ctypes.sizeof(value), ctypes.byref(bytesRead))
        if not result:
            print(f"Failed to read memory at address {hex(address)}")
            return None
        return value.value

    def read_coordinates(self, base_address, offsets):
        address = base_address
        for offset in offsets[:-1]:
            address = self.read_memory(address + offset, ctypes.c_ulonglong)
            if address is None:
                return None
            address = int(address)
        final_address = address + offsets[-1]
        return self.read_memory(final_address, ctypes.c_float)

# Пример использования
if __name__ == "__main__":
    process_name = "Game.exe"
    memory_manager = MemoryManager(process_name)
    base_address = memory_manager.get_base_address()
    print(f"Base address: {hex(base_address)}")
