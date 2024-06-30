from movement_manager import MovementManager
from memory_manager import MemoryManager
from utils import wait_for_game_window

def main():
    wait_for_game_window("Pirates Online")  # Ожидание активного окна игры
    process_name = "Game.exe"
    memory_manager = MemoryManager(process_name)
    movement_manager = MovementManager(memory_manager)
    
    # Тестирование перемещения по воде к координатам (пример координат 1234, 5678) с радиусом 5
    route = [(842,3699), (846,3731), (877,3751)]  # Пример маршрута из нескольких точек
    movement_manager.follow_route(route, tolerance=2)
    
if __name__ == "__main__":
    main()
