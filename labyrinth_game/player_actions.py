from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import random_event


def _has_treasure_key(inv: list[str]) -> bool:
    """Проверяет, есть ли у игрока ключ для входа в treasure_room."""
    keys = {"treasure key", "rusty key"}
    return any(k in inv for k in keys)


def move_player(game_state: dict, direction: str) -> None:
    """
    Перемещает игрока в указанном направлении, если есть выход.
    Проверяет наличие ключа при попытке войти в treasure_room.
    После успешного перемещения вызывает событие random_event().
    """
    current = game_state["current_room"]
    direction = direction.lower()
    exits = ROOMS[current]["exits"]

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = exits[direction]

    if next_room == "treasure_room":
        if _has_treasure_key(game_state.get("player_inventory", [])):
            print(
                "Вы используете найденный ключ, чтобы открыть путь "
                "в комнату сокровищ."
            )
        else:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return

    game_state["current_room"] = next_room
    game_state["steps_taken"] += 1

    new_room = ROOMS[next_room]
    print(new_room.get("description", ""))
    if new_room.get("items"):
        print("Заметные предметы:", ", ".join(new_room["items"]))
    if new_room.get("exits"):
        print("Выходы:", ", ".join(new_room["exits"].keys()))
    if new_room.get("puzzle"):
        print("Кажется, здесь есть загадка (используйте команду solve).")

    random_event(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    """
    Поднимает предмет из текущей комнаты и добавляет его в инвентарь.
    Исключение: treasure chest нельзя взять.
    """
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
    """
    Использует предмет из инвентаря игрока.
    torch → светлее,
    sword → уверенность,
    bronze box → добавляет rusty key,
    иначе → выводит сообщение о неизвестном действии.
    """
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
    """Выводит содержимое инвентаря игрока или сообщение, если он пуст."""
    inv = game_state.get("player_inventory", [])
    if inv:
        print("Инвентарь:", ", ".join(inv))
    else:
        print("Инвентарь пуст.")


def get_input(prompt: str = "> ") -> str:
    """
    Запрашивает ввод пользователя.
    Обрабатывает прерывание (Ctrl+C / Ctrl+D) как выход из игры.
    """
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"