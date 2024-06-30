import pyautogui
import time
from math import cos, sin
from core.utils import load_coordinates, wait_for_game_window, click_with_delay
from config.offsets import X_OFFSETS_WATER, Y_OFFSETS_WATER, X_OFFSETS_LAND, Y_OFFSETS_LAND

class MovementManager:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.coordinates, self.colors = load_coordinates()
        self.camera_angle = 330
        self.stationary_threshold = 3

    def set_camera_angle(self, angle):
        self.camera_angle = angle

    def get_current_coordinates(self, offsets):
        return self.memory_manager.read_coordinates(self.memory_manager.base_address, offsets)

    def calculate_click_position(self, step_x, step_y):
        angle_rad = self.camera_angle * (3.14159265 / 180)
        rotated_x = step_x * cos(angle_rad) - step_y * sin(angle_rad)
        rotated_y = step_x * sin(angle_rad) + step_y * cos(angle_rad)
        return int(rotated_x), int(rotated_y)

    def move_to_coordinates_land(self, target_x, target_y, tolerance=5):
        wait_for_game_window("Pirates Online")
        self.open_radar(self.coordinates['radar_button'])
        self.enter_coordinates(self.coordinates['x_input'], self.coordinates['y_input'], self.coordinates['confirm_button'], target_x, target_y)
        self.wait_until_coordinates_reached(X_OFFSETS_LAND, Y_OFFSETS_LAND, target_x, target_y, tolerance)

    def move_to_coordinates_water(self, target_x, target_y, step_size=500, tolerance=5, target_x2=1, target_y2=1):
        wait_for_game_window("Pirates Online")

        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2

        coordinates_history = []
        use_land_offsets = False

        while True:
            current_x, current_y = self.get_current_position(use_land_offsets)

            if current_x is None or current_y is None:
                print("Ошибка получения координат персонажа")
                break

            coordinates_history.append((current_x, current_y))
            if len(coordinates_history) > 10:
                coordinates_history.pop(0)

            if not self.has_coordinates_changed(coordinates_history, (current_x, current_y), threshold=5):
                use_land_offsets = not use_land_offsets
                print("Переключение оффсетов")
                continue

            if self.reached_target(current_x, current_y, target_x, target_y, tolerance):
                self.stop_character(center_x, center_y)
                break
            
            if self.reached_target(current_x, current_y, target_x2, target_y2, tolerance):
                self.stop_character(center_x, center_y)
                break

            new_x, new_y = self.calculate_new_position(center_x, center_y, current_x, current_y, target_x, target_y, step_size)
            self.move_and_click(new_x, new_y)

    def follow_route(self, route, tolerance=5):
        for waypoint in route:
            self.move_to_coordinates_water(waypoint[0], waypoint[1], tolerance=tolerance)
            time.sleep(1)

    def enter_portal(self, portal_x, portal_y, target_x, target_y, step_size=75, tolerance=3):
        self.move_to_coordinates_water(portal_x, portal_y, step_size=step_size, tolerance=tolerance, target_x2=target_x, target_y2=target_y)

        previous_coordinates = None
        stationary_count = 0

        x_offsets_water = X_OFFSETS_WATER
        y_offsets_water = Y_OFFSETS_WATER
        x_offsets_land = X_OFFSETS_LAND
        y_offsets_land = Y_OFFSETS_LAND

        use_land_offsets = False  # Инициализация переменной use_land_offsets

        while True:
            current_x, current_y = self.get_current_position(use_land_offsets)

            if current_x is None or current_y is None:
                time.sleep(1)
                current_x, current_y = self.get_current_position(use_land_offsets)
                if current_x is None or current_y is None:
                    print("Ошибка получения координат персонажа")
                    break

            if previous_coordinates == (current_x, current_y):
                stationary_count += 1
            else:
                stationary_count = 0

            previous_coordinates = (current_x, current_y)

            if stationary_count >= self.stationary_threshold:
                print("Похоже, что персонаж вошел в портал. Проверка новых координат...")
                time.sleep(2)  # Даем персонажу время переместиться в новую локацию

            if abs(current_x - target_x) <= 10 and abs(current_y - target_y) <= 10:
                print("Персонаж вошел в портал и переместился на новую локацию")
                # self.stop_character()
                time.sleep(1)
                break

            if stationary_count >= self.stationary_threshold:
                use_land_offsets = not use_land_offsets
                print("Переключение оффсетов")

            time.sleep(1)


    def get_screen_center(self):
        screen_width, screen_height = pyautogui.size()
        return screen_width // 2, screen_height // 2

    def update_coordinates_history(self, coordinates_history):
        if len(coordinates_history) > 10:
            coordinates_history.pop(0)
        return coordinates_history

    def reached_target(self, current_x, current_y, target_x, target_y, tolerance):
        return abs(current_x - target_x) <= tolerance and abs(current_y - target_y) <= tolerance

    def get_current_position(self, use_land_offsets):
        x_offsets = X_OFFSETS_LAND if use_land_offsets else X_OFFSETS_WATER
        y_offsets = Y_OFFSETS_LAND if use_land_offsets else Y_OFFSETS_WATER
        current_x = self.get_current_coordinates(x_offsets)
        current_y = self.get_current_coordinates(y_offsets)
        print(current_x, current_y)
        return current_x, current_y

    def move_and_click(self, new_x, new_y):
        pyautogui.moveTo(new_x, new_y)
        click_with_delay(new_x, new_y, button='left')
        time.sleep(0.3)

    def stop_character(self, center_x=None, center_y=None):
        if center_x is None or center_y is None:
            center_x, center_y = self.get_screen_center()
        click_with_delay(center_x, center_y, button='left')

    def has_coordinates_changed(self, coordinates_history, new_coordinates, threshold=5):
        if len(coordinates_history) < threshold:
            return True
        for coords in coordinates_history[-threshold:]:
            if coords != new_coordinates:
                return True
        return False

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

    def enter_coordinates(self, x_input_coordinates, y_input_coordinates, confirm_button_coordinates, target_x, target_y):
        click_with_delay(*x_input_coordinates, button='left')
        pyautogui.typewrite(str(target_x), interval=0.1)
        click_with_delay(*y_input_coordinates, button='left')
        pyautogui.typewrite(str(target_y), interval=0.1)
        click_with_delay(*confirm_button_coordinates, button='left')

    def wait_until_coordinates_reached(self, x_offsets, y_offsets, target_x, target_y, tolerance):
        while True:
            current_x, current_y = self.get_current_coordinates(x_offsets), self.get_current_coordinates(y_offsets)
            if abs(current_x - target_x) <= tolerance and abs(current_y - target_y) <= tolerance:
                print(f"Персонаж достиг координат ({target_x}, {target_y}) с допустимым отклонением {tolerance}")
                break
            time.sleep(1)

    def calculate_new_position(self, center_x, center_y, current_x, current_y, target_x, target_y, step_size):
        distance_x = target_x - current_x
        distance_y = target_y - current_y
        total_distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        step_ratio = step_size / total_distance

        step_x = int(step_ratio * distance_x)
        step_y = int(step_ratio * distance_y)

        rotated_x, rotated_y = self.calculate_click_position(step_x, step_y)
        new_x = center_x + rotated_x
        new_y = center_y + rotated_y
        return new_x, new_y
