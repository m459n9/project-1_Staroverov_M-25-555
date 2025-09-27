from labyrinth_game.constants import ROOMS


def move_player(game_state: dict, direction: str) -> None:
    current = game_state["current_room"]
    exits = ROOMS[current]["exits"]
    if direction in exits:
        game_state["current_room"] = exits[direction]
        game_state["steps_taken"] += 1
        new_room = ROOMS[game_state["current_room"]]
        print(new_room.get("description", ""))
        if new_room.get("items"):
            print("Заметные предметы:", ", ".join(new_room["items"]))
        if new_room.get("exits"):
            print("Выходы:", ", ".join(new_room["exits"].keys()))
        if new_room.get("puzzle"):
            print("Кажется, здесь есть загадка (используйте команду solve).")
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state: dict, item_name: str) -> None:
    room = ROOMS[game_state["current_room"]]
    if item_name.lower() == "treasure chest":
        print("Сундук слишком тяжёлый, его нельзя взять.")
        return
    if item_name in room["items"]:
        room["items"].remove(item_name)
        game_state["player_inventory"].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state: dict, item_name: str) -> None:
    if item_name not in game_state["player_inventory"]:
        print("У вас нет такого предмета.")
        return
    if item_name == "torch":
        print("Вы зажгли факел. Стало светлее.")
    elif item_name == "sword":
        print("Вы держите меч. Чувствуете себя увереннее.")
    elif item_name == "bronze box":
        if "rusty key" not in game_state["player_inventory"]:
            game_state["player_inventory"].append("rusty key")
            print(
                "Вы открыли бронзовую шкатулку и нашли внутри ржавый ключ!"
            )
        else:
            print("Шкатулка пуста.")
    else:
        print("Вы не знаете, как использовать этот предмет.")


def show_inventory(game_state: dict) -> None:
    inv = game_state.get("player_inventory", [])
    if inv:
        print("Инвентарь:", ", ".join(inv))
    else:
        print("Инвентарь пуст.")


def get_input(prompt: str = "> ") -> str:
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"