from dataclasses import dataclass

@dataclass
class Theme:
    name: str
    is_completed: bool = False

def mark_as_completed(theme: Theme) -> None:
    theme.is_completed = True

def main():
    course_name = "Разработка на Python"
    themes = [
        Theme("Переменные"),
        Theme("Условные операторы"),
        Theme("Циклы"),
        Theme("Функции"),
        Theme("Списки и словари")
    ]
    themes_amount = len(themes)

    print(f"Курс: {course_name}")
    print(f"Всего тем: {themes_amount}")
    print("Темы до отметок:")
    for t in themes:
        print(f"  - {t.name}: {'пройдено' if t.is_completed else 'не пройдено'}")

    mark_as_completed(themes[0])

    print("\nПосле отметки первой темы:")
    for t in themes:
        print(f"  - {t.name}: {'пройдено' if t.is_completed else 'не пройдено'}")

if __name__ == "__main__":
    main()