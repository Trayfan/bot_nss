import pygetwindow as gw
import time
import pyautogui

def load_coordinates(file_path='coordinates.txt'):
    coordinates = {}
    colors = {}
    with open(file_path, 'r') as f:
        for line in f:
            if '_color' in line:
                key, value = line.strip().split(': ')
                colors[key.replace('_color', '')] = tuple(map(int, value.split(', ')))
            else:
                key, value = line.strip().split(': ')
                coordinates[key] = tuple(map(int, value.split(', ')))
    return coordinates, colors

def wait_for_game_window(window_title="Pirates Online"):
    print("Ожидание, пока окно игры не станет активным...")
    while True:
        active_window = gw.getActiveWindow()
        if active_window and window_title in active_window.title:
            print("Окно игры активно!")
            break
        time.sleep(1)

def click_with_delay(x, y, button='left', delay=0.1):
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown(button=button)
    time.sleep(delay)
    pyautogui.mouseUp(button=button)
