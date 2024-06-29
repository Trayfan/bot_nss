from movement_manager import MovementManager
from memory_manager import MemoryManager
from utils import wait_for_game_window

def main():
    wait_for_game_window("Pirates Online")  # Ожидание активного окна игры
    process_name = "Game.exe"
    memory_manager = MemoryManager(process_name)
    movement_manager = MovementManager(memory_manager)
    
    # Тестирование перемещения к координатам (пример координат 1234, 5678)
    movement_manager.move_to_coordinates_water(843,3702)
    movement_manager.move_to_coordinates_water(846,3740)
    movement_manager.move_to_coordinates_water(877,3758)
if __name__ == "__main__":
    main()
