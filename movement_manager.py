import pyautogui
import time
from memory_manager import MemoryManager
from utils import load_coordinates, wait_for_game_window, click_with_delay

class MovementManager:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.coordinates, self.colors = load_coordinates()

    def get_current_coordinates(self, offsets):
        base_address = self.memory_manager.base_address
        return self.memory_manager.read_coordinates(base_address, offsets)

    def move_to_coordinates_land(self, target_x, target_y, tolerance=5):
        wait_for_game_window("Pirates Online")  # Ожидание активного окна игры

        radar_button_coordinates = self.coordinates['radar_button']
        radar_open_coordinates = self.coordinates['radar_open']  # Координаты для проверки открытия радара
        x_input_coordinates = self.coordinates['x_input']
        y_input_coordinates = self.coordinates['y_input']
        confirm_button_coordinates = self.coordinates['confirm_button']

        x_offsets_land = [0x004F24C8, 0x90, 0x6A0, 0x44]
        y_offsets_land = [0x004F24C8, 0x90, 0x6A0, 0x48]

        max_attempts = 5
        attempt = 0
        radar_opened = False

        while attempt < max_attempts and not radar_opened:
            click_with_delay(*radar_button_coordinates, button='left')
            time.sleep(1)

            # Проверка открытия радара
            radar_opened = self.is_radar_open(radar_open_coordinates)
            attempt += 1

        if not radar_opened:
            print("Ошибка: не удалось открыть радар после нескольких попыток")
            return

        # Ввод координаты X
        click_with_delay(*x_input_coordinates, button='left')
        pyautogui.typewrite(str(target_x), interval=0.1)

        # Ввод координаты Y
        click_with_delay(*y_input_coordinates, button='left')
        pyautogui.typewrite(str(target_y), interval=0.1)

        # Нажать кнопку Confirm
        click_with_delay(*confirm_button_coordinates, button='left')

        # Ожидание достижения координат с учетом допустимого радиуса отклонения
        while True:
            current_x, current_y = self.get_current_coordinates(x_offsets_land), self.get_current_coordinates(y_offsets_land)
            if abs(current_x - target_x) <= tolerance and abs(current_y - target_y) <= tolerance:
                print(f"Персонаж достиг координат ({target_x}, {target_y}) с допустимым отклонением {tolerance}")
                break
            time.sleep(1)

    def move_to_coordinates_water(self, target_x, target_y, step_size=300, tolerance=1):
        wait_for_game_window("Pirates Online")  # Ожидание активного окна игры

        x_offsets_water = [0x004F24C8, 0xC8, 0xF98, 0x3B0, 0x30, 0x40]
        y_offsets_water = [0x004F24C8, 0xC8, 0xF98, 0x3B0, 0x30, 0x44]

        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2

        while True:
            current_x, current_y = self.get_current_coordinates(x_offsets_water), self.get_current_coordinates(y_offsets_water)
            distance_x = target_x - current_x
            distance_y = target_y - current_y

            if abs(distance_x) <= tolerance and abs(distance_y) <= tolerance:
                print(f"Персонаж достиг координат ({target_x}, {target_y}) с допустимым отклонением {tolerance}")
                break

            if abs(distance_x) > tolerance:
                step_x = step_size if distance_x > 0 else -step_size
            else:
                step_x = 0

            if abs(distance_y) > tolerance:
                step_y = step_size if distance_y > 0 else -step_size
            else:
                step_y = 0

            new_x = center_x + step_x
            new_y = center_y + step_y

            # Убедиться, что курсор находится за пределами персонажа
            if abs(step_x) < 50 and abs(step_y) < 50:
                if step_x > 0:
                    new_x += 50
                else:
                    new_x -= 50
                if step_y > 0:
                    new_y += 50
                else:
                    new_y -= 50

            pyautogui.moveTo(new_x, new_y)
            click_with_delay(new_x, new_y, button='left')

            time.sleep(0.3)  # Уменьшенное ожидание перед следующим шагом для ускорения

    def is_radar_open(self, radar_open_coordinates):
        x, y = radar_open_coordinates
        screenshot = pyautogui.screenshot(region=(x, y, 1, 1))
        expected_color = self.colors['radar_open']
        actual_color = screenshot.getpixel((0, 0))
        return actual_color == expected_color

if __name__ == "__main__":
    process_name = "Game.exe"
    memory_manager = MemoryManager(process_name)
    movement_manager = MovementManager(memory_manager)
    
    # Тестирование перемещения по суше к координатам (пример координат 1234, 5678) с радиусом 5
    movement_manager.move_to_coordinates_land(1234, 5678, tolerance=5)
    
    # Тестирование перемещения по воде к координатам (пример координат 1234, 5678) с радиусом 5
    movement_manager.move_to_coordinates_water(1234, 5678, step_size=300, tolerance=5)
