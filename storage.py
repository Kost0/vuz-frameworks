import json

from models import Course, Progress, User


def load_courses(filename: str) -> list[Course]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_courses = json.load(file)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден, начинаем с пустого списка.")
        return []
    except json.JSONDecodeError:
        print(f"Файл '{filename}' повреждён, начинаем с пустого списка.")
        return []

    courses = []
    for course_id, course_data in raw_courses.items():
        data = {"id": int(course_id), **course_data}
        themes = []
        for index, theme_data in enumerate(data.get("themes", []), start=1):
            theme = dict(theme_data)
            theme["id"] = int(theme.get("id", index))
            themes.append(theme)
        data["themes"] = themes
        courses.append(Course.from_data(data))
    return courses


def save_courses(filename: str, courses: list[Course]) -> None:
    raw_courses = {
        str(course.id): {
            "name": course.name,
            "themes": [
                {"name": theme.name, "is_completed": False}
                for theme in course.themes
            ],
        }
        for course in courses
    }
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_courses, file, ensure_ascii=False, indent=2)


def load_users(filename: str) -> list[User]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_users = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    if isinstance(raw_users, dict):
        raw_users = list(raw_users.values())
    return [User.from_data(user) for user in raw_users]


def save_users(filename: str, users: list[User]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            [user.to_data() for user in users],
            file,
            ensure_ascii=False,
            indent=2,
        )


def load_progresses(
    filename: str, users: list[User], courses: list[Course]
) -> list[Progress]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_progresses = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    user_by_id = {user.id: user for user in users}
    course_by_id = {course.id: course for course in courses}
    progresses = []
    for data in raw_progresses:
        user = user_by_id.get(int(data["user_id"]))
        course = course_by_id.get(int(data["course_id"]))
        if user is None or course is None:
            continue
        progress = Progress(
            progress_id=int(data["id"]),
            user=user,
            course=course,
            completed_theme_ids=[
                int(x) for x in data.get("completed_theme_ids", [])
            ],
        )
        progresses.append(progress)
        user.add_progress(progress)
    return progresses


def save_progresses(filename: str, progresses: list[Progress]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            [progress.to_data() for progress in progresses],
            file,
            ensure_ascii=False,
            indent=2,
        )
