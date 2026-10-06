from typing import Iterator

from models import Course, Progress, Theme, User


def add_course(
    courses: list[Course], name: str, theme_names: list[str]
) -> Course:
    course_id = max((course.id for course in courses), default=0) + 1
    themes = [
        Theme(theme_id=index, name=theme_name)
        for index, theme_name in enumerate(theme_names, start=1)
    ]
    course = Course(course_id=course_id, name=name, themes=themes)
    courses.append(course)
    return course


def find_courses(courses: list[Course], query: str) -> Iterator[Course]:
    for course in courses:
        if query.lower() in course.name.lower():
            yield course


def find_theme(course: Course, theme_name: str) -> Theme | None:
    return course.get_theme(theme_name)


def find_course_by_id(
    courses: list[Course], course_id: int
) -> Course | None:
    """Найти курс по идентификатору."""
    for course in courses:
        if course.id == course_id:
            return course
    return None


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_user_by_name(users: list[User], name: str) -> User | None:
    """Найти пользователя по имени (без учёта регистра и пробелов)."""
    wanted = name.strip().casefold()
    for user in users:
        if user.name.casefold() == wanted:
            return user
    return None


def find_progress_by_id(
    progresses: list[Progress], progress_id: int
) -> Progress | None:
    """Найти объект прогресса по идентификатору."""
    for progress in progresses:
        if progress.id == progress_id:
            return progress
    return None


def get_or_create_progress(
    user: User, course: Course, progresses: list[Progress]
) -> Progress:
    progress = user.get_progress(course.id)
    if progress is not None:
        return progress

    progress_id = max((item.id for item in progresses), default=0) + 1
    progress = Progress(progress_id, user, course)
    progresses.append(progress)
    user.add_progress(progress)
    return progress


def mark_theme_completed(
    user: User, course: Course, theme_name: str, progresses: list[Progress]
) -> bool:
    theme = find_theme(course, theme_name)
    if theme is None:
        return False
    progress = get_or_create_progress(user, course, progresses)
    return progress.mark_theme_completed(theme)


def calculate_progress(user: User, course: Course) -> float:
    progress = user.get_progress(course.id)
    if progress is None:
        return 0.0
    return progress.calculate_percent()


def filter_courses_by_progress(
    courses: list[Course], user: User, min_percent: float
) -> Iterator[Course]:
    for course in courses:
        if calculate_progress(user, course) >= min_percent:
            yield course


def sort_courses_by_progress(
    courses: list[Course], user: User, reverse: bool = False
) -> list[Course]:
    return sorted(
        courses,
        key=lambda course: calculate_progress(user, course),
        reverse=reverse,
    )
