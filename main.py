from core.movement_manager import MovementManager
from core.memory_manager import MemoryManager
from core.utils import wait_for_game_window

def main():
    wait_for_game_window("Pirates Online")  # Ожидание активного окна игры
    process_name = "Game.exe"
    memory_manager = MemoryManager(process_name)
    movement_manager = MovementManager(memory_manager)
    

    route = [(842, 3699), (846, 3731), (877, 3751)]  # Пример маршрута из нескольких точек
    movement_manager.follow_route(route, tolerance=2)
    # Координаты портала
    portal_x, portal_y = 877, 3758
    movement_manager.enter_portal(portal_x, portal_y, target_x=734, target_y=1032)

    route = [(711, 1029), (701, 1008), (702, 975), (668, 930), (643, 917)]  # Пример маршрута из нескольких точек (711,990),
    route = [(712, 1024), (713, 991), (674, 953), (670, 930), (643, 917)]  # Пример маршрута из нескольких точек (711,990),
    movement_manager.follow_route(route, tolerance=2)

    portal_to_port_x, portal_to_port_y = 636, 916
    movement_manager.enter_portal(portal_to_port_x, portal_to_port_y, target_x=632, target_y=928)
    
if __name__ == "__main__":
    main()
