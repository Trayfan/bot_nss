import pyautogui

def get_mouse_position(prompt):
    input(f"{prompt}\nНажмите Enter, чтобы сохранить текущие координаты мыши...")
    x, y = pyautogui.position()
    print(f"Координаты сохранены: ({x}, {y})")
    return x, y

def main():
    coordinates = {}

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

    # Вы можете добавить другие координаты по мере необходимости

    # Сохранение координат в файл
    with open("coordinates.txt", "w") as f:
        for key, value in coordinates.items():
            f.write(f"{key}: {value[0]}, {value[1]}\n")

    print("Все координаты сохранены в файл coordinates.txt.")

if __name__ == "__main__":
    main()
