import pyautogui
import time
from PIL import ImageGrab

def get_cursor_info():
    while True:
        x, y = pyautogui.position()
        screenshot = ImageGrab.grab()
        color = screenshot.getpixel((x, y))
        print(f"Координаты: ({x}, {y}), Цвет: {color}")
        time.sleep(1)

if __name__ == "__main__":
    print("Для остановки скрипта нажмите Ctrl+C")
    get_cursor_info()
