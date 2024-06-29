import pyautogui
from PIL import ImageGrab

def get_mouse_position_and_color(prompt):
    input(f"{prompt}\nНажмите Enter, чтобы сохранить текущие координаты мыши...")
    x, y = pyautogui.position()
    print(f"Координаты сохранены: ({x}, {y})")
    
    screenshot = ImageGrab.grab()
    color = screenshot.getpixel((x, y))
    print(f"Цвет пикселя сохранен: {color}")
    
    return (x, y), color

def main():
    coordinates = {}
    colors = {}

    print("Этот скрипт поможет вам настроить координаты для бота.")

    coordinates['inventory_button'], _ = get_mouse_position_and_color(
        "Пожалуйста, наведите курсор на кнопку открытия инвентаря."
    )

    coordinates['slot_1'], _ = get_mouse_position_and_color(
        "Пожалуйста, наведите курсор на первую ячейку инвентаря."
    )

    coordinates['slot_2'], _ = get_mouse_position_and_color(
        "Пожалуйста, наведите курсор на вторую ячейку инвентаря."
    )

    coordinates['white_icon'], colors['white_icon'] = get_mouse_position_and_color(
        "Пожалуйста, наведите курсор на белый значок в инвентаре."
    )

    # Сохранение координат и цветов в файл
    with open("coordinates.txt", "w") as f:
        for key, value in coordinates.items():
            f.write(f"{key}: {value[0]}, {value[1]}\n")
        for key, value in colors.items():
            f.write(f"{key}_color: {value[0]}, {value[1]}, {value[2]}\n")

    print("Все координаты и цвета сохранены в файл coordinates.txt.")

if __name__ == "__main__":
    main()
