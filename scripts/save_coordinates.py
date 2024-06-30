import pyautogui
from PIL import ImageGrab

def get_mouse_position_and_color(prompt):
    input(f"{prompt}\nНажмите Enter, чтобы сохранить текущие координаты мыши и цвет...")
    x, y = pyautogui.position()
    screenshot = ImageGrab.grab()
    color = screenshot.getpixel((x, y))
    print(f"Координаты сохранены: ({x}, {y}) и цвет: {color}")
    return (x, y), color

def get_mouse_position(prompt):
    input(f"{prompt}\nНажмите Enter, чтобы сохранить текущие координаты мыши...")
    x, y = pyautogui.position()
    print(f"Координаты сохранены: ({x}, {y})")
    return x, y

def main():
    coordinates = {}
    colors = {}

    print("Этот скрипт поможет вам настроить координаты для бота.")

    coordinates['inventory_button'] = get_mouse_position(
        "Пожалуйста, наведите курсор на кнопку открытия инвентаря."
    )

    coordinates['slot_1'] = get_mouse_position(
        "Пожалуйста, наведите курсор на первую ячейку инвентаря."
    )

    coordinates['slot_2'] = get_mouse_position(
        "Пожалуйста, наведите курсор на вторую ячейку инвентаря."
    )

    coordinates['white_icon'], colors['white_icon'] = get_mouse_position_and_color(
        "Пожалуйста, наведите курсор на белый значок в инвентаре."
    )

    coordinates['radar_button'] = get_mouse_position(
        "Пожалуйста, наведите курсор на кнопку радара."
    )

    coordinates['radar_open'], colors['radar_open'] = get_mouse_position_and_color(
        "Пожалуйста, наведите курсор на элемент, указывающий на открытие радара."
    )

    coordinates['x_input'] = get_mouse_position(
        "Пожалуйста, наведите курсор на поле ввода координаты X."
    )

    coordinates['y_input'] = get_mouse_position(
        "Пожалуйста, наведите курсор на поле ввода координаты Y."
    )

    coordinates['confirm_button'] = get_mouse_position(
        "Пожалуйста, наведите курсор на кнопку подтверждения."
    )

    # Сохранение координат и цветов в файл
    with open("coordinates.txt", "w") as f:
        for key, value in coordinates.items():
            f.write(f"{key}: {value[0]}, {value[1]}\n")

        for key, value in colors.items():
            if isinstance(value, tuple):
                f.write(f"{key}_color: {value[0]}, {value[1]}, {value[2]}\n")

    print("Все координаты и цвета сохранены в файл coordinates.txt.")

if __name__ == "__main__":
    main()
