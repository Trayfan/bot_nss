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

    def get_current_coordinates(self, offsets):
        return self.memory_manager.read_coordinates(self.memory_manager.base_address, offsets)

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

        x_offsets_land = [0x004F24C8, 0x90, 0x6A0, 0x44]
        y_offsets_land = [0x004F24C8, 0x90, 0x6A0, 0x48]

        self.open_radar(radar_button_coordinates)

        click_with_delay(*x_input_coordinates, button='left')
        pyautogui.typewrite(str(target_x), interval=0.1)
        click_with_delay(*y_input_coordinates, button='left')
        pyautogui.typewrite(str(target_y), interval=0.1)
        click_with_delay(*confirm_button_coordinates, button='left')

        self.wait_until_coordinates_reached(x_offsets_land, y_offsets_land, target_x, target_y, tolerance)

    def move_to_coordinates_water(self, target_x, target_y, step_size=500, tolerance=5):
        wait_for_game_window("Pirates Online")

        x_offsets_water = [0x004F24C8, 0xC8, 0xF98, 0x3B0, 0x30, 0x40]
        y_offsets_water = [0x004F24C8, 0xC8, 0xF98, 0x3B0, 0x30, 0x44]
        x_offsets_land = [0x004F24C8, 0x90, 0x6A0, 0x44]
        y_offsets_land = [0x004F24C8, 0x90, 0x6A0, 0x48]

        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2

        coordinates_history = []
        use_land_offsets = False

        while True:
            if use_land_offsets:
                current_x = self.get_current_coordinates(x_offsets_land)
                current_y = self.get_current_coordinates(y_offsets_land)
            else:
                current_x = self.get_current_coordinates(x_offsets_water)
                current_y = self.get_current_coordinates(y_offsets_water)

            if current_x is None or current_y is None:
                print("Ошибка получения координат персонажа")
                break

            print(f"Current coordinates: {current_x}, {current_y}")

            coordinates_history.append((current_x, current_y))
            if len(coordinates_history) > 10:
                coordinates_history.pop(0)

            if not self.has_coordinates_changed(coordinates_history, (current_x, current_y), threshold=5):
                # Если координаты не меняются, переключаемся на другие оффсеты
                use_land_offsets = not use_land_offsets
                print("Переключение оффсетов")
                continue

            distance_x = target_x - current_x
            distance_y = target_y - current_y

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

    def is_radar_open(self, radar_open_coordinates):
        x, y = radar_open_coordinates
        screenshot = pyautogui.screenshot(region=(x, y, 1, 1))
        expected_color = self.colors['radar_open']
        actual_color = screenshot.getpixel((0, 0))
        return actual_color == expected_color

    def open_radar(self, radar_button_coordinates):
        max_attempts = 5
        attempt = 0
        radar_opened = False

        while attempt < max_attempts and not radar_opened:
            click_with_delay(*radar_button_coordinates, button='left')
            time.sleep(1)

            radar_opened = self.is_radar_open(self.coordinates['radar_open'])
            attempt += 1

        if not radar_opened:
            raise Exception("Ошибка: не удалось открыть радар после нескольких попыток")

    def wait_until_coordinates_reached(self, x_offsets, y_offsets, target_x, target_y, tolerance):
        while True:
            current_x, current_y = self.get_current_coordinates(x_offsets), self.get_current_coordinates(y_offsets)
            if abs(current_x - target_x) <= tolerance and abs(current_y - target_y) <= tolerance:
                print(f"Персонаж достиг координат ({target_x}, {target_y}) с допустимым отклонением {tolerance}")
                break
            time.sleep(1)

    def enter_portal(self, portal_x, portal_y, target_x, target_y, step_size=150, tolerance=2):
        self.move_to_coordinates_water(portal_x, portal_y, step_size=step_size, tolerance=tolerance)
        while True:
            current_x, current_y = self.get_current_coordinates([0x004F24C8, 0x90, 0x6A0, 0x44]), self.get_current_coordinates([0x004F24C8, 0x90, 0x6A0, 0x48])
            if current_x is None or current_y is None:
                print("Ошибка получения координат персонажа")
                break
            if abs(current_x - target_x) <= 10 and abs(current_y - target_y) <= 10:
                print("Персонаж вошел в портал и переместился на сушу")
                click_with_delay(pyautogui.size()[0] // 2, pyautogui.size()[1] // 2, button='left')  # Остановить движение после телепортации
                break
            time.sleep(1)

    def has_coordinates_changed(self, coordinates_history, new_coordinates, threshold=5):
        if len(coordinates_history) < threshold:
            return True
        for coords in coordinates_history[-threshold:]:
            if coords != new_coordinates:
                return True
        return False


