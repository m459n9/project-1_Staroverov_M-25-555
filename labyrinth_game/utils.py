import math

from labyrinth_game.constants import ROOMS


def pseudo_random(seed: int, modulo: int) -> int:
    """Возвращает детерминированное псевдослучайное целое в диапазоне [0, modulo)."""
    if modulo <= 0:
        return 0
    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(frac * modulo)


def trigger_trap(game_state: dict) -> None:
    """Срабатывает ловушка: теряем предмет из инвентаря или получаем урон/поражение."""
    print("Ловушка активирована! Пол стал дрожать...")

    inv = game_state.get("player_inventory", [])
    seed = game_state.get("steps_taken", 0)

    if inv:
        idx = pseudo_random(seed, len(inv))
        lost = inv.pop(idx)
        print(f"Вы потеряли предмет: {lost}")
        return

    roll = pseudo_random(seed, 10)
    if roll < 3:
        print("Вы получили урон и потеряли сознание. Поражение.")
        game_state["game_over"] = True
    else:
        print("Вы едва уцелели и продолжаете путь.")


def random_event(game_state: dict) -> None:
    """С небольшой вероятностью запускает одно из случайных событий при перемещении."""
    seed = game_state.get("steps_taken", 0)
    room_key = game_state.get("current_room", "entrance")
    room = ROOMS.get(room_key, {})

    # редкость события: ~1 из 10
    if pseudo_random(seed, 10) != 0:
        return

    choice = pseudo_random(seed + 1, 3)

    if choice == 0:
        print("На полу блеснула монетка.")
        room.setdefault("items", []).append("coin")
    elif choice == 1:
        print("Вы слышите шорох где-то рядом...")
        if "sword" in game_state.get("player_inventory", []):
            print("Вы выставляете меч — существо отступает.")
    else:
        if room_key == "trap_room" and "torch" not in game_state.get(
            "player_inventory", []
        ):
            print("Опасно! В темноте может быть ловушка.")
            trigger_trap(game_state)


def get_input(prompt: str = "> ") -> str:
    """Запрашивает ввод. Ctrl+C/Ctrl+D — выход (возвращает 'quit')."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def describe_current_room(game_state: dict) -> None:
    """Печатает заголовок, описание, предметы, выходы и пометку о загадке."""
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


def show_help(commands: dict) -> None:
    """Выводит список доступных команд с краткими описаниями."""
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<16} - {desc}")


def solve_puzzle(game_state: dict) -> None:
    """Показывает загадку, проверяет ответ (с альтернативами), выдаёт награду."""
    room_key = game_state["current_room"]
    room = ROOMS[room_key]
    puzzle = room.get("puzzle")

    if not puzzle:
        print("Загадок здесь нет.")
        return

    question, correct_answer = puzzle
    print("Загадка:", question)
    user_answer = get_input("Ваш ответ: ").strip().lower()

    alt_map = {
        "10": {"10", "десять"},
        "6": {"6", "шесть"},
        "дождь": {"дождь", "дожди"},
        "париж": {"париж"},
        "урок": {"урок"},
        "равны": {"равны", "одинаковы"},
    }

    correct_key = str(correct_answer).strip().lower()
    valid_answers = alt_map.get(correct_key, {correct_key})

    if user_answer in valid_answers:
        print("Верно! Загадка решена.")
        room["puzzle"] = None

        reward_by_room = {
            "hall": "treasure key",
            "library": "rusty key",
        }
        reward = reward_by_room.get(room_key)
        if reward and reward not in game_state["player_inventory"]:
            game_state["player_inventory"].append(reward)
            print(f"Вы получили награду: {reward}")
    else:
        print("Неверно. Попробуйте снова.")
        if room_key == "trap_room":
            print("Кажется, сработала ловушка за неверный ответ!")
            trigger_trap(game_state)


def attempt_open_treasure(game_state: dict) -> None:
    """Открывает сундук ключом или кодом. Успех — победа в игре."""
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
        k in inv for k in ("treasure key", "rusty key")
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