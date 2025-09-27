#!/usr/bin/env python3
from labyrinth_game import player_actions as actions
from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    get_input,
    show_help,
)


def process_command(game_state: dict, command: str) -> None:
    parts = command.strip().split(maxsplit=1)
    if not parts:
        return

    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    match cmd:
        case "look":
            describe_current_room(game_state)
        case "go":
            actions.move_player(game_state, arg)
        case "take":
            actions.take_item(game_state, arg)
        case "use":
            if arg.strip().lower() == "treasure chest":
                attempt_open_treasure(game_state)
            else:
                actions.use_item(game_state, arg)
        case "inventory":
            actions.show_inventory(game_state)
        case "solve":
            # Пытаемся решить загадку; логика победы — в utils.attempt_open_treasure
            from labyrinth_game.utils import solve_puzzle

            solve_puzzle(game_state)
            room = ROOMS[game_state["current_room"]]
            if (
                not game_state["game_over"]
                and "treasure chest" in room.get("items", [])
            ):
                attempt_open_treasure(game_state)
        case "help" | "?":
            show_help()
        case "quit" | "exit":
            print("Игра завершена. До встречи!")
            game_state["game_over"] = True
        case _:
            print(
                "Неизвестная команда. Доступные: look, go <dir>, take <item>, "
                "use <item>, inventory, solve, help, quit"
            )


def main() -> None:
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    show_help()
    describe_current_room(game_state)

    while not game_state["game_over"]:
        cmd = get_input("> ")
        process_command(game_state, cmd)


if __name__ == "__main__":
    main()