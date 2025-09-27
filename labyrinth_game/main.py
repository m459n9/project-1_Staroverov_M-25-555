#!/usr/bin/env python3
from labyrinth_game.constants import ROOMS

game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
}
def main():
    print("Добро пожаловать в Лабиринт!")
    print(ROOMS[game_state['current_room']]['description'])

if __name__ == "__main__":
    main()
  