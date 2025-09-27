from labyrinth_game.constants import ROOMS


def get_input(prompt: str = "> ") -> str:
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def describe_current_room(game_state: dict) -> None:
    room_key = game_state["current_room"]
    room = ROOMS[room_key]

    print(f"== {room_key.upper()} ==")
    print(room.get("description", ""))

    items = room.get("items", [])
    if items:
        print("Заметные предметы:", ", ".join(items))

    exits = room.get("exits", {})
    if exits:
        print("Выходы:", ", ".join(exits.keys()))

    if room.get("puzzle"):
        print("Кажется, здесь есть загадка (используйте команду solve).")


def show_help() -> None:
    print("\nДоступные команды:")
    print("  go <direction>  - перейти (north/south/east/west/up/down)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")


def solve_puzzle(game_state: dict) -> None:
    """Задать вопрос, принять ответ, проверить и выдать награду при успехе."""
    room_key = game_state["current_room"]
    room = ROOMS[room_key]
    puzzle = room.get("puzzle")

    if not puzzle:
        print("Загадок здесь нет.")
        return

    question, correct_answer = puzzle
    print("Загадка:", question)
    user_answer = get_input("Ваш ответ: ")

    if str(user_answer).strip().lower() == str(correct_answer).strip().lower():
        print("Верно! Загадка решена.")
        room["puzzle"] = None

        reward_by_room = {
            # пример награды за библиотеку
            "library": "treasure key",
        }
        reward = reward_by_room.get(room_key)
        if reward and reward not in game_state["player_inventory"]:
            game_state["player_inventory"].append(reward)
            print(f"Вы получили награду: {reward}")
        else:
            if reward is None:
                print("Вы чувствуете, как что-то изменилось в лабиринте...")
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state: dict) -> None:
    """
    Открыть 'treasure chest' ключом или кодом.
    Если сундук в инвентаре — вернуть его в комнату и продолжить.
    """
    room_key = game_state["current_room"]
    room = ROOMS[room_key]
    items = room.get("items", [])
    inv = game_state.get("player_inventory", [])

    chest_in_room = "treasure chest" in items
    chest_in_inv = "treasure chest" in inv

    if not chest_in_room and chest_in_inv:
        print("Вы ставите сундук обратно на стол.")
        inv.remove("treasure chest")
        items.append("treasure chest")
        chest_in_room = True

    if not chest_in_room:
        print("Сундук уже открыт или отсутствует.")
        return

    has_key = any(
        k in inv for k in ("treasure key", "treasure_key", "rusty key", "rusty_key")
    )

    if has_key:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        if "treasure chest" in items:
            items.remove("treasure chest")
        if "treasure chest" in inv:
            inv.remove("treasure chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    print("Сундук заперт. Похоже, его можно открыть кодом.")
    consent = get_input("Ввести код? (да/нет): ").strip().lower()
    if consent != "да":
        print("Вы отступаете от сундука.")
        return

    puzzle = room.get("puzzle")
    if not puzzle:
        print("Код неизвестен. Здесь нет подсказки.")
        return

    _, correct_code = puzzle
    code = get_input("Введите код: ").strip()
    if code.lower() == str(correct_code).strip().lower():
        print("Замок щёлкнул! Сундук открыт.")
        if "treasure chest" in items:
            items.remove("treasure chest")
        if "treasure chest" in inv:
            inv.remove("treasure chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Код неверный.")