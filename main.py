from dataclasses import dataclass, field


@dataclass
class Theme:
    name: str
    is_completed: bool = False


@dataclass
class Course:
    name: str
    themes: list[Theme] = field(default_factory=list)


def mark_as_completed(theme: Theme) -> None:
    theme.is_completed = True


def add_course(courses: list[Course], name: str, theme_names: list[str]) -> Course:
    course = Course(
        name=name,
        themes=[Theme(theme_name) for theme_name in theme_names]
    )
    courses.append(course)
    
    return course


def view_theme(course: Course, theme_name: str) -> None:
    for theme in course.themes:
        if theme.name == theme_name:
            status = "пройдена" if theme.is_completed else "не пройдена"
            print(f"Курс: {course.name}")
            print(f"Тема: {theme.name}")
            print(f"Статус: {status}")

            return

    print(f"Тема '{theme_name}' не найдена в курсе '{course.name}'")


def mark_theme_completed(course: Course, theme_name: str) -> None:
    for theme in course.themes:
        if theme.name == theme_name:
            mark_as_completed(theme)
            print(f"Тема '{theme.name}' отмечена как пройденная.")

            return

    print(f"Тема '{theme_name}' не найдена в курсе '{course.name}'")


def view_progress(course: Course) -> None:
    total = len(course.themes)
    completed = sum(theme.is_completed for theme in course.themes)
    percent = completed / total * 100 if total else 0

    print(f"Прогресс по курсу '{course.name}': {completed}/{total} ({percent:.0f}%)")


def main():
    courses: list[Course] = []

    course = add_course(
        courses,
        "Разработка на Python",
        [
            "Переменные",
            "Условные операторы",
            "Циклы",
            "Функции",
            "Списки и словари"
        ]
    )

    view_theme(course, "Циклы")
    mark_theme_completed(course, "Переменные")
    view_theme(course, "Переменные")
    view_progress(course)


if __name__ == "__main__":
    main()