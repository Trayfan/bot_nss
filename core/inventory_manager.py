import pyautogui
import time
from core.memory_manager import MemoryManager
from core.utils import load_coordinates, wait_for_game_window, click_with_delay

class InventoryManager:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.coordinates, self.colors = load_coordinates()

    def open_inventory(self):
        wait_for_game_window("Pirates Online")  # Ожидание активного окна игры

        inventory_button_coordinates = self.coordinates['inventory_button']
        max_attempts = 5
        attempt = 0
        inventory_opened = False

        while attempt < max_attempts and not inventory_opened:
            x, y = inventory_button_coordinates
            click_with_delay(x, y, button='right')
            time.sleep(1)  # Ожидание открытия инвентаря

            # Проверка открытия инвентаря
            inventory_opened = self.is_inventory_open()

            attempt += 1

        if not inventory_opened:
            print("Ошибка: не удалось открыть инвентарь после нескольких попыток")
        else:
            print("Инвентарь успешно открыт")

    def is_inventory_open(self):
        icon_coordinates = self.coordinates['white_icon']
        expected_color = self.colors['white_icon']
        screenshot = pyautogui.screenshot(region=(icon_coordinates[0], icon_coordinates[1], 1, 1))
        actual_color = screenshot.getpixel((0, 0))
        return actual_color == expected_color

    def check_item(self, slot):
        slot_coordinates = self.coordinates[slot]
        x, y = slot_coordinates
        screenshot = pyautogui.screenshot(region=(x, y, 32, 32))
        return screenshot  # Вернуть скриншот для дальнейшего анализа

    def use_item(self, slot):
        slot_coordinates = self.coordinates[slot]
        x, y = slot_coordinates
        click_with_delay(x, y, button='left')
        time.sleep(0.5)  # Ожидание использования предмета

if __name__ == "__main__":
    process_name = "Game.exe"  # Изменено на правильное имя процесса
    memory_manager = MemoryManager(process_name)
    inventory_manager = InventoryManager(memory_manager)
    
    # Тестирование открытия инвентаря
    inventory_manager.open_inventory()
