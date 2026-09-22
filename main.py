from courses import (
    add_course,
    calculate_progress,
    filter_courses_by_progress,
    find_courses,
    find_theme,
    mark_theme_completed,
    sort_courses_by_progress,
)
from models import Course, Progress, User
from storage import (
    load_courses,
    load_progresses,
    load_users,
    save_courses,
    save_progresses,
    save_users,
)
from utils import input_int, input_nonempty, input_theme_list

COURSES_FILE = "data/courses.json"
USERS_FILE = "data/users.json"
PROGRESS_FILE = "data/progress.json"

MENU = """
Трекер прогресса обучения

1. Показать курсы
2. Добавить курс
3. Посмотреть тему
4. Отметить тему пройденной
5. Найти курс по названию
6. Курсы с прогрессом не менее X%
7. Курсы, отсортированные по прогрессу
8. Показать пользователя
0. Выход
"""


def show_courses(courses: list[Course], user: User) -> None:
    if not courses:
        print("Курсов пока нет.")
        return
    for course in courses:
        print(
            f"{course.id}. {course.name} — "
            f"{calculate_progress(user, course):.0f}%"
        )


def show_theme(course: Course, user: User, theme_name: str) -> None:
    theme = find_theme(course, theme_name)
    if theme is None:
        print(f"Тема '{theme_name}' не найдена в курсе '{course.name}'.")
        return
    progress = user.get_progress(course.id)
    completed = progress is not None and progress.is_theme_completed(theme)
    status = "пройдена" if completed else "не пройдена"
    print(f"Курс: {course.name}")
    print(f"Тема: {theme.name}")
    print(f"Статус: {status}")


def get_course(courses: list[Course], course_id: int) -> Course | None:
    for course in courses:
        if course.id == course_id:
            return course
    return None


def get_current_user(users: list[User]) -> User:
    if users:
        return users[0]
    user = User(1, "Студент", "student@example.com")
    users.append(user)
    return user


def main() -> None:
    courses = load_courses(COURSES_FILE)
    users = load_users(USERS_FILE)
    progresses = load_progresses(PROGRESS_FILE, users, courses)
    user = get_current_user(users)

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_courses(courses, user)
        elif choice == "2":
            name = input_nonempty("Название курса: ")
            theme_names = input_theme_list("Темы курса через запятую: ")
            course = add_course(courses, name, theme_names)
            print(f"Курс '{course.name}' добавлен с ID {course.id}.")
        elif choice == "3":
            course_id = input_int("Идентификатор курса: ")
            course = get_course(courses, course_id)
            if course is None:
                print("Курс не найден.")
                continue
            theme_name = input_nonempty("Название темы: ")
            show_theme(course, user, theme_name)
        elif choice == "4":
            course_id = input_int("Идентификатор курса: ")
            course = get_course(courses, course_id)
            if course is None:
                print("Курс не найден.")
                continue
            theme_name = input_nonempty("Название темы: ")
            if mark_theme_completed(user, course, theme_name, progresses):
                print(f"Тема '{theme_name}' отмечена как пройденная.")
            else:
                print(f"Тема '{theme_name}' не найдена.")
        elif choice == "5":
            query = input_nonempty("Подстрока для поиска: ")
            found = list(find_courses(courses, query))
            if not found:
                print("Ничего не найдено.")
            for course in found:
                print(f"{course.id}. {course.name}")
        elif choice == "6":
            min_percent = input_int("Минимальный процент прогресса: ")
            found = list(
                filter_courses_by_progress(courses, user, min_percent)
            )
            if not found:
                print("Подходящих курсов нет.")
            for course in found:
                print(
                    f"{course.id}. {course.name} — "
                    f"{calculate_progress(user, course):.0f}%"
                )
        elif choice == "7":
            for course in sort_courses_by_progress(
                courses, user, reverse=True
            ):
                print(
                    f"{course.id}. {course.name} — "
                    f"{calculate_progress(user, course):.0f}%"
                )
        elif choice == "8":
            print(user)
            for progress in progresses:
                if progress.user.id == user.id:
                    print(f"  {progress}")
        elif choice == "0":
            save_courses(COURSES_FILE, courses)
            save_users(USERS_FILE, users)
            save_progresses(PROGRESS_FILE, progresses)
            print("Данные сохранены. До встречи!")
            break
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
