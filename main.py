from courses import (
    add_course,
    calculate_progress,
    filter_courses_by_progress,
    find_courses,
    find_theme,
    mark_theme_completed,
    sort_courses_by_progress,
)
from storage import load_courses, save_courses
from utils import input_int, input_nonempty, input_theme_list

DATA_FILE = "data/courses.json"

MENU = """
Трекер прогресса обучения
1. Показать курсы
2. Добавить курс
3. Посмотреть тему
4. Отметить тему пройденной
5. Найти курс по названию
6. Курсы с прогрессом не менее X%
7. Курсы, отсортированные по прогрессу
0. Выход
"""


def show_courses(courses: dict[int, dict]) -> None:
    if not courses:
        print("Курсов пока нет.")
        return

    for course_id, course in courses.items():
        progress = calculate_progress(course)
        print(f"{course_id}. {course['name']} — {progress:.0f}%")


def show_theme(course: dict, theme_name: str) -> None:
    theme = find_theme(course, theme_name)
    if theme is None:
        print(f"Тема '{theme_name}' не найдена в курсе '{course['name']}'.")
        return

    status = "пройдена" if theme["is_completed"] else "не пройдена"
    print(f"Курс: {course['name']}")
    print(f"Тема: {theme['name']}")
    print(f"Статус: {status}")


def get_course(courses: dict[int, dict], course_id: int) -> dict | None:
    return courses.get(course_id)


def main() -> None:
    courses = load_courses(DATA_FILE)

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_courses(courses)
        elif choice == "2":
            name = input_nonempty("Название курса: ")
            theme_names = input_theme_list("Темы курса через запятую: ")
            add_course(courses, name, theme_names)
            print("Курс добавлен.")
        elif choice == "3":
            course_id = input_int("Идентификатор курса: ")
            course = get_course(courses, course_id)
            if course is None:
                print("Курс не найден.")
                continue
            theme_name = input_nonempty("Название темы: ")
            show_theme(course, theme_name)
        elif choice == "4":
            course_id = input_int("Идентификатор курса: ")
            course = get_course(courses, course_id)
            if course is None:
                print("Курс не найден.")
                continue
            theme_name = input_nonempty("Название темы: ")
            if mark_theme_completed(course, theme_name):
                print(f"Тема '{theme_name}' отмечена как пройденная.")
            else:
                print(f"Тема '{theme_name}' не найдена.")
        elif choice == "5":
            query = input_nonempty("Подстрока для поиска: ")
            found = list(find_courses(courses, query))
            if not found:
                print("Ничего не найдено.")
            for course_id, course in found:
                print(f"{course_id}. {course['name']}")
        elif choice == "6":
            min_percent = input_int("Минимальный процент прогресса: ")
            found = list(filter_courses_by_progress(courses, min_percent))
            if not found:
                print("Подходящих курсов нет.")
            for course_id, course in found:
                progress = calculate_progress(course)
                print(f"{course_id}. {course['name']} — {progress:.0f}%")
        elif choice == "7":
            sorted_courses = sort_courses_by_progress(courses, reverse=True)
            for course_id, course in sorted_courses:
                progress = calculate_progress(course)
                print(f"{course_id}. {course['name']} — {progress:.0f}%")
        elif choice == "0":
            save_courses(DATA_FILE, courses)
            print("Данные сохранены. До встречи!")
            break
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
