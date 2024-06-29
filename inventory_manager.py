import pyautogui
import time
from memory_manager import MemoryManager
from utils import load_coordinates

class InventoryManager:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.coordinates = load_coordinates()

    def open_inventory(self):
        # Нажатие на координаты кнопки открытия инвентаря
        inventory_button_coordinates = self.coordinates['inventory_button']
        pyautogui.click(inventory_button_coordinates)
        time.sleep(1)  # Ожидание открытия инвентаря

    def check_item(self, slot):
        slot_coordinates = self.coordinates[slot]
        x, y = slot_coordinates
        screenshot = pyautogui.screenshot(region=(x, y, 32, 32))
        return screenshot  # Вернуть скриншот для дальнейшего анализа

    def use_item(self, slot):
        slot_coordinates = self.coordinates[slot]
        x, y = slot_coordinates
        pyautogui.click(x, y)
        time.sleep(0.5)  # Ожидание использования предмета

if __name__ == "__main__":
    process_name = "PiratesOnline.exe"
    memory_manager = MemoryManager(process_name)
    inventory_manager = InventoryManager(memory_manager)
    
    inventory_manager.open_inventory()
    inventory_manager.check_item('slot_1')
    inventory_manager.use_item('slot_1')
