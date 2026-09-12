from courses import (
    add_course,
    calculate_progress,
    find_courses,
    find_theme,
    mark_theme_completed,
)


def test_add_course():
    courses = {}
    course_id = add_course(courses, "Python", ["Переменные", "Циклы"])

    assert len(courses) == 1
    assert courses[course_id]["name"] == "Python"


def test_find_theme():
    courses = {}
    course_id = add_course(courses, "Python", ["Переменные"])

    theme = find_theme(courses[course_id], "Переменные")

    assert theme is not None
    assert theme["is_completed"] is False


def test_mark_theme_completed():
    courses = {}
    course_id = add_course(courses, "Python", ["Переменные"])

    assert mark_theme_completed(courses[course_id], "Переменные")
    assert courses[course_id]["themes"][0]["is_completed"] is True


def test_mark_theme_completed_not_found():
    courses = {}
    course_id = add_course(courses, "Python", ["Переменные"])

    assert not mark_theme_completed(courses[course_id], "Несуществующая тема")


def test_calculate_progress():
    courses = {}
    course_id = add_course(courses, "Python", ["A", "B"])
    mark_theme_completed(courses[course_id], "A")

    assert calculate_progress(courses[course_id]) == 50.0


def test_find_courses():
    courses = {}
    add_course(courses, "Python для бэкенда", ["A"])
    add_course(courses, "Java", ["B"])

    found = list(find_courses(courses, "python"))

    assert len(found) == 1
