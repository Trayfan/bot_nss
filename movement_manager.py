import pyautogui
import time
from math import cos, sin
from memory_manager import MemoryManager
from utils import load_coordinates, wait_for_game_window, click_with_delay

class MovementManager:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.coordinates, self.colors = load_coordinates()
        self.camera_angle = 330  # начальный угол камеры (0 - по умолчанию)

    def set_camera_angle(self, angle):
        self.camera_angle = angle

    def get_valid_coordinates(self):
        x_offsets_land = [0x004F24C8, 0x90, 0x6A0, 0x44]
        y_offsets_land = [0x004F24C8, 0x90, 0x6A0, 0x48]
        x_offsets_water = [0x004F24C8, 0xC8, 0xF98, 0x3B0, 0x30, 0x40]
        y_offsets_water = [0x004F24C8, 0xC8, 0xF98, 0x3B0, 0x30, 0x44]

        x_land = self.memory_manager.read_memory(self.memory_manager.base_address, x_offsets_land)
        y_land = self.memory_manager.read_memory(self.memory_manager.base_address, y_offsets_land)
        x_water = self.memory_manager.read_memory(self.memory_manager.base_address, x_offsets_water)
        y_water = self.memory_manager.read_memory(self.memory_manager.base_address, y_offsets_water)

        print(f"x_land: {x_land}, y_land: {y_land}, x_water: {x_water}, y_water: {y_water}")

        if 100 <= x_land <= 4000 and 100 <= y_land <= 4000:
            return x_land, y_land
        elif 100 <= x_water <= 4000 and 100 <= y_water <= 4000:
            return x_water, y_water
        else:
            return None, None

    def calculate_click_position(self, step_x, step_y):
        angle_rad = self.camera_angle * (3.14159265 / 180)  # перевод градусов в радианы
        rotated_x = step_x * cos(angle_rad) - step_y * sin(angle_rad)
        rotated_y = step_x * sin(angle_rad) + step_y * cos(angle_rad)
        return int(rotated_x), int(rotated_y)

    def move_to_coordinates_land(self, target_x, target_y, tolerance=5):
        wait_for_game_window("Pirates Online")

        radar_button_coordinates = self.coordinates['radar_button']
        x_input_coordinates = self.coordinates['x_input']
        y_input_coordinates = self.coordinates['y_input']
        confirm_button_coordinates = self.coordinates['confirm_button']

        max_attempts = 5
        attempt = 0
        radar_opened = False

        while attempt < max_attempts and not radar_opened:
            click_with_delay(*radar_button_coordinates, button='left')
            time.sleep(1)

            radar_opened = self.is_radar_open(self.coordinates['radar_open'])
            attempt += 1

        if not radar_opened:
            print("Ошибка: не удалось открыть радар после нескольких попыток")
            return

        click_with_delay(*x_input_coordinates, button='left')
        pyautogui.typewrite(str(target_x), interval=0.1)
        click_with_delay(*y_input_coordinates, button='left')
        pyautogui.typewrite(str(target_y), interval=0.1)
        click_with_delay(*confirm_button_coordinates, button='left')

        while True:
            current_x, current_y = self.get_valid_coordinates()
            if current_x is None or current_y is None:
                print("Ошибка получения координат персонажа")
                break
            if abs(current_x - target_x) <= tolerance and abs(current_y - target_y) <= tolerance:
                print(f"Персонаж достиг координат ({target_x}, {target_y}) с допустимым отклонением {tolerance}")
                break
            time.sleep(1)

    def move_to_coordinates_water(self, target_x, target_y, step_size=500, tolerance=5, exit_coordinates=None):
        wait_for_game_window("Pirates Online")

        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2

        while True:
            current_x, current_y = self.get_valid_coordinates()
            if current_x is None or current_y is None:
                print("Ошибка получения координат персонажа")
                break
            distance_x = target_x - current_x
            distance_y = target_y - current_y

            if exit_coordinates and (abs(current_x - exit_coordinates[0]) <= 10 and abs(current_y - exit_coordinates[1]) <= 10):
                print("Персонаж переместился в новую локацию")
                click_with_delay(center_x, center_y, button='left')  # Остановить движение после телепортации
                break

            if abs(distance_x) <= tolerance and abs(distance_y) <= tolerance:
                print(f"Персонаж достиг координат ({target_x}, {target_y}) с допустимым отклонением {tolerance}")
                click_with_delay(center_x, center_y, button='left')
                break

            total_distance = (distance_x**2 + distance_y**2)**0.5
            step_ratio = step_size / total_distance

            step_x = int(step_ratio * distance_x)
            step_y = int(step_ratio * distance_y)

            rotated_x, rotated_y = self.calculate_click_position(step_x, step_y)
            new_x = center_x + rotated_x
            new_y = center_y + rotated_y

            pyautogui.moveTo(new_x, new_y)
            click_with_delay(new_x, new_y, button='left')

            time.sleep(0.3)

    def follow_route(self, route, tolerance=5):
        for waypoint in route:
            self.move_to_coordinates_water(waypoint[0], waypoint[1], tolerance=tolerance)
            time.sleep(1)  # Задержка перед переходом к следующей точке

    def enter_portal(self, portal_x, portal_y, target_x, target_y, step_size=150, tolerance=0):
        exit_coordinates = (target_x, target_y)
        self.move_to_coordinates_water(portal_x, portal_y, step_size=step_size, tolerance=tolerance, exit_coordinates=exit_coordinates)
        while True:
            current_x, current_y = self.get_valid_coordinates()
            if current_x is None or current_y is None:
                print("Ошибка получения координат персонажа")
                break
            if abs(current_x - target_x) <= 10 and abs(current_y - target_y) <= 10:
                print("Персонаж вошел в портал и переместился на сушу")
                click_with_delay(pyautogui.size()[0] // 2, pyautogui.size()[1] // 2, button='left')  # Остановить движение после телепортации
                break
            time.sleep(1)

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

    movement_manager.set_camera_angle(330)  # Установить угол камеры (пример)

    # Тестирование перемещения по суше к координ
