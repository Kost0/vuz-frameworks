from typing import Iterator


def add_course(
    courses: dict[int, dict], name: str, theme_names: list[str]
) -> int:
    course_id = max(courses.keys(), default=0) + 1
    themes = [
        {"name": theme_name, "is_completed": False}
        for theme_name in theme_names
    ]
    courses[course_id] = {"name": name, "themes": themes}

    return course_id


def find_courses(
    courses: dict[int, dict], query: str
) -> Iterator[tuple[int, dict]]:
    for course_id, course in courses.items():
        if query.lower() in course["name"].lower():
            yield course_id, course


def find_theme(course: dict, theme_name: str) -> dict | None:
    for theme in course["themes"]:
        if theme["name"] == theme_name:
            return theme

    return None


def mark_theme_completed(course: dict, theme_name: str) -> bool:
    theme = find_theme(course, theme_name)
    if theme is None:
        return False

    theme["is_completed"] = True

    return True


def calculate_progress(course: dict) -> float:
    themes = course["themes"]
    if not themes:
        return 0.0

    completed = sum(theme["is_completed"] for theme in themes)

    return completed / len(themes) * 100


def filter_courses_by_progress(
    courses: dict[int, dict], min_percent: float
) -> Iterator[tuple[int, dict]]:
    for course_id, course in courses.items():
        if calculate_progress(course) >= min_percent:
            yield course_id, course


def sort_courses_by_progress(
    courses: dict[int, dict], reverse: bool = False
) -> list[tuple[int, dict]]:
    return sorted(
        courses.items(),
        key=lambda item: calculate_progress(item[1]),
        reverse=reverse,
    )
