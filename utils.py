def input_int(prompt: str) -> int:
    while True:
        raw_value = input(prompt)
        try:
            return int(raw_value)
        except ValueError:
            print("Введите целое число.")


def input_nonempty(prompt: str) -> str:
    while True:
        raw_value = input(prompt).strip()
        if raw_value:
            return raw_value
        print("Значение не может быть пустым.")


def input_theme_list(prompt: str) -> list[str]:
    raw_value = input(prompt)

    return [name.strip() for name in raw_value.split(",") if name.strip()]
