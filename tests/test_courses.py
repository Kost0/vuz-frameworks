from models import Course, Progress, Theme, User
from courses import (
    add_course,
    calculate_progress,
    find_courses,
    find_theme,
    mark_theme_completed,
    sort_courses_by_progress,
)


def make_user() -> User:
    return User(1, "Иван", "ivan@example.com")


def test_theme_creation_and_string():
    theme = Theme(1, "Переменные")
    assert theme.id == 1
    assert str(theme) == "1. Переменные"


def test_course_creation_and_theme_search():
    course = Course(1, "Python", [Theme(1, "Переменные")])
    assert course.get_theme("Переменные") is not None
    assert course.get_theme("Нет") is None


def test_add_course_creates_objects():
    courses = []
    course = add_course(courses, "Python", ["Переменные", "Циклы"])
    assert len(courses) == 1
    assert isinstance(course, Course)
    assert all(isinstance(theme, Theme) for theme in course.themes)
    assert course.name == "Python"


def test_find_theme():
    courses = []
    course = add_course(courses, "Python", ["Переменные"])
    theme = find_theme(course, "Переменные")
    assert theme is not None
    assert theme.name == "Переменные"


def test_mark_theme_completed_and_progress():
    courses = []
    progresses = []
    user = make_user()
    course = add_course(courses, "Python", ["A", "B"])
    assert mark_theme_completed(user, course, "A", progresses)
    assert calculate_progress(user, course) == 50.0
    assert user.get_progress(course.id) is not None


def test_mark_theme_completed_not_found():
    courses = []
    progresses = []
    user = make_user()
    course = add_course(courses, "Python", ["A"])
    assert not mark_theme_completed(
        user, course, "Несуществующая тема", progresses
    )


def test_find_courses():
    courses = []
    add_course(courses, "Python для бэкенда", ["A"])
    add_course(courses, "Java", ["B"])
    found = list(find_courses(courses, "python"))
    assert len(found) == 1
    assert found[0].name == "Python для бэкенда"


def test_sort_courses_by_progress():
    courses = []
    progresses = []
    user = make_user()
    first = add_course(courses, "Python", ["A"])
    second = add_course(courses, "Go", ["A", "B"])
    mark_theme_completed(user, first, "A", progresses)
    mark_theme_completed(user, second, "A", progresses)
    result = sort_courses_by_progress(courses, user, reverse=True)
    assert result == [first, second]


def test_progress_links_user_and_course():
    user = make_user()
    course = Course(1, "Python", [Theme(1, "A")])
    progress = Progress(1, user, course)
    user.add_progress(progress)
    assert progress.user is user
    assert progress.course is course
